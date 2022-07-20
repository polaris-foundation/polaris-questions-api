import csv
from datetime import date, datetime, timedelta, timezone
from io import StringIO
from typing import Dict, Generator, List, Optional, Tuple

from flask_batteries_included.helpers.request_arg import RequestArg
from flask_batteries_included.helpers.timestamp import (
    parse_iso8601_to_date_typesafe,
    split_timestamp,
)
from flask_batteries_included.sqldb import db, generate_uuid
from sqlalchemy.sql import join, select

from dhos_questions_api.models.answer import Answer
from dhos_questions_api.models.group import Group
from dhos_questions_api.models.question import Question
from dhos_questions_api.models.survey import Survey
from dhos_questions_api.queries.softdelete import QueryWithSoftDelete


def create_survey(survey_details: Dict) -> Dict:
    group: Group = Group.query.filter_by(group=survey_details["group"]).first()
    if group is None:
        raise KeyError(f"Question group {survey_details['group']} not found.")

    new_survey = Survey(
        uuid=generate_uuid(),
        group=group,
        user_id=survey_details["user_id"],
        user_type=survey_details["user_type"],
    )
    db.session.add(new_survey)
    db.session.commit()
    return new_survey.to_dict()


def get_surveys() -> List[Dict]:
    start_date: str = RequestArg.string("start_date", default=None)
    end_date: str = RequestArg.string("end_date", default=None)

    q: QueryWithSoftDelete = Survey.query

    if start_date:
        q = q.filter(Survey.modified >= start_date)
    if end_date:
        q = q.filter(Survey.modified <= end_date)

    surveys: List[Survey] = q.all()
    return [survey.to_dict() for survey in surveys]


def get_survey_by_uuid(survey_uuid: str) -> Dict:
    return Survey.query.filter_by(uuid=survey_uuid).first_or_404().to_dict()


def update_survey(survey_uuid: str, survey_details: Dict) -> Dict:
    survey: Survey = Survey.query.filter_by(uuid=survey_uuid).first_or_404()
    schema: Dict = Survey.schema()
    for key in survey_details:
        if key not in schema["updatable"]:
            raise KeyError(f"{key} is not an updatable property")

        if key in ["completed", "declined"]:
            ts, tz = split_timestamp(survey_details[key])
            setattr(survey, key, ts)
            setattr(survey, f"{key}_tz", tz)
        else:
            setattr(survey, key, survey_details[key])

    db.session.commit()
    return survey.to_dict()


def get_survey_responses(
    start_date: Optional[str] = None, end_date: Optional[str] = None
) -> Generator[str, None, None]:
    # select survey_id, question, value from "dhos-dev-dhos-questions".answer a
    # left join "dhos-dev-dhos-questions".question q on q.uuid = a.question_id
    session = db.session
    j = join(Answer, Question, Answer.question_id == Question.uuid)
    q = select(
        [Answer.created, Answer.survey_id, Question.question, Answer.value]
    ).select_from(j)

    if start_date:
        start_date_parsed: date = parse_iso8601_to_date_typesafe(start_date)
        q = q.where(Answer.modified >= start_date_parsed)
    if end_date:
        end_date_parsed: date = parse_iso8601_to_date_typesafe(end_date)
        end_date_beginning: datetime = datetime(
            end_date_parsed.year,
            end_date_parsed.month,
            end_date_parsed.day,
            tzinfo=timezone.utc,
        )
        end_date_next_midnight: datetime = end_date_beginning + timedelta(days=1)
        q = q.where(Answer.modified < end_date_next_midnight)

    answers = session.execute(q)
    header = ["created", "survey_id", "question", "answer"]

    return _iter_csv(data=answers, header=header)


def _iter_csv(data: List[Tuple], header: List) -> Generator[str, None, None]:
    line = StringIO()
    writer = csv.writer(line)
    header_written = False
    for csv_line in data:
        if header_written is False:
            writer.writerow(header)
            header_written = True
        writer.writerow(csv_line)
        line.seek(0)
        yield line.read()
        line.truncate(0)
        line.seek(0)

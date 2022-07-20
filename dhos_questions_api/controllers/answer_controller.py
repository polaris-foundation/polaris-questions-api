from datetime import datetime
from typing import Dict, List, Optional

from flask_batteries_included.helpers.timestamp import (
    parse_datetime_to_iso8601,
    split_timestamp,
)
from flask_batteries_included.sqldb import db, generate_uuid
from she_logging import logger

from dhos_questions_api.models.answer import Answer
from dhos_questions_api.models.question import Question
from dhos_questions_api.models.survey import Survey
from dhos_questions_api.queries.softdelete import QueryWithSoftDelete


def create_answers(answers: List[Dict]) -> List[Dict]:
    db_answers = []
    answer_batch: Dict = {}

    for answer in answers:
        if not validate_answer(answer):
            raise KeyError("Answer failed validation")
        if not answer["question_id"] in answer_batch:
            answer_batch[answer["question_id"]] = []
        answer_batch[answer["question_id"]].append(answer)

    for question_uuid in answer_batch:
        if not validate_answer_batch(question_uuid, answer_batch[question_uuid]):
            raise KeyError("Answers failed batch validation")

    for answer in answers:
        new_answer = Answer(
            uuid=generate_uuid(),
            survey_id=answer["survey_id"],
            question_id=answer["question_id"],
            value=answer["value"],
        )
        if "text" in answer:
            new_answer.text = answer["text"]

        db.session.add(new_answer)
        db_answers.append(new_answer)

    db.session.commit()
    return [answer.to_dict() for answer in db_answers]


def create_answers_for_survey(survey_id: str, answers: List[Dict]) -> List[Dict]:
    db_answers = []
    answer_batch: Dict = {}

    for answer in answers:
        if not validate_answer(answer, survey_id):
            raise KeyError("Answer failed validation")
        if not answer["question_id"] in answer_batch:
            answer_batch[answer["question_id"]] = []
        answer_batch[answer["question_id"]].append(answer)

    for question_id in answer_batch:
        if not validate_answer_batch(question_id, answer_batch[question_id]):
            raise KeyError("Answers failed batch validation")

    for answer in answers:
        new_answer = Answer(
            uuid=generate_uuid(),
            survey_id=survey_id,
            question_id=answer["question_id"],
            value=answer["value"],
        )
        if "text" in answer:
            new_answer.text = answer["text"]

        db.session.add(new_answer)
        db_answers.append(new_answer)

    # Update the survey completion date to the most recent
    # submitted batch of answers
    survey = Survey.query.filter_by(uuid=survey_id).first()
    now_iso8601 = parse_datetime_to_iso8601(datetime.utcnow())
    if now_iso8601 is None:
        raise ValueError("Couldn't generate timestamp")
    ts, tz = split_timestamp(now_iso8601 + "Z")
    survey.completed = ts
    survey.completed_tz = tz

    db.session.commit()
    return [answer.to_dict() for answer in db_answers]


def get_answers(
    start_date: Optional[str] = None, end_date: Optional[str] = None
) -> List[Dict]:
    q: QueryWithSoftDelete = Answer.query
    if start_date:
        q = q.filter(Answer.modified >= start_date)
    if end_date:
        q = q.filter(Answer.modified <= end_date)

    answers: List[Answer] = q.all()
    return [answer.to_dict() for answer in answers]


def get_answers_by_survey_uuid(survey_uuid: str) -> List[Dict]:
    q = Answer.query.filter(Answer.survey_id == survey_uuid)
    return [answer.to_dict() for answer in q]


def get_answers_by_survey_and_question_uuid(
    survey_uuid: str, question_uuid: str
) -> List[Dict]:
    q = Answer.query.filter_by(survey_id=survey_uuid, question_id=question_uuid)
    return [answer.to_dict() for answer in q]


def get_answer_by_uuid(answer_id: str) -> Dict:
    answer = Answer.query.filter_by(uuid=answer_id).first_or_404()
    return answer.to_dict()


def update_answer(answer_uuid: str, answer: Dict) -> Dict:
    answer_db = Answer.query.filter_by(uuid=answer_uuid).first_or_404()
    schema = Answer.schema()
    for property_to_update in answer:
        if len(answer[property_to_update]) == 0:
            raise KeyError(
                "Empty fields should not be sent, property '%s' is empty",
                property_to_update,
            )

        if property_to_update not in schema["updatable"]:
            raise KeyError("Property '%s' cannot be updated", property_to_update)

        answer_db.set_property(property_to_update, answer[property_to_update])

    db.session.commit()
    return answer_db.to_dict()


def is_int(input_string: str) -> bool:
    try:
        int(input_string)
    except ValueError:
        logger.info("Could not parse integer '%s'", input_string)
        return False
    return True


def validate_answer(answer: Dict, survey_uuid: str = None) -> bool:
    if not survey_uuid:
        survey_uuid = answer.get("survey_id")

    if survey_uuid is None:
        raise ValueError("No survey ID provided")

    survey: Optional[Survey] = Survey.query.filter_by(uuid=survey_uuid).first()
    if not survey:
        logger.info("Could not find survey with UUID %s", survey_uuid)
        return False

    question: Optional[Question] = Question.query.filter_by(
        uuid=answer["question_id"]
    ).first()
    if question is None:
        logger.error("Could not find question with UUID %s", answer["question_id"])
        return False

    if is_question_already_answered(answer["question_id"], survey_uuid):
        logger.info(
            "Question %s in survey %s already answered",
            answer["question_id"],
            survey_uuid,
        )
        return False

    return True


def validate_answer_batch(question_uuid: str, answers: List[Dict]) -> bool:
    question = Question.query.filter_by(uuid=question_uuid).first()

    if question.question_type.value in (0, 1, 3, 4, 5):
        if len(answers) > 1:
            logger.info(
                "%d answers sent for question %s when only 1 was expected",
                len(answers),
                question_uuid,
            )
            return False

    if question.question_type.value == 0:
        return True

    if question.question_type.value == 1:
        return is_int(answers[0]["value"])

    if question.question_type.value == 3:
        return is_answer_from_available_options(question, answers[0])

    if question.question_type.value == 5:
        return is_answer_in_question_range(question, answers[0])

    if question.question_type.value in [2, 6]:
        return are_all_answers_from_available_options(question, answers)

    return True


def is_question_already_answered(question_uuid: str, survey_uuid: str) -> bool:
    a = Answer.query.filter_by(question_id=question_uuid, survey_id=survey_uuid).first()
    if a is None:
        return False
    return True


def is_answer_from_available_options(question: Question, answer: Dict) -> bool:

    for option in question.question_options:
        if option.value == answer["value"]:
            return True
    logger.info("Answer value %s is not in the available options", answer["value"])
    return False


def is_answer_in_question_range(question: Question, answer: Dict) -> bool:
    for option in question.question_options:
        if option.question_option_type.value == 2:
            min_val = float(option.value)
        if option.question_option_type.value == 3:
            max_val = float(option.value)
        if option.question_option_type.value == 4:
            interval = float(option.value)

        value = float(answer["value"])

    if value >= min_val and value <= max_val:
        if (value - min_val) % interval == 0:
            logger.info(
                "Answer is within value range, but has failed the interval check"
            )
            return True

    logger.info(
        "Answer not in acceptable range",
        extra={
            "answer_value": value,
            "answer_min": min_val,
            "answer_max": max_val,
            "answer_interval": interval,
        },
    )
    return False


def are_all_answers_from_available_options(
    question: Question, answers: List[Dict]
) -> bool:
    if are_any_options_values_duplicated(answers=answers):
        return False

    for answer in answers:
        if not is_answer_from_available_options(question, answer):
            return False

    return True


def are_any_options_values_duplicated(answers: List[Dict]) -> bool:
    option_values: List = []
    for answer in answers:
        if answer["value"] in option_values:
            return True

        option_values.append(answer["value"])

    return False

from typing import Dict, List

from flask_batteries_included.sqldb import db, generate_uuid

from dhos_questions_api.models.group import Group
from dhos_questions_api.models.question import Question
from dhos_questions_api.models.question_option import QuestionOption
from dhos_questions_api.models.question_option_type import QuestionOptionType
from dhos_questions_api.models.question_type import QuestionType
from dhos_questions_api.models.survey import Survey


def create_question(question_details: Dict) -> Dict:
    return create_question_from_dict(question_details)


def create_question_from_dict(question: Dict) -> Dict:
    question_type = QuestionType.query.filter_by(
        value=question["question_type"]["value"]
    ).first()

    if not question_type:
        raise KeyError(
            f"Question type {question['question_type']['value']} does not exist"
        )

    options = []
    if "question_options" in question:
        if question["question_type"]["value"] in [0, 1]:
            raise KeyError(
                f"Question type {question['question_type']['value']} should not have options"
            )

        for option in question["question_options"]:
            question_option_type_value = option["question_option_type"]
            db_option_type = QuestionOptionType.query.filter_by(
                value=question_option_type_value
            ).first()
            if not db_option_type:
                raise KeyError(
                    f"Question Option Type {question_option_type_value} does not exist"
                )

            qo_schema = QuestionOption.schema()
            qo_create = {**qo_schema["optional"], **qo_schema["required"]}

            qo = QuestionOption(
                uuid=generate_uuid(), question_option_type=db_option_type
            )
            for key in qo_create:
                if key != "question_option_type":
                    if key in option:
                        setattr(qo, key, option[key])

            options.append(qo)

    groups = []
    if "groups" in question:
        for group in question["groups"]:
            query_result = Group.query.filter_by(group=group["group"]).first()
            if query_result:
                db_group = query_result
            else:
                db_group = Group(uuid=generate_uuid(), group=group["group"])
            groups.append(db_group)

    insert = Question(
        uuid=generate_uuid(),
        question=question["question"],
        question_type=question_type,
        groups=groups,
        question_options=options,
    )

    db.session.add(insert)
    db.session.commit()

    return insert.to_dict()


def create_question_type_from_dict(question_type: Dict) -> Dict:
    candidate_value = QuestionType.query.filter_by(value=question_type["value"]).first()
    candidate_uuid = QuestionType.query.filter_by(uuid=question_type["uuid"]).first()

    if candidate_value:
        raise KeyError(f"Question type '{question_type['value']}' already exists")

    if candidate_uuid:
        raise KeyError(
            f"Question type with UUID '{question_type['uuid']}' already exists"
        )

    insert = QuestionType(uuid=question_type["uuid"], value=question_type["value"])

    db.session.add(insert)
    db.session.commit()

    return insert.to_dict()


def create_question_option_type_from_dict(question_option_type: Dict) -> Dict:
    candidate_value = QuestionOptionType.query.filter_by(
        value=question_option_type["value"]
    ).first()
    candidate_uuid = QuestionOptionType.query.filter_by(
        uuid=question_option_type["uuid"]
    ).first()

    if candidate_value:
        raise KeyError(
            f"Question option type '{question_option_type['value']}' already exists"
        )

    if candidate_uuid:
        raise KeyError(
            f"Question option type with UUID '{question_option_type['uuid']}' already exists"
        )

    insert = QuestionOptionType(
        uuid=question_option_type["uuid"], value=question_option_type["value"]
    )

    db.session.add(insert)
    db.session.commit()

    return insert.to_dict()


def get_question_by_uuid(question_uuid: str) -> Dict:
    return Question.query.filter_by(uuid=question_uuid).first_or_404().to_dict()


def get_questions_by_survey_uuid(survey_uuid: str) -> List[Dict]:
    survey = Survey.query.filter_by(uuid=survey_uuid).first_or_404()
    return get_questions_by_question_group_uuid(survey.group.uuid)


def get_questions_by_question_group_uuid(group_uuid: str) -> List[Dict]:
    q = Question.query.filter(Question.groups.any(Group.uuid == group_uuid))
    return [question.to_dict() for question in q]


def create_question_type(question_type_details: Dict) -> Dict:
    return create_question_type_from_dict(question_type_details)


def create_question_option_type(question_option_type_details: Dict) -> Dict:
    return create_question_option_type_from_dict(question_option_type_details)

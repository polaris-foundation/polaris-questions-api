from behave import step
from behave.runner import Context
from clients import survey_client
from faker import Faker
from helpers import question as question_helper
from requests import Response


@step("a new survey is created")
def create_new_survey(context: Context) -> None:
    body = {
        "group": context.question_group,
        "user_id": context.patient_uuid,
        "user_type": "patient",
    }
    context.survey_body = body

    response: Response = survey_client.post_survey(jwt=context.current_jwt, body=body)
    response.raise_for_status()
    response_json: dict = response.json()
    assert "uuid" in response_json
    context.survey_uuid = context.survey_uuid + [response_json["uuid"]]


@step("the survey can be retrieved by its uuid")
def get_survey_by_uuid(context: Context) -> None:
    response: Response = survey_client.get_survey(
        jwt=context.current_jwt, uuid=context.survey_uuid[-1]
    )
    response.raise_for_status()
    context.api_survey_body = response.json()


@step("the survey can be seen in all surveys")
def assert_survey_in_all_surveys(context: Context) -> None:
    response: Response = survey_client.get_all_surveys(jwt=context.current_jwt)
    response.raise_for_status()
    all_ids: list = [q["uuid"] for q in response.json()]
    assert context.survey_uuid[-1] in all_ids


@step("the retrieved survey matches that previously posted")
def assert_question_body(context: Context) -> None:
    assert context.survey_body["user_id"] == context.api_survey_body["user_id"]
    assert context.survey_body["user_type"] == context.api_survey_body["user_type"]
    assert context.survey_body["group"] == context.api_survey_body["group"]["group"]


@step("all the answers to the survey are provided")
def submit_all_answers(context: Context) -> None:
    survey_uuid: str = context.survey_uuid[-1]
    response: Response = survey_client.get_all_survey_questions(
        jwt=context.current_jwt, uuid=survey_uuid
    )
    response.raise_for_status()
    questions = response.json()

    fake: Faker = Faker()
    answers = []
    for question in questions:
        if (
            question["question_type"]["value"]
            == question_helper.QuestionTypes.FREE_TEXT.value
        ):
            answers += [
                {
                    "survey_id": survey_uuid,
                    "question_id": question["uuid"],
                    "value": fake.sentence(),
                }
            ]
        elif (
            question["question_type"]["value"]
            == question_helper.QuestionTypes.INTEGER.value
        ):
            answers += [
                {
                    "survey_id": survey_uuid,
                    "question_id": question["uuid"],
                    "value": str(fake.random_number()),
                }
            ]
        elif (
            question["question_type"]["value"]
            == question_helper.QuestionTypes.RANGE.value
        ):
            answers += [
                {
                    "survey_id": survey_uuid,
                    "question_id": question["uuid"],
                    "value": "5",
                }
            ]
        else:
            answers += [
                {
                    "survey_id": survey_uuid,
                    "question_id": question["uuid"],
                    "value": "1",
                }
            ]

    response = survey_client.post_survey_answers(
        jwt=context.current_jwt, uuid=survey_uuid, body=answers
    )
    response.raise_for_status()
    context.survey_answers = answers


@step("the submitted answers can be seen in all answers for that survey")
def assert_answers_in_all_answers_for_survey(context: Context) -> None:
    response: Response = survey_client.get_all_survey_answers(
        jwt=context.current_jwt, uuid=context.survey_uuid[-1]
    )
    response.raise_for_status()

    api_question_ids = sorted([question["question_id"] for question in response.json()])
    survey_question_ids = sorted(
        [question["question_id"] for question in context.survey_answers]
    )
    assert api_question_ids == survey_question_ids

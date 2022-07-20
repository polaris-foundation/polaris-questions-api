from behave import step
from behave.runner import Context
from clients import questions_client
from faker import Faker
from helpers import question
from requests import Response


@step("a new {question_type} question is created")
def create_new_question(context: Context, question_type: str) -> None:
    body: dict = question.get_body(
        question_type={"value": question.QuestionTypes[question_type].value}
    )
    if question_type in ["CHECKBOX", "RADIO", "DROPDOWN"]:
        body["question_options"] = [
            {
                "text": "Option 1",
                "value": "1",
                "question_option_type": question.QuestionOptionTypes.FIXED.value,
            }
        ]
    elif question_type == "RANGE":
        body["question_options"] = [
            {
                "value": "1",
                "question_option_type": question.QuestionOptionTypes.RANGE_START.value,
            },
            {
                "value": "10",
                "question_option_type": question.QuestionOptionTypes.RANGE_END.value,
            },
            {
                "value": "1",
                "question_option_type": question.QuestionOptionTypes.INTERVAL.value,
            },
        ]
    if "question_group" in context:
        body["groups"].append({"group": context.question_group})
    context.question_body = body

    response: Response = questions_client.post_question(
        jwt=context.current_jwt, body=body
    )
    response.raise_for_status()
    response_json: dict = response.json()
    assert "uuid" in response_json
    context.question_uuid = context.question_uuid + [response_json["uuid"]]


@step("a new question is created from the custom question type")
def create_new_question_from_custom_type(context: Context) -> None:
    body: dict = question.get_body(question_type={"value": context.question_type_value})
    if "question_group" in context:
        body["groups"].append({"group": context.question_group})
    context.question_body = body

    response: Response = questions_client.post_question(
        jwt=context.current_jwt, body=body
    )
    response.raise_for_status()
    response_json: dict = response.json()
    assert "uuid" in response_json
    context.question_uuid = context.question_uuid + [response_json["uuid"]]


@step("the question can be retrieved by its uuid")
def get_question_by_uuid(context: Context) -> None:
    response: Response = questions_client.get_question(
        jwt=context.current_jwt, uuid=context.question_uuid[-1]
    )
    response.raise_for_status()
    context.api_question_body = response.json()


@step("the retrieved question matches that previously posted")
def assert_question_body(context: Context) -> None:
    assert context.question_body["question"] == context.api_question_body["question"]
    assert (
        context.question_body["question_type"]["value"]
        == context.api_question_body["question_type"]["value"]
    )


@step("there exists a question group")
def get_random_question_group(context: Context) -> None:
    fake: Faker = Faker()
    context.question_group = fake.word()

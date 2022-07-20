from behave import step
from behave.runner import Context
from clients import question_type_client
from helpers import question_type
from requests import Response


@step("a new question type is created")
def create_new_question_type(context: Context) -> None:
    body: dict = question_type.get_body()
    context.question_type_body = body

    response: Response = question_type_client.post_question_type(
        jwt=context.current_jwt, body=body
    )
    response.raise_for_status()
    response_json: dict = response.json()
    assert "uuid" in response_json
    assert "value" in response_json
    context.question_type_value = response_json["value"]

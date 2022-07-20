from typing import Dict

import requests
from environs import Env
from requests import Response


def _get_base_url() -> str:
    base_url: str = Env().str(
        "DHOS_QUESTIONS_BASE_URL", "http://dhos-questions-api:5000"
    )
    return f"{base_url}/dhos/v1/survey"


def post_survey(jwt: str, body: Dict) -> Response:
    return requests.post(
        _get_base_url(),
        timeout=15,
        headers={"Authorization": f"Bearer {jwt}"},
        json=body,
    )


def get_survey(jwt: str, uuid: str) -> Response:
    return requests.get(
        f"{_get_base_url()}/{uuid}",
        timeout=15,
        headers={"Authorization": f"Bearer {jwt}"},
    )


def get_all_surveys(jwt: str) -> Response:
    return requests.get(
        _get_base_url(),
        timeout=15,
        headers={"Authorization": f"Bearer {jwt}"},
    )


def get_all_survey_questions(jwt: str, uuid: str) -> Response:
    return requests.get(
        f"{_get_base_url()}/{uuid}/question",
        timeout=15,
        headers={"Authorization": f"Bearer {jwt}"},
    )


def get_survey_question(jwt: str, survey_uuid: str, question_uuid: str) -> Response:
    return requests.get(
        f"{_get_base_url()}/{survey_uuid}/question/{question_uuid}",
        timeout=15,
        headers={"Authorization": f"Bearer {jwt}"},
    )


def post_survey_answers(jwt: str, uuid: str, body: Dict) -> Response:
    return requests.post(
        f"{_get_base_url()}/{uuid}/answer",
        timeout=15,
        headers={"Authorization": f"Bearer {jwt}"},
        json=body,
    )


def get_all_survey_answers(jwt: str, uuid: str) -> Response:
    return requests.get(
        f"{_get_base_url()}/{uuid}/answer",
        timeout=15,
        headers={"Authorization": f"Bearer {jwt}"},
    )

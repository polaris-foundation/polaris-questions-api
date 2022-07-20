from typing import Dict

import requests
from environs import Env
from requests import Response


def _get_base_url() -> str:
    base_url: str = Env().str(
        "DHOS_QUESTIONS_BASE_URL", "http://dhos-questions-api:5000"
    )
    return f"{base_url}/dhos/v1/question_type"


def post_question_type(jwt: str, body: Dict) -> Response:
    return requests.post(
        _get_base_url(),
        timeout=15,
        headers={"Authorization": f"Bearer {jwt}"},
        json=body,
    )

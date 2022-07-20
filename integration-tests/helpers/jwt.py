import uuid

from environs import Env
from jose import jwt as jose_jwt


def get_system_token() -> str:
    env: Env = Env()
    hs_issuer: str = env.str("HS_ISSUER")
    hs_key: str = env.str("HS_KEY")
    proxy_url: str = env.str("PROXY_URL")
    scope: str = " ".join(
        [
            "read:gdm_answer",
            "read:gdm_answer_all",
            "read:gdm_question",
            "read:gdm_survey",
            "read:gdm_survey_all",
            "write:gdm_answer",
            "write:gdm_answer_all",
            "write:gdm_question",
            "write:gdm_survey",
        ]
    )
    return jose_jwt.encode(
        {
            "metadata": {"system_id": "dhos-robot", "can_edit_ews": True},
            "iss": hs_issuer,
            "aud": proxy_url + "/",
            "scope": scope,
            "exp": 9_999_999_999,
        },
        key=hs_key,
        algorithm="HS512",
    )


def get_patient_token() -> str:
    env: Env = Env()
    hs_issuer: str = env.str("HS_ISSUER")
    hs_key: str = env.str("HS_KEY")
    proxy_url: str = env.str("PROXY_URL")
    scope: str = " ".join(
        [
            "read:gdm_question",
            "read:gdm_survey",
            "read:gdm_answer",
            "read:gdm_answer_all",
            "write:gdm_answer",
            "write:gdm_answer_all",
        ]
    )
    return jose_jwt.encode(
        {
            "metadata": {"patient_id": str(uuid.uuid4())},
            "iss": hs_issuer,
            "aud": proxy_url + "/",
            "scope": scope,
            "exp": 9_999_999_999,
        },
        key=hs_key,
        algorithm="HS512",
    )


def decode_jwt(jwt: str) -> dict:
    decode_options: dict = {
        "verify_signature": False,
        "verify_aud": False,
        "verify_sub": False,
    }
    return jose_jwt.decode(token=jwt, key="", options=decode_options)

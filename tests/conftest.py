from typing import Any, Dict, Generator, List, Tuple

import pytest
from flask import Flask, g
from flask_batteries_included.sqldb import db
from mock import Mock
from pytest_dhos.jwt_permissions import GDM_CLINICIAN_PERMISSIONS
from pytest_mock import MockFixture

from dhos_questions_api.controllers import (
    answer_controller,
    question_controller,
    survey_controller,
)
from dhos_questions_api.models.group import Group
from dhos_questions_api.models.question_option_type import QuestionOptionType
from dhos_questions_api.models.question_type import QuestionType


@pytest.fixture
def app(mocker: MockFixture) -> Flask:
    """Fixture that creates app for testing"""
    from flask_batteries_included.helpers.security import _ProtectedRoute

    import dhos_questions_api.app

    app: Flask = dhos_questions_api.app.create_app(
        testing=True, use_pgsql=False, use_sqlite=True
    )

    def mock_claims(self: Any, verify: bool = True) -> Tuple:
        return getattr(g, "jwt_claims", {}), getattr(g, "jwt_scopes", [])

    mocker.patch.object(_ProtectedRoute, "_retrieve_jwt_claims", mock_claims)
    app.config["IGNORE_JWT_VALIDATION"] = False

    return app


@pytest.fixture
def app_context(app: Flask) -> Generator[None, None, None]:
    with app.app_context():
        yield


@pytest.fixture
def jwt_gdm_clinician_uuid(app_context: Any, jwt_scopes: Any) -> str:
    """Use this fixture to make requests as a GDM clinician"""
    from flask import g

    gdm_clinician = "4c4f1d24-2952-4d4e-b1d1-3637e33cc161"
    g.jwt_claims = {
        "clinician_id": gdm_clinician,
    }
    if jwt_scopes is None:
        g.jwt_scopes = GDM_CLINICIAN_PERMISSIONS
    else:
        if isinstance(jwt_scopes, str):
            jwt_scopes = jwt_scopes.split(",")
        g.jwt_scopes = jwt_scopes
    return gdm_clinician


@pytest.fixture
def mock_bearer_validation(mocker: MockFixture) -> Mock:
    from jose import jwt

    mocked = mocker.patch.object(jwt, "get_unverified_claims")
    mocked.return_value = {
        "sub": "1234567890",
        "name": "John Doe",
        "iat": 1_516_239_022,
        "iss": "http://localhost/",
    }
    return mocked


@pytest.fixture
def question_types() -> List[QuestionType]:
    question_types = []
    for qt in QUESTION_TYPE_DATA:
        insert = QuestionType(uuid=qt["uuid"], value=qt["value"])
        db.session.add(insert)
        question_types.append(insert)
    db.session.commit()

    return question_types


@pytest.fixture
def question_option_types() -> List[QuestionOptionType]:
    question_option_types = []
    for qot in QUESTION_OPTION_TYPE_DATA:
        insert = QuestionOptionType(uuid=qot["uuid"], value=qot["value"])
        db.session.add(insert)
        question_option_types.append(insert)
    db.session.commit()

    return question_option_types


@pytest.fixture
def question_groups() -> List[Group]:
    question_groups = []
    for group in QUESTION_GROUP_DATA:
        insert = Group(uuid=group["uuid"], group=group["group"])
        db.session.add(insert)
        question_groups.append(insert)
    db.session.commit()

    return question_groups


@pytest.fixture
def question_good(question_types: List[QuestionType]) -> Dict:
    question = {
        "question": "Hello, is it me you are looking for?",
        "question_type": dict(value=0),
        "groups": [dict(group="feedback1")],
    }
    return question_controller.create_question(question)


@pytest.fixture
def survey(question_groups: List[Group]) -> Dict:
    survey_details: Dict = {
        "user_id": "663a5c11-fa30-4dd4-ba17-def0ce58e383",
        "group": "feedback1",
        "user_type": "patient",
    }
    return survey_controller.create_survey(survey_details)


@pytest.fixture
def answer_good(question_good: Dict, survey: Dict) -> Dict:
    answer = {
        "question_id": question_good["uuid"],
        "survey_id": survey["uuid"],
        "value": "I am an answer",
    }
    return answer_controller.create_answers([answer])[0]


@pytest.fixture
def question_in_survey(
    question_types: List[QuestionType], question_groups: List[Group], survey: Dict
) -> Tuple[Dict, Dict]:
    question: Dict = question_controller.create_question(
        {
            "question": "Hello, is it me you are looking for?",
            "question_type": {"value": 0},
            "groups": [{"group": "feedback1"}],
        }
    )

    return question, survey


QUESTION_TYPE_DATA = [
    {"uuid": "free_text", "value": "0"},
    {"uuid": "integer", "value": "1"},
    {"uuid": "checkbox", "value": "2"},
    {"uuid": "radio", "value": "3"},
    {"uuid": "drop_down", "value": "4"},
    {"uuid": "range", "value": "5"},
    {"uuid": "multi_select", "value": "6"},
]

QUESTION_OPTION_TYPE_DATA = [
    {"uuid": "fixed", "value": "0"},
    {"uuid": "free_text", "value": "1"},
    {"uuid": "range_start", "value": "2"},
    {"uuid": "range_end", "value": "3"},
    {"uuid": "interval", "value": "4"},
]

QUESTION_GROUP_DATA = [
    {"uuid": "feedback1", "group": "feedback1"},
]

QUESTIONS = [
    "I am satisfied with my current treatment.",
    "I am satisfied that the treatment I am receiveing is the best for me.",
    "I am satisfied with my understanding of diabetes.",
    "I feel my maternity diabetes team knows enough about my current level of diabetes control.",
    "I feel I have a good relationship with my maternity diabetes team.",
    "I am satisfied with my maternity diabetes team's understanding of my diabetes.",
    "I find the equipment I use to check my blood sugars is convenient.",
    "I feel the equipment I use to check my blood sugars is reliable.",
    "My blood sugar monitoring fits with my lifestyle.",
    "I enjoy using this app.",
]

FEEDBACK_QUESTION_OPTIONS = {
    "question_type": {"value": 5},
    "groups": [{"group": "patient_satisfaction_survey"}],
    "question_options": [
        {"text": "Strongly Disagree", "value": "1", "question_option_type": 2},
        {"text": "Strongly Agree", "value": "5", "question_option_type": 3},
        {"value": "1", "question_option_type": 4},
    ],
}

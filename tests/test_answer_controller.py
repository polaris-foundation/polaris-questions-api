from datetime import datetime, timedelta
from typing import Dict

import pytest
from flask.testing import FlaskClient

from dhos_questions_api.controllers import question_controller


@pytest.mark.usefixtures(
    "mock_bearer_validation",
    "jwt_gdm_clinician_uuid",
    "question_types",
    "question_option_types",
)
class TestAnswerController:
    def test_create_answer(
        self, client: FlaskClient, question_good: Dict, survey: Dict
    ) -> None:
        expected_answer = "238476"
        answer = [
            {
                "question_id": question_good["uuid"],
                "survey_id": survey["uuid"],
                "value": expected_answer,
            }
        ]
        response = client.post(
            "/dhos/v1/answer", json=answer, headers={"Authorization": "Bearer TOKEN"}
        )
        assert response.status_code == 200
        assert response.json is not None
        assert response.json[0]["value"] == expected_answer

    def test_create_answer_by_survey_id(
        self, client: FlaskClient, question_good: Dict, survey: Dict
    ) -> None:
        expected_answer = "238476"
        answer = [
            {
                "question_id": question_good["uuid"],
                "value": expected_answer,
            }
        ]
        response = client.post(
            f"/dhos/v1/survey/{survey['uuid']}/answer",
            json=answer,
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert response.status_code == 200
        assert response.json is not None
        assert response.json[0]["value"] == expected_answer

    def test_get_answers(self, client: FlaskClient, answer_good: Dict) -> None:
        response = client.get(
            "/dhos/v1/answer", headers={"Authorization": "Bearer TOKEN"}
        )
        assert response.status_code == 200
        assert response.json is not None
        assert len(response.json) == 1
        assert response.json[0]["uuid"] == answer_good["uuid"]

    def test_get_answers_by_date(self, client: FlaskClient, answer_good: Dict) -> None:
        start_date = (datetime.utcnow() - timedelta(days=1)).isoformat(
            timespec="milliseconds"
        )
        end_date = (datetime.utcnow() + timedelta(days=1)).isoformat(
            timespec="milliseconds"
        )
        response = client.get(
            f"/dhos/v1/answer?start_date={start_date}&end_date={end_date}",
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert response.status_code == 200
        assert response.json is not None
        assert len(response.json) == 1
        assert response.json[0]["uuid"] == answer_good["uuid"]

        response = client.get(
            f"/dhos/v1/answer?start_date={end_date}",
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert response.status_code == 200
        assert response.json == []

    def test_get_answers_by_survey_id(
        self, client: FlaskClient, survey: Dict, answer_good: Dict
    ) -> None:
        response = client.get(
            f"/dhos/v1/survey/{survey['uuid']}/answer",
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert response.status_code == 200
        assert response.json is not None
        assert response.json[0]["uuid"] == answer_good["uuid"]

    def test_get_answers_by_id(self, client: FlaskClient, answer_good: Dict) -> None:
        response = client.get(
            f"/dhos/v1/answer/{answer_good['uuid']}",
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert response.status_code == 200
        assert response.json is not None
        assert response.json["uuid"] == answer_good["uuid"]

    def test_update_answer(self, client: FlaskClient, answer_good: Dict) -> None:
        update_answer = {"value": "Actually changed my mind, you're ok"}
        response = client.patch(
            f"/dhos/v1/answer/{answer_good['uuid']}",
            json=update_answer,
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert response.status_code == 200
        assert response.json is not None
        assert response.json["value"] == update_answer["value"]

    def test_update_answer_non_updatable_field(
        self, client: FlaskClient, answer_good: Dict
    ) -> None:
        update_answer = {"question_id": "1234", "value": "hello"}
        response = client.patch(
            f"/dhos/v1/answer/{answer_good['uuid']}",
            json=update_answer,
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert response.status_code == 400

    def test_update_answer_empty_answer(
        self, client: FlaskClient, answer_good: Dict
    ) -> None:
        update_answer = {"value": ""}
        response = client.patch(
            f"/dhos/v1/answer/{answer_good['uuid']}",
            json=update_answer,
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert response.status_code == 400

    def test_create_answer_bad_survey_id(
        self, client: FlaskClient, question_good: Dict
    ) -> None:
        answer = [
            {
                "question_id": question_good["uuid"],
                "survey_id": "unknown",
                "value": "some answer",
            }
        ]
        response = client.post(
            "/dhos/v1/answer", json=answer, headers={"Authorization": "Bearer TOKEN"}
        )
        assert response.status_code == 400

    def test_create_answer_bad_question_id(
        self, client: FlaskClient, survey: Dict
    ) -> None:
        answer = [
            {
                "question_id": "unknown",
                "survey_id": survey["uuid"],
                "value": "some answer",
            }
        ]
        response = client.post(
            "/dhos/v1/answer", json=answer, headers={"Authorization": "Bearer TOKEN"}
        )
        assert response.status_code == 400

    def test_get_answers_by_survey_id_and_question_id(
        self, client: FlaskClient, survey: Dict, question_good: Dict, answer_good: Dict
    ) -> None:
        response = client.get(
            f"/dhos/v1/survey/{survey['uuid']}/question/{question_good['uuid']}/answer",
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert response.status_code == 200
        assert response.json is not None
        assert len(response.json) == 1
        assert response.json[0]["uuid"] == answer_good["uuid"]

    def test_create_int_answer(self, client: FlaskClient, survey: Dict) -> None:
        int_question = question_controller.create_question(
            question_details={
                "question": "Hello, is it me you are looking for?",
                "question_type": {"value": 1},
                "groups": [{"group": "feedback1"}],
            }
        )
        answer = [
            {
                "question_id": int_question["uuid"],
                "survey_id": survey["uuid"],
                "value": "56",
            }
        ]
        response = client.post(
            "/dhos/v1/answer", json=answer, headers={"Authorization": "Bearer TOKEN"}
        )
        assert response.status_code == 200

    def test_create_bad_int_answer(self, client: FlaskClient, survey: Dict) -> None:
        int_question = question_controller.create_question(
            question_details={
                "question": "Hello, is it me you are looking for?",
                "question_type": {"value": 1},
                "groups": [{"group": "feedback1"}],
            }
        )
        answer = [
            {
                "question_id": int_question["uuid"],
                "survey_id": survey["uuid"],
                "value": "no",
            }
        ]
        response = client.post(
            "/dhos/v1/answer", json=answer, headers={"Authorization": "Bearer TOKEN"}
        )
        assert response.status_code == 400

    def test_create_duplicate_answer(
        self, client: FlaskClient, answer_good: Dict
    ) -> None:
        response = client.post(
            "/dhos/v1/answer",
            json=answer_good,
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert response.status_code == 400

    def test_create_multi_answer_checkbox(
        self, client: FlaskClient, survey: Dict
    ) -> None:
        multi_question = question_controller.create_question(
            {
                "question": "How many would you like?",
                "question_type": {"value": 2},
                "question_options": [
                    {"text": "1", "value": "1", "question_option_type": 0},
                    {
                        "text": "1 million",
                        "value": "1000000",
                        "question_option_type": 0,
                    },
                ],
                "groups": [{"group": "feedback1"}],
            }
        )
        answers = [
            {
                "question_id": multi_question["uuid"],
                "survey_id": survey["uuid"],
                "value": "1000000",
            },
            {
                "question_id": multi_question["uuid"],
                "survey_id": survey["uuid"],
                "value": "1",
            },
        ]
        response = client.post(
            "/dhos/v1/answer", json=answers, headers={"Authorization": "Bearer TOKEN"}
        )
        assert response.status_code == 200

    def test_create_multi_answer_checkbox_bad(
        self, client: FlaskClient, survey: Dict
    ) -> None:
        multi_question = question_controller.create_question(
            {
                "question": "How many would you like?",
                "question_type": {"value": 2},
                "question_options": [
                    {"text": "1", "value": "1", "question_option_type": 0},
                    {
                        "text": "1 million",
                        "value": "1000000",
                        "question_option_type": 0,
                    },
                ],
                "groups": [{"group": "feedback1"}],
            }
        )
        answers = [
            {
                "question_id": multi_question["uuid"],
                "survey_id": survey["uuid"],
                "value": "1",
            },
            {
                "question_id": multi_question["uuid"],
                "survey_id": survey["uuid"],
                "value": "2",
            },
        ]
        response = client.post(
            "/dhos/v1/answer", json=answers, headers={"Authorization": "Bearer TOKEN"}
        )
        assert response.status_code == 400

    def test_create_multi_answer_radio_bad(
        self, client: FlaskClient, survey: Dict
    ) -> None:
        multi_question = question_controller.create_question(
            {
                "question": "How many would you like?",
                "question_type": {"value": 3},
                "question_options": [
                    {"text": "1", "value": "1", "question_option_type": 0},
                    {
                        "text": "1 million",
                        "value": "1000000",
                        "question_option_type": 0,
                    },
                ],
                "groups": [{"group": "feedback1"}],
            }
        )
        answers = [
            {
                "question_id": multi_question["uuid"],
                "survey_id": survey["uuid"],
                "value": "1000000",
            },
            {
                "question_id": multi_question["uuid"],
                "survey_id": survey["uuid"],
                "value": "1",
            },
        ]
        response = client.post(
            "/dhos/v1/answer", json=answers, headers={"Authorization": "Bearer TOKEN"}
        )
        assert response.status_code == 400

    def test_create_range_answer(self, client: FlaskClient, survey: Dict) -> None:
        range_question = question_controller.create_question(
            {
                "question": "How many would you like?",
                "question_type": {"value": 5},
                "question_options": [
                    {"text": "1", "value": "1", "question_option_type": 2},
                    {
                        "text": "1 million",
                        "value": "1000000",
                        "question_option_type": 3,
                    },
                    {"text": "1", "value": "1", "question_option_type": 4},
                ],
                "groups": [{"group": "feedback1"}],
            }
        )
        answers = [
            {
                "question_id": range_question["uuid"],
                "survey_id": survey["uuid"],
                "value": "5",
            }
        ]
        response = client.post(
            "/dhos/v1/answer", json=answers, headers={"Authorization": "Bearer TOKEN"}
        )
        assert response.status_code == 200

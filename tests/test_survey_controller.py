from datetime import date, datetime, timedelta
from typing import Any, Dict, List

import pytest
from flask.testing import FlaskClient

from dhos_questions_api.controllers import answer_controller
from dhos_questions_api.models.group import Group


@pytest.mark.usefixtures("mock_bearer_validation")
class TestSurveyController:
    def test_create_survey(
        self,
        client: FlaskClient,
        question_groups: List[Group],
        jwt_system: str,
    ) -> None:
        survey = {
            "user_id": "0e9971fe-1a93-480a-b2cd-4091d5ebb0f9",
            "group": "feedback1",
            "user_type": "patient",
        }
        response = client.post(
            "/dhos/v1/survey",
            json=survey,
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert response.status_code == 200

    def test_create_survey_bad_group(
        self,
        client: FlaskClient,
        jwt_system: str,
    ) -> None:
        """
        Tests that creating a new survey with a non-existent group results in a 400
        """
        survey = dict(
            user_id="0e9971fe-1a93-480a-b2cd-4091d5ebb0f9",
            group="wont-exist-yet",
            user_type="patient",
        )
        response = client.post(
            "/dhos/v1/survey",
            json=survey,
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert response.status_code == 400

    def test_get_all_surveys(
        self,
        client: FlaskClient,
        survey: Dict,
        jwt_system: str,
        mock_bearer_validation: Any,
    ) -> None:
        response = client.get(
            "/dhos/v1/survey",
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert response.status_code == 200
        assert response.json is not None
        assert response.json[0]["uuid"] == survey["uuid"]

    def test_get_survey_by_uuid(
        self,
        client: FlaskClient,
        survey: Dict,
        jwt_system: str,
    ) -> None:
        response = client.get(
            f"/dhos/v1/survey/{survey['uuid']}",
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert response.status_code == 200
        assert response.json is not None
        assert response.json["user_id"] == survey["user_id"]

    def test_update_survey(
        self, client: FlaskClient, question_good: Dict, jwt_system: str, survey: Dict
    ) -> None:
        update = {"completed": "2018-03-15T10:11:52.683Z"}
        response = client.patch(
            f"/dhos/v1/survey/{survey['uuid']}",
            json=update,
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert response.status_code == 200

    def test_bad_update_survey(
        self, client: FlaskClient, question_good: Dict, jwt_system: str, survey: Dict
    ) -> None:
        update = {"completed": "2018-03-15T10:11:52.683Z", "uuid": "1234"}
        response = client.patch(
            f"/dhos/v1/survey/{survey['uuid']}",
            json=update,
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert response.status_code == 400

    def test_get_surveys_by_date(
        self, client: FlaskClient, question_good: Dict, jwt_system: str, survey: Dict
    ) -> None:
        start_date = (datetime.utcnow() - timedelta(days=1)).isoformat(
            timespec="milliseconds"
        )
        end_date = (datetime.utcnow() + timedelta(days=1)).isoformat(
            timespec="milliseconds"
        )
        response = client.get(
            f"/dhos/v1/survey?start_date={start_date}&end_date={end_date}",
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert response.status_code == 200
        assert response.json is not None
        assert len(response.json) == 1
        assert response.json[0]["uuid"] == survey["uuid"]

        response = client.get(
            f"/dhos/v1/survey?start_date={end_date}",
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert response.status_code == 200
        assert response.json == []

    def test_get_survey_responses(
        self,
        client: FlaskClient,
        question_good: Dict,
        jwt_system: str,
        survey: Dict,
    ) -> None:
        expected_answer = "234578923987456"
        answer_controller.create_answers(
            answers=[
                {
                    "question_id": question_good["uuid"],
                    "survey_id": survey["uuid"],
                    "value": expected_answer,
                }
            ]
        )
        response = client.get(
            "/dhos/v1/survey_responses", headers={"Authorization": "Bearer TOKEN"}
        )
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "text/csv; charset=utf-8"
        assert isinstance(response.data.decode("utf8"), str)
        assert expected_answer in response.data.decode("utf8")

    @pytest.mark.parametrize(
        "start_delta,end_delta,expected",
        [
            (0, 0, True),
            (0, 1, True),
            (-1, 0, True),
            (-2, -1, False),
            (1, 2, False),
        ],
    )
    def test_get_survey_responses_filtered(
        self,
        client: FlaskClient,
        question_good: Dict,
        jwt_system: str,
        survey: Dict,
        start_delta: int,
        end_delta: int,
        expected: bool,
    ) -> None:
        date_today: date = date.today()
        expected_answer = "234578923987456"
        answer_controller.create_answers(
            answers=[
                {
                    "question_id": question_good["uuid"],
                    "survey_id": survey["uuid"],
                    "value": expected_answer,
                }
            ]
        )
        start_date = date_today + timedelta(days=start_delta)
        end_date = date_today + timedelta(days=end_delta)
        response = client.get(
            f"/dhos/v1/survey_responses?start_date={str(start_date)}&end_date={str(end_date)}",
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "text/csv; charset=utf-8"
        assert isinstance(response.data.decode("utf8"), str)
        assert (expected_answer in response.data.decode("utf8")) == expected

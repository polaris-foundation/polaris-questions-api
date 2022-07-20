from typing import Any, Dict, List, Tuple

from flask.testing import FlaskClient

from dhos_questions_api.models.group import Group
from dhos_questions_api.models.question import Question
from dhos_questions_api.models.question_option_type import QuestionOptionType
from dhos_questions_api.models.question_type import QuestionType


class TestQuestionRoutes:
    def test_get_question_by_uuid(
        self,
        client: FlaskClient,
        question_good: Dict,
        jwt_system: str,
        mock_bearer_validation: Any,
    ) -> None:
        """
        Test case for get_question_by_uuid

        Get question by id
        """
        response = client.get(
            f"/dhos/v1/question/{question_good['uuid']}",
            headers={"Authorization": "Bearer TOKEN"},
        )

        assert response.status_code == 200

    def test_get_questions_by_survey_uuid(
        self,
        client: FlaskClient,
        question_in_survey: Tuple[Dict, Dict],
        jwt_system: str,
        mock_bearer_validation: Any,
    ) -> None:
        """
        Test case for get_questions_by_survey_uuid

        Get all questions for a survey
        """
        question, survey = question_in_survey
        response = client.get(
            f"/dhos/v1/survey/{survey['uuid']}/question",
            headers={"Authorization": "Bearer TOKEN"},
        )

        assert response.status_code == 200
        assert response.json is not None
        assert response.json[0]["question"] == question["question"]

    def test_get_questions_by_question_group_uuid(
        self,
        client: FlaskClient,
        question_good: Question,
        jwt_system: str,
        mock_bearer_validation: Any,
    ) -> None:
        response = client.get(
            f"/dhos/v1/group/{question_good['groups'][0]['uuid']}/question",
            headers={"Authorization": "Bearer TOKEN"},
        )

        assert response.status_code == 200
        assert response.json is not None
        assert response.json[0]["question"] == question_good["question"]

    def test_post_question_type(
        self, client: FlaskClient, jwt_system: str, mock_bearer_validation: Any
    ) -> None:
        question_type = {"uuid": "sometestuuid", "value": 678}
        response = client.post(
            "/dhos/v1/question_type",
            json=question_type,
            headers={"Authorization": "Bearer TOKEN"},
        )

        assert response.status_code == 200
        assert response.json is not None
        assert response.json["value"] == question_type["value"]

    def test_post_question_option_type(
        self, client: FlaskClient, jwt_system: str, mock_bearer_validation: Any
    ) -> None:
        question_option_type = {"uuid": "anothertestuuid", "value": 567}
        response = client.post(
            "/dhos/v1/question_option_type",
            json=question_option_type,
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert response.status_code == 200
        assert response.json is not None
        assert response.json["value"] == question_option_type["value"]

    def test_post_question_with_options(
        self,
        client: FlaskClient,
        question_types: List[QuestionType],
        question_option_types: List[QuestionOptionType],
        jwt_system: str,
        mock_bearer_validation: Any,
    ) -> None:
        question: Dict = dict(
            question="Hello, is it me you are looking for?",
            question_type=dict(value=3),
            groups=[dict(group="feedback1")],
            question_options=[
                dict(text="Yes", value="0", order=1, question_option_type=0),
                dict(text="No", value="1", order=2, question_option_type=0),
                dict(text="Maybe", value="2", order=3, question_option_type=0),
            ],
        )

        response = client.post(
            "/dhos/v1/question",
            json=question,
            headers={"Authorization": "Bearer TOKEN"},
        )

        assert response.status_code == 200
        assert response.json is not None
        assert response.json["question"] == question["question"]
        assert (
            response.json["question_type"]["value"]
            == question["question_type"]["value"]
        )
        assert response.json["groups"][0]["group"] == question["groups"][0]["group"]
        assert (
            response.json["question_options"][0]["text"]
            == question["question_options"][0]["text"]
        )

    def test_post_question_with_bad_option_type(
        self,
        client: FlaskClient,
        question_types: List[QuestionType],
        question_option_types: List[QuestionOptionType],
        jwt_system: str,
        mock_bearer_validation: Any,
    ) -> None:
        question: Dict = dict(
            question="Hello, is it me you are looking for?",
            question_type=dict(value=3),
            groups=[dict(group="feedback1")],
            question_options=[
                dict(text="Yes", value="0", order=1, question_option_type=0),
                dict(text="No", value="1", order=2, question_option_type=99),
                dict(text="Maybe", value="2", order=3, question_option_type=0),
            ],
        )

        response = client.post(
            "/dhos/v1/question",
            json=question,
            headers={"Authorization": "Bearer TOKEN"},
        )

        assert response.status_code == 400

    def test_post_question_with_bad_question_type(
        self,
        client: FlaskClient,
        question_types: List[QuestionType],
        question_option_types: List[QuestionOptionType],
        jwt_system: str,
        mock_bearer_validation: Any,
    ) -> None:
        question = dict(
            question="Hello, is it me you are looking for?",
            question_type=dict(value=99),
            groups=[dict(group="feedback1")],
            question_options=[
                dict(text="Yes", value="0", order=1, question_option_type=0),
                dict(text="No", value="1", order=2, question_option_type=0),
                dict(text="Maybe", value="2", order=3, question_option_type=0),
            ],
        )

        response = client.post(
            "/dhos/v1/question",
            json=question,
            headers={"Authorization": "Bearer TOKEN"},
        )

        assert response.status_code == 400

    def test_post_question_with_missing_option_type(
        self,
        client: FlaskClient,
        question_types: List[QuestionType],
        question_option_types: List[QuestionOptionType],
        mock_bearer_validation: Any,
    ) -> None:
        question = dict(
            question="Hello, is it me you are looking for?",
            question_type=dict(value=3),
            groups=[dict(group="feedback1")],
            question_options=[
                dict(text="Yes", value="0", order=1, question_option_type=0),
                dict(text="No", value="1", order=2),
                dict(text="Maybe", value="2", order=3, question_option_type=0),
            ],
        )

        response = client.post(
            "/dhos/v1/question",
            json=question,
            headers={"Authorization": "Bearer TOKEN"},
        )

        assert response.status_code == 400

    def test_post_question_with_existing_group(
        self,
        client: FlaskClient,
        question_types: List[QuestionType],
        question_option_types: List[QuestionOptionType],
        question_groups: List[Group],
        jwt_system: str,
        mock_bearer_validation: Any,
    ) -> None:
        question = dict(
            question="What is up with that?",
            question_type=dict(value=3),
            groups=[dict(group="feedback1")],
            question_options=[
                dict(text="Yes", value="0", order=1, question_option_type=0),
                dict(text="No", value="1", order=2, question_option_type=0),
                dict(text="Maybe", value="2", order=3, question_option_type=0),
            ],
        )

        response = client.post(
            "/dhos/v1/question",
            json=question,
            headers={"Authorization": "Bearer TOKEN"},
        )

        assert response.status_code == 200

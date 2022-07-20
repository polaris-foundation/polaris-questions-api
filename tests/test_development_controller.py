import pytest
from flask.testing import FlaskClient


@pytest.mark.usefixtures("mock_bearer_validation", "jwt_system")
class TestDevelopmentController:
    def test_get_questions(self, client: FlaskClient) -> None:

        response = client.get("/question", headers={"Authorization": "Bearer TOKEN"})
        assert response.status_code == 200

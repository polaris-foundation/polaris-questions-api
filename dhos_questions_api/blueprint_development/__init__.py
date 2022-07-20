import time

from flask import Blueprint, Response, current_app, jsonify
from flask_batteries_included.helpers.security import protected_route
from flask_batteries_included.helpers.security.endpoint_security import (
    and_,
    key_present,
    non_production_only_route,
    scopes_present,
)

from dhos_questions_api.blueprint_development import controller

development = Blueprint("dev", __name__, template_folder="templates")


@development.route("/drop_data", methods=["POST"])
@protected_route(key_present("system_id"))
def drop_data_route() -> Response:
    if current_app.config["ALLOW_DROP_DATA"] is not True:
        raise PermissionError("Cannot drop data in this environment")

    start: float = time.time()
    controller.reset_database()
    total_time: float = time.time() - start
    return jsonify({"complete": True, "time_taken": str(total_time) + "s"})


@development.route("/question", methods=["GET"])
@protected_route(
    and_(
        non_production_only_route(), scopes_present(required_scopes="read:gdm_question")
    )
)
def get_all_questions() -> Response:
    """
    ---
    get:
      summary: Get all questions
      description: Get a list of all questions
      tags: [question]
      responses:
        '200':
          description: A list of all questions
          content:
            application/json:
              schema:
                type: array
                items: QuestionResponse
        default:
          description: >-
              Error, e.g. 400 Bad Request, 404 Not Found, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """
    return jsonify(controller.get_questions())

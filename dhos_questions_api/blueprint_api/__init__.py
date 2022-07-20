from typing import Dict, Generator, List, Optional

import connexion
import flask
from flask import Response, jsonify
from flask_batteries_included.helpers.security import protected_route
from flask_batteries_included.helpers.security.endpoint_security import (
    and_,
    or_,
    scopes_present,
)

from dhos_questions_api.controllers import (
    answer_controller,
    question_controller,
    survey_controller,
)
from dhos_questions_api.helper.security import survey_by_uuid_protection

api_blueprint = flask.Blueprint("questions", __name__)


@api_blueprint.route("/question_type", methods=["POST"])
@protected_route(scopes_present(required_scopes="write:gdm_question"))
def create_question_type() -> Response:
    """
    ---
    post:
      summary: Create question type
      description: Create a new question type using the details provided in the request body.
      tags: [question]
      requestBody:
        description: Question type details
        required: true
        content:
          application/json:
            schema: QuestionTypeRequest
      responses:
        '200':
          description: The new question type
          content:
            application/json:
              schema: QuestionTypeResponse
        default:
          description: >-
            Error, e.g. 400 Bad Request, 404 Not Found, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """
    question_type_details: Dict = connexion.request.get_json()

    return jsonify(question_controller.create_question_type(question_type_details))


@api_blueprint.route("/question_option_type", methods=["POST"])
@protected_route(scopes_present(required_scopes="write:gdm_question"))
def create_question_option_type() -> Response:
    """
    ---
    post:
      summary: Create question option type
      description: Create a new question option type using the details provided in the request body.
      tags: [question]
      requestBody:
        description: Question option type details
        required: true
        content:
          application/json:
            schema: QuestionOptionTypeRequest
      responses:
        '200':
          description: The new question option type
          content:
            application/json:
              schema: QuestionOptionTypeResponse
        default:
          description: >-
            Error, e.g. 400 Bad Request, 404 Not Found, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """
    question_option_type_details: Dict = connexion.request.get_json()

    return jsonify(
        question_controller.create_question_option_type(question_option_type_details)
    )


@api_blueprint.route("/question", methods=["POST"])
@protected_route(scopes_present(required_scopes="write:gdm_question"))
def create_question() -> Response:
    """
    ---
    post:
      summary: Create question
      description: Create a new question using the details provided in the request body.
      tags: [question]
      requestBody:
        description: Question details
        required: true
        content:
          application/json:
            schema: QuestionRequest
      responses:
        '200':
          description: The new question
          content:
            application/json:
              schema: QuestionResponse
        default:
          description: >-
            Error, e.g. 400 Bad Request, 404 Not Found, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """
    question_details: Dict = connexion.request.get_json()

    return jsonify(question_controller.create_question(question_details))


@api_blueprint.route("/survey", methods=["POST"])
@protected_route(scopes_present(required_scopes="write:gdm_survey"))
def create_survey() -> Response:
    """
    ---
    post:
      summary: Create survey
      description: Create a new survey using the details provided in the request body.
      tags: [survey]
      requestBody:
        description: Survey details
        required: true
        content:
          application/json:
            schema: SurveyRequest
      responses:
        '200':
          description: The new survey
          content:
            application/json:
              schema: SurveyResponse
        default:
          description: >-
            Error, e.g. 400 Bad Request, 404 Not Found, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """
    survey_details: Dict = connexion.request.get_json()

    return jsonify(survey_controller.create_survey(survey_details))


@api_blueprint.route("/answer", methods=["POST"])
@protected_route(
    or_(
        scopes_present(required_scopes="write:gdm_answer_all"),
        and_(
            scopes_present(required_scopes="write:gdm_answer"),
            survey_by_uuid_protection,
        ),
    )
)
def create_answers() -> Response:
    """
    ---
    post:
      summary: Create answers
      description: Create a new answers using the array of objects provided in the request body.
      tags: [answer]
      requestBody:
        description: Array of answers
        required: true
        content:
          application/json:
            schema:
              type: array
              items: AnswerRequest
      responses:
        200:
          description: Created answers
          content:
            application/json:
              schema:
                type: array
                items: AnswerResponse
        default:
          description: >-
            Error, e.g. 400 Bad Request, 404 Not Found, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """
    answers: List[Dict] = connexion.request.get_json()
    return jsonify(answer_controller.create_answers(answers))


@api_blueprint.route("/survey/<survey_uuid>/answer", methods=["POST"])
@protected_route(
    or_(
        scopes_present(required_scopes="write:gdm_answer_all"),
        and_(
            scopes_present(required_scopes="write:gdm_answer"),
            survey_by_uuid_protection,
        ),
    )
)
def create_answers_for_survey(survey_uuid: str) -> Response:
    """
    ---
    post:
      summary: Create answers for a survey
      description: Create new answers for a particular survey using the array of objects provided in the request body.
      tags: [answer]
      parameters:
        - name: survey_uuid
          in: path
          required: true
          description: Survey UUID
          schema:
            type: string
            example: '18439f36-ffa9-42ae-90de-0beda299cd37'
      requestBody:
        description: Array of answers
        required: true
        content:
          application/json:
            schema:
              type: array
              items: SurveyAnswerRequest
      responses:
        200:
          description: Created answers
          content:
            application/json:
              schema:
                type: array
                items: AnswerResponse
        default:
          description: >-
            Error, e.g. 400 Bad Request, 404 Not Found, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """
    answers = connexion.request.get_json()
    return jsonify(answer_controller.create_answers_for_survey(survey_uuid, answers))


@api_blueprint.route("/question/<question_uuid>", methods=["GET"])
@protected_route(scopes_present(required_scopes="read:gdm_question"))
def get_question_by_uuid(question_uuid: str) -> Response:
    """
    ---
    get:
      summary: Get question by UUID
      description: Get the question that matches the UUID provided in the URL path.
      tags: [question]
      parameters:
        - name: question_uuid
          in: path
          required: true
          description: The question UUID
          schema:
            type: string
            example: '18439f36-ffa9-42ae-90de-0beda299cd37'
      responses:
        '200':
          description: The question with the specified UUID
          content:
            application/json:
              schema: QuestionResponse
        default:
          description: >-
            Error, e.g. 400 Bad Request, 404 Not Found, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """
    return jsonify(question_controller.get_question_by_uuid(question_uuid))


@api_blueprint.route("/survey/<survey_uuid>/question", methods=["GET"])
@protected_route(scopes_present(required_scopes="read:gdm_question"))
def get_questions_by_survey_uuid(survey_uuid: str) -> Response:
    """
    ---
    get:
      summary: Get questions by survey UUID
      description: >-
        Get a list of all the questions belonging to the survey that matches the UUID provided in
        the URL path.
      tags: [question]
      parameters:
        - name: survey_uuid
          in: path
          required: true
          description: The survey UUID
          schema:
            type: string
            example: '18439f36-ffa9-42ae-90de-0beda299cd37'
      responses:
        '200':
          description: A list of the questions belonging to the survey with the specified UUID.
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
    return jsonify(question_controller.get_questions_by_survey_uuid(survey_uuid))


@api_blueprint.route("/group/<group_uuid>/question", methods=["GET"])
@protected_route(scopes_present(required_scopes="read:gdm_question"))
def get_questions_by_group_uuid(group_uuid: str) -> Response:
    """
    ---
    get:
      summary: Get questions by group UUID
      description: >-
        Get a list of all the questions belonging to the group that matches the UUID provided in
        the URL path.
      tags: [question]
      parameters:
        - name: group_uuid
          in: path
          required: true
          description: The group UUID
          schema:
            type: string
            example: '18439f36-ffa9-42ae-90de-0beda299cd37'
      responses:
        '200':
          description: A list of the questions belonging to the group with the specified UUID.
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
    return jsonify(question_controller.get_questions_by_question_group_uuid(group_uuid))


@api_blueprint.route("/survey", methods=["GET"])
@protected_route(scopes_present(required_scopes="read:gdm_survey_all"))
def get_all_surveys() -> Response:
    """
    ---
    get:
      summary: Get all surveys
      description: Get a list of all surveys.
      tags: [survey]
      responses:
        '200':
          description: An array of surveys
          content:
            application/json:
              schema:
                type: array
                items: SurveyResponse
        default:
          description: >-
            Error, e.g. 400 Bad Request, 404 Not Found, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """
    return jsonify(survey_controller.get_surveys())


@api_blueprint.route("/survey/<survey_uuid>", methods=["GET"])
@protected_route(
    or_(
        scopes_present(required_scopes="read:gdm_survey_all"),
        and_(
            scopes_present(required_scopes="read:gdm_survey"), survey_by_uuid_protection
        ),
    )
)
def get_survey_by_uuid(survey_uuid: str) -> Response:
    """
    ---
    get:
      summary: Get survey by UUID
      description: Get the survey that matches the UUID provided in the URL path.
      tags: [survey]
      parameters:
        - name: survey_uuid
          in: path
          required: true
          description: The survey UUID
          schema:
            type: string
            example: '18439f36-ffa9-42ae-90de-0beda299cd37'
      responses:
        '200':
          description: The survey
          content:
            application/json:
              schema: SurveyResponse
        default:
          description: >-
            Error, e.g. 400 Bad Request, 404 Not Found, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """
    return jsonify(survey_controller.get_survey_by_uuid(survey_uuid))


@api_blueprint.route("/answer", methods=["GET"])
@protected_route(scopes_present(required_scopes="read:gdm_answer_all"))
def get_answers(
    start_date: Optional[str] = None, end_date: Optional[str] = None
) -> Response:
    """
    ---
    get:
      summary: Get all answers
      description: Get all answers for all surveys. Responds with an array of answer objects.
      tags: [answer]
      parameters:
        - name: start_date
          in: query
          required: false
          description: Start date of survey answers
          schema:
            type: string
            example: '2020-03-01'
        - name: end_date
          in: query
          required: false
          description: End date of survey answers
          schema:
            type: string
            example: '2020-04-01'
      responses:
        200:
          description: Array of answers
          content:
            application/json:
              schema:
                type: array
                items: AnswerResponse
        default:
          description: >-
            Error, e.g. 400 Bad Request, 404 Not Found, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """
    return jsonify(answer_controller.get_answers(start_date, end_date))


@api_blueprint.route("/survey/<survey_uuid>/answer", methods=["GET"])
@protected_route(
    or_(
        scopes_present(required_scopes="read:gdm_answer_all"),
        and_(
            scopes_present(required_scopes="read:gdm_answer"), survey_by_uuid_protection
        ),
    )
)
def get_answers_by_survey_uuid(survey_uuid: str) -> Response:
    """
    ---
    get:
      summary: Get answers by survey UUID
      description: Get answers for the survey with the provided UUID. Responds with an array of answers.
      tags: [answer]
      parameters:
        - name: survey_uuid
          in: path
          required: true
          description: Survey UUID
          schema:
            type: string
            example: 'be4db181-076d-40f8-87c4-303761990563'
      responses:
        200:
          description: Array of answers
          content:
            application/json:
              schema:
                type: array
                items: AnswerResponse
        default:
          description: >-
            Error, e.g. 400 Bad Request, 404 Not Found, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """
    return jsonify(answer_controller.get_answers_by_survey_uuid(survey_uuid))


@api_blueprint.route(
    "/survey/<survey_uuid>/question/<question_uuid>/answer", methods=["GET"]
)
@protected_route(
    or_(
        scopes_present(required_scopes="read:gdm_answer_all"),
        and_(
            scopes_present(required_scopes="read:gdm_answer"), survey_by_uuid_protection
        ),
    )
)
def get_answers_by_survey_and_question_uuid(
    survey_uuid: str, question_uuid: str
) -> Response:
    """
    ---
    get:
      summary: Get answers by survey and question UUID
      description: Get answers for the survey and question with the provided UUIDs. Responds with an array of answers.
      tags: [answer]
      parameters:
        - name: survey_uuid
          in: path
          required: true
          description: Survey UUID
          schema:
            type: string
            example: 'be4db181-076d-40f8-87c4-303761990563'
        - name: question_uuid
          in: path
          required: true
          description: Question UUID
          schema:
            type: string
            example: 'e2025736-c93b-42b8-b522-2ee45be89002'
      responses:
        200:
          description: An array of answer
          content:
            application/json:
              schema:
                type: array
                items: AnswerResponse
        default:
          description: >-
            Error, e.g. 400 Bad Request, 404 Not Found, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """
    return jsonify(
        answer_controller.get_answers_by_survey_and_question_uuid(
            survey_uuid, question_uuid
        )
    )


@api_blueprint.route("/answer/<answer_uuid>", methods=["GET"])
@protected_route(
    or_(
        scopes_present(required_scopes="read:gdm_answer_all"),
        and_(
            scopes_present(required_scopes="read:gdm_answer"), survey_by_uuid_protection
        ),
    )
)
def get_answer_by_uuid(answer_uuid: str) -> Response:
    """
    ---
    get:
      summary: Get answer by UUID
      description: Get a particular answer by UUID
      tags: [answer]
      parameters:
        - name: answer_uuid
          in: path
          required: true
          description: Answer UUID
          schema:
            type: string
            example: 'a7b72a66-e0f3-43e5-9bb9-99058b4af114'
      responses:
        200:
          description: The answer
          content:
            application/json:
              schema: AnswerResponse
        default:
          description: >-
            Error, e.g. 400 Bad Request, 404 Not Found, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """
    return jsonify(answer_controller.get_answer_by_uuid(answer_uuid))


@api_blueprint.route("/survey/<survey_uuid>", methods=["PATCH"])
@protected_route(scopes_present(required_scopes="write:gdm_survey"))
def update_survey(survey_uuid: str) -> Response:
    """
    ---
    patch:
      summary: Update survey
      description: Update a survey by UUID with the details provided in the request body
      tags: [survey]
      parameters:
        - name: survey_uuid
          in: path
          required: true
          description: The survey UUID
          schema:
            type: string
            example: '18439f36-ffa9-42ae-90de-0beda299cd37'
      requestBody:
        description: JSON body containing the survey details
        required: true
        content:
          application/json:
            schema: SurveyUpdateRequest
      responses:
        '200':
          description: The survey with the specified UUID
          content:
            application/json:
              schema: SurveyResponse
        default:
          description: >-
            Error, e.g. 400 Bad Request, 404 Not Found, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """
    survey_details: Dict = connexion.request.get_json()
    return jsonify(survey_controller.update_survey(survey_uuid, survey_details))


@api_blueprint.route("/answer/<answer_uuid>", methods=["PATCH"])
@protected_route(
    or_(
        scopes_present(required_scopes="write:gdm_answer_all"),
        and_(
            scopes_present(required_scopes="write:gdm_answer"),
            survey_by_uuid_protection,
        ),
    )
)
def update_answer(answer_uuid: str) -> Response:
    """
    ---
    patch:
      summary: Update answer
      description: Update an answer by UUID using the answer details provided in the request body.
      tags: [answer]
      parameters:
        - name: answer_uuid
          in: path
          required: true
          description: Survey UUID
          schema:
            type: string
            example: 'a7b72a66-e0f3-43e5-9bb9-99058b4af114'
      requestBody:
        content:
          application/json:
            schema: AnswerUpdateRequest
      responses:
        200:
          description: Updated answer
          content:
            application/json:
              schema: AnswerResponse
        default:
          description: >-
            Error, e.g. 400 Bad Request, 404 Not Found, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """
    answer_details: Dict = connexion.request.get_json()
    return jsonify(answer_controller.update_answer(answer_uuid, answer_details))


@api_blueprint.route("/survey_responses", methods=["GET"])
@protected_route(
    and_(
        scopes_present(required_scopes="read:gdm_survey_all"),
        scopes_present(required_scopes="read:gdm_question"),
        scopes_present(required_scopes="read:gdm_answer_all"),
    )
)
def get_survey_responses(
    start_date: Optional[str] = None, end_date: Optional[str] = None
) -> Response:
    """
    ---
    get:
      summary: Get CSV of survey answers
      description: >-
        Generates and returns a CSV of survey questions and answers between two dates. The dates are
        inclusive - if an end_date is specified then any survey answers recorded on that day will be included.
      tags: [survey]
      parameters:
        - name: start_date
          in: query
          required: false
          description: Start date of survey answers
          schema:
            type: string
            format: date
            example: '2020-03-01'
        - name: end_date
          in: query
          required: false
          description: End date of survey answers
          schema:
            type: string
            format: date
            example: '2020-04-01'
      responses:
        '200':
          description: CSV of survey answers
          content:
            text/csv:
              schema:
                type: string
        default:
          description: >-
            Error, e.g. 400 Bad Request, 404 Not Found, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """
    iter_csv: Generator[str, None, None] = survey_controller.get_survey_responses(
        start_date, end_date
    )
    response = Response(iter_csv, mimetype="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=data.csv"
    return response

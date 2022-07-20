from typing import List, Optional, TypedDict

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask_batteries_included.helpers.apispec import (
    FlaskBatteriesPlugin,
    Identifier,
    initialise_apispec,
    openapi_schema,
)
from marshmallow import EXCLUDE, Schema, fields

dhos_questions_api_spec: APISpec = APISpec(
    version="1.0.0",
    openapi_version="3.0.3",
    title="DHOS Questions API",
    info={
        "description": "The DHOS Questions API is responsible for storing and retrieving surveys, and their associated questions and answers."
    },
    plugins=[FlaskPlugin(), MarshmallowPlugin(), FlaskBatteriesPlugin()],
)
initialise_apispec(dhos_questions_api_spec)


class QuestionOptionTypeSchema(Schema):
    class Meta:
        title = "Question option type"
        unknown = EXCLUDE
        ordered = True

        class Dict(TypedDict, total=False):
            value: int

    value = fields.Integer(
        description="Identifier of the question option type",
        example=0,
        required=True,
    )


class QuestionGroupSchema(Schema):
    class Meta:
        title = "Question group"
        unknown = EXCLUDE
        ordered = True

        class Dict(TypedDict, total=False):
            group: str

    group = fields.String(
        description="The question group name",
        example="GDM_FEEDBACK",
        required=True,
    )


class QuestionTypeSchema(Schema):
    class Meta:
        title = "Question type"
        unknown = EXCLUDE
        ordered = True

        class Dict(TypedDict, total=False):
            value: int

    value = fields.Integer(
        description="Identifier of the question type",
        example=0,
        required=True,
    )


class QuestionOptionSchema(Schema):
    class Meta:
        title = "Question option"
        unknown = EXCLUDE
        ordered = True

        class Dict(TypedDict, total=False):
            question_option_type: int
            value: str
            text: Optional[str]
            order: Optional[int]

    question_option_type = fields.Integer(
        description="Identifier of the question option type",
        example=0,
        required=True,
    )
    value = fields.String(
        description="Value related to the option",
        example="1",
        required=True,
    )
    text = fields.String(
        description="Display text related to the option. Commonly used for radio/check options. Can be the same as the value",
        example="one",
        required=False,
        allow_none=True,
    )
    order = fields.Integer(
        description="Sort order for display purposes",
        example=1,
        required=False,
        allow_none=True,
    )


class QuestionSchema(Schema):
    class Meta:
        title = "Question fields common to request and response"
        unknown = EXCLUDE
        ordered = True

        class Dict(TypedDict, total=False):
            question: str
            question_type: QuestionTypeSchema.Meta.Dict
            question_options: List[QuestionOptionSchema.Meta.Dict]
            groups: List[QuestionGroupSchema.Meta.Dict]

    question = fields.String(
        description="The question text",
        example="What is the average airspeed velocity of an unladen swallow?",
        required=True,
    )
    question_type = fields.Nested(QuestionTypeSchema, required=True)
    question_options = fields.List(fields.Nested(QuestionOptionSchema), required=False)
    groups = fields.List(fields.Nested(QuestionGroupSchema), required=False)


@openapi_schema(dhos_questions_api_spec)
class QuestionRequest(QuestionSchema):
    class Meta:
        title = "Question request"
        unknown = EXCLUDE
        ordered = True

        class Dict(TypedDict, QuestionSchema.Meta.Dict, total=False):
            pass


@openapi_schema(dhos_questions_api_spec)
class QuestionResponse(QuestionSchema, Identifier):
    class Meta:
        title = "Question response"
        unknown = EXCLUDE
        ordered = True

        class Dict(TypedDict, QuestionSchema.Meta.Dict, total=False):
            pass


@openapi_schema(dhos_questions_api_spec)
class QuestionTypeRequest(QuestionTypeSchema):
    class Meta:
        title = "Question Type request"
        unknown = EXCLUDE
        ordered = True

        class Dict(TypedDict, QuestionTypeSchema.Meta.Dict, total=False):
            pass


@openapi_schema(dhos_questions_api_spec)
class QuestionTypeResponse(QuestionTypeSchema):
    class Meta:
        title = "Question Type response"
        unknown = EXCLUDE
        ordered = True

        class Dict(TypedDict, QuestionTypeSchema.Meta.Dict, total=False):
            pass


@openapi_schema(dhos_questions_api_spec)
class QuestionOptionTypeRequest(QuestionOptionTypeSchema):
    class Meta:
        title = "Question Option Type request"
        unknown = EXCLUDE
        ordered = True

        class Dict(TypedDict, QuestionOptionTypeSchema.Meta.Dict, total=False):
            pass


@openapi_schema(dhos_questions_api_spec)
class QuestionOptionTypeResponse(QuestionOptionTypeSchema):
    class Meta:
        title = "Question Option Type response"
        unknown = EXCLUDE
        ordered = True

        class Dict(TypedDict, QuestionOptionTypeSchema.Meta.Dict, total=False):
            pass

        deleted = fields.String(
            description="When the question option type was deleted",
            example="2019-01-01T00:00:00.000Z",
            required=False,
        )


class SurveySchema(Schema):
    class Meta:
        title = "Survey fields"
        unknown = EXCLUDE
        ordered = True

        class Dict(TypedDict, total=False):
            user_id: str
            user_type: str

    user_id = fields.String(
        description="The UUID of the entity being asked the questions",
        example="2c4f1d24-2952-4d4e-b1d1-3637e33cc161",
        required=True,
    )

    user_type = fields.String(
        description="The object type of the entity being asked the questions",
        example="2c4f1d24-2952-4d4e-b1d1-3637e33cc161",
        required=True,
    )

    completed = fields.String(
        description="When the survey was completed",
        example="2019-01-01T00:00:00.000Z",
        required=False,
    )
    declined = fields.String(
        description="When the survey was declined",
        example="2019-01-01T00:00:00.000Z",
        required=False,
    )


@openapi_schema(dhos_questions_api_spec)
class SurveyRequest(SurveySchema):
    class Meta:
        title = "Survey request"
        unknown = EXCLUDE
        ordered = True

        class Dict(TypedDict, SurveySchema.Meta.Dict, total=False):
            group: str

    group = fields.String(
        description="The question group",
        example="GDM_FEEDBACK",
        required=True,
    )


@openapi_schema(dhos_questions_api_spec)
class SurveyResponse(SurveySchema, Identifier):
    class Meta:
        title = "Survey response"
        unknown = EXCLUDE
        ordered = True

        class Dict(TypedDict, SurveySchema.Meta.Dict, total=False):
            group: QuestionGroupSchema.Meta.Dict

    group = fields.Nested(QuestionGroupSchema, required=True)

    deleted = fields.String(
        description="When the survey was deleted",
        example="2019-01-01T00:00:00.000Z",
        required=False,
    )


@openapi_schema(dhos_questions_api_spec)
class SurveyUpdateRequest(Schema):
    class Meta:
        title = "Survey update request"
        unknown = EXCLUDE
        ordered = True

        class Dict(TypedDict, total=False):
            completed: str
            declined: str

    completed = fields.String(
        description="When the survey was completed",
        example="2019-01-01T00:00:00.000Z",
        required=False,
    )
    declined = fields.String(
        description="When the survey was declined",
        example="2019-01-01T00:00:00.000Z",
        required=False,
    )


class AnswerSchema(Schema):
    survey_id = fields.String(
        description="The survey UUID",
        example="6971e1ba-4ab2-48a8-8ba5-080b2e4b65fd",
        required=True,
    )
    question_id = fields.String(
        description="The question UUID",
        example="6971e1ba-4ab2-48a8-8ba5-080b2e4b65fd",
        required=True,
    )
    value = fields.String(description="The answer value", example="4", required=True)
    text = fields.String(
        description="Display text related to the option, can be the same as the value",
        example="four",
        required=False,
        allow_none=True,
    )


@openapi_schema(dhos_questions_api_spec)
class AnswerRequest(AnswerSchema):
    class Meta:
        title = "Answer request"
        unknown = EXCLUDE
        ordered = True


@openapi_schema(dhos_questions_api_spec)
class AnswerResponse(AnswerSchema, Identifier):
    class Meta:
        title = "Answer response"
        unknown = EXCLUDE
        ordered = True

    deleted = fields.String(
        description="When the answer was deleted",
        example="2019-01-01T00:00:00.000Z",
        required=False,
    )


@openapi_schema(dhos_questions_api_spec)
class SurveyAnswerRequest(Schema):
    class Meta:
        title = "Survey answer request"
        unknown = EXCLUDE
        ordered = True

    question_id = fields.String(
        description="The question UUID",
        example="6971e1ba-4ab2-48a8-8ba5-080b2e4b65fd",
        required=True,
    )
    value = fields.String(description="The answer value", example="4", required=True)
    text = fields.String(
        description="Display text related to the option, can be the same as the value",
        example="four",
        required=False,
        allow_none=True,
    )


@openapi_schema(dhos_questions_api_spec)
class AnswerUpdateRequest(Schema):
    class Meta:
        title = "Answer update request"
        unknown = EXCLUDE
        ordered = True

    value = fields.String(
        description="The answer value", example="4", required=False, allow_none=True
    )
    text = fields.String(
        description="Display text related to the option, can be the same as the value",
        example="four",
        required=False,
        allow_none=True,
    )

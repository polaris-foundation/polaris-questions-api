from datetime import datetime
from typing import Dict

from flask_batteries_included.sqldb import ModelIdentifier, db

from dhos_questions_api.queries.softdelete import QueryWithSoftDelete


class QuestionOption(ModelIdentifier, db.Model):
    query_class = QueryWithSoftDelete

    text = db.Column(db.String, unique=False, nullable=True)
    value = db.Column(db.String, unique=False, nullable=False)
    order = db.Column(db.Integer, unique=False, nullable=True)

    deleted = db.Column(db.DateTime, unique=False, nullable=True)

    question_id = db.Column(db.String, db.ForeignKey("question.uuid"))

    question_option_type_id = db.Column(
        db.String, db.ForeignKey("question_option_type.uuid")
    )
    question_option_type = db.relationship("QuestionOptionType")

    @staticmethod
    def schema() -> Dict:
        return {
            "optional": {"text": str, "order": int},
            "required": {"question_option_type": str, "value": str},
            "updatable": {
                "text": str,
                "order": int,
                "question_option_type": str,
                "question_type": str,
            },
        }

    def to_dict(self) -> Dict:
        schema = self.schema()
        question_option = {}
        for key in schema["required"]:
            if key == "question_option_type":
                question_option[key] = self.question_option_type.to_dict()
            else:
                question_option[key] = getattr(self, key)

        for key in schema["optional"]:
            value = getattr(self, key)
            if value is not None:
                question_option[key] = value

        if self.deleted is not None:
            question_option["deleted"] = self.deleted

        return {**question_option, **self.pack_identifier()}

    def delete(self) -> None:
        self.deleted = datetime.utcnow()

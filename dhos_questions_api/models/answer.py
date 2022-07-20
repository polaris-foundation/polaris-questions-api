from datetime import datetime
from typing import Any, Dict

from flask_batteries_included.sqldb import ModelIdentifier, db

from dhos_questions_api.queries.softdelete import QueryWithSoftDelete


class Answer(ModelIdentifier, db.Model):
    query_class = QueryWithSoftDelete

    survey_id = db.Column(db.String, unique=False, nullable=False)
    question_id = db.Column(db.String, unique=False, nullable=False)

    value = db.Column(db.String, unique=False, nullable=False)
    text = db.Column(db.String, unique=False, nullable=True)

    __table_args__ = (
        db.Index(
            "only_one_active_identical_question_option",
            survey_id,
            question_id,
            value,
            unique=True,
            postgresql_where=db.text("deleted IS NULL"),
        ),
    )

    deleted = db.Column(db.DateTime, unique=False, nullable=True)

    @staticmethod
    def schema() -> Dict:
        return {
            "optional": {},
            "required": {"survey_id": str, "question_id": str, "value": str},
            "updatable": {"value": str, "text": str},
        }

    def to_dict(self) -> Dict:
        answer = {
            "survey_id": self.survey_id,
            "question_id": self.question_id,
            "value": self.value,
        }
        if self.text is not None:
            answer["text"] = self.text
        if self.deleted is not None:
            answer["deleted"] = self.deleted
        return {**answer, **self.pack_identifier()}

    def delete(self) -> None:
        self.deleted = datetime.utcnow()

    def set_property(self, key: str, value: Any) -> None:
        setattr(self, key, value)

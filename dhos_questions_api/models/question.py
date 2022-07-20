from datetime import datetime
from typing import Dict

from flask_batteries_included.sqldb import ModelIdentifier, db

from dhos_questions_api.queries.softdelete import QueryWithSoftDelete


class Question(ModelIdentifier, db.Model):
    query_class = QueryWithSoftDelete

    # required
    question = db.Column(db.String, unique=False, nullable=False)

    # system
    deleted = db.Column(db.DateTime, unique=False, nullable=True)

    # relationships
    question_type_id = db.Column(db.String, db.ForeignKey("question_type.uuid"))
    question_type = db.relationship("QuestionType")

    question_options = db.relationship("QuestionOption")

    relationship_table = db.Table(
        "question_group",
        db.Column(
            "question_id", db.String, db.ForeignKey("question.uuid"), nullable=False
        ),
        db.Column("group_id", db.String, db.ForeignKey("group.uuid"), nullable=False),
        db.PrimaryKeyConstraint("question_id", "group_id"),
    )

    groups = db.relationship(
        "Group", secondary="question_group", backref="question", lazy=True
    )

    @staticmethod
    def schema() -> Dict:
        return {
            "optional": {"question_options": list, "groups": list},
            "required": {"question": str, "question_type": str},
            "updatable": {
                "question": str,
                "question_options": list,
                "groups": list,
                "question_type": str,
            },
        }

    def to_dict(self) -> Dict:
        schema = self.schema()
        question = {}
        for key in schema["required"]:
            if key == "question_type":
                question[key] = self.question_type.to_dict()
            else:
                question[key] = getattr(self, key)

        for key in schema["optional"]:
            if key == "question_options":
                qo = [qo.to_dict() for qo in self.question_options]
                if len(self.question_options) > 0:
                    question[key] = qo
            elif key == "groups":
                question[key] = [qg.to_dict() for qg in self.groups]

        if self.deleted is not None:
            question["deleted"] = self.deleted

        return {**question, **self.pack_identifier()}

    def delete(self) -> None:
        self.deleted = datetime.utcnow()

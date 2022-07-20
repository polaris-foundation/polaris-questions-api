from datetime import datetime
from typing import Dict

from flask_batteries_included.helpers.timestamp import join_timestamp
from flask_batteries_included.sqldb import ModelIdentifier, db

from dhos_questions_api.queries.softdelete import QueryWithSoftDelete


class Survey(ModelIdentifier, db.Model):
    query_class = QueryWithSoftDelete

    user_type = db.Column(db.String, unique=False, nullable=False)
    user_id = db.Column(db.String, unique=False, nullable=False)

    group_id = db.Column(db.String, db.ForeignKey("group.uuid"))
    group = db.relationship("Group")

    completed = db.Column(db.DateTime, unique=False, nullable=True)
    completed_tz = db.Column(db.Integer, unique=False, nullable=True)

    declined = db.Column(db.DateTime, unique=False, nullable=True)
    declined_tz = db.Column(db.Integer, unique=False, nullable=True)

    deleted = db.Column(db.DateTime, unique=False, nullable=True)

    @staticmethod
    def schema() -> Dict:
        return {
            "optional": {"completed": list, "declined": list},
            "required": {"user_type": str, "user_id": str, "group_id": str},
            "updatable": {"completed": list, "declined": list},
        }

    def to_dict(self) -> Dict:
        survey = {
            "user_type": self.user_type,
            "user_id": self.user_id,
            "group": self.group.to_dict(),
        }

        for key in ["completed", "declined"]:
            ts = getattr(self, key)
            if ts is not None:
                value = join_timestamp(ts, getattr(self, f"{key}_tz"))
                survey[key] = value

        if self.deleted is not None:
            survey["deleted"] = self.deleted

        return {**survey, **self.pack_identifier()}

    def delete(self) -> None:
        self.deleted = datetime.utcnow()

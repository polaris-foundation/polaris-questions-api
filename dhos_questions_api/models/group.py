from datetime import datetime
from typing import Dict

from flask_batteries_included.sqldb import ModelIdentifier, db

from dhos_questions_api.queries.softdelete import QueryWithSoftDelete


class Group(ModelIdentifier, db.Model):
    query_class = QueryWithSoftDelete

    group = db.Column(db.String, unique=False, nullable=False)

    deleted = db.Column(db.DateTime, unique=False, nullable=True)

    def to_dict(self) -> Dict:
        group = {"group": self.group}
        if self.deleted is not None:
            group["deleted"] = self.deleted
        return {**group, **self.pack_identifier()}

    def delete(self) -> None:
        self.deleted = datetime.utcnow()

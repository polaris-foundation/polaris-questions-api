from datetime import datetime
from typing import Dict

from flask_batteries_included.sqldb import ModelIdentifier, db

from dhos_questions_api.queries.softdelete import QueryWithSoftDelete

# Question option types
# 0 - fixed
# 1 - free text
# 2 - range start
# 3 - range end
# 4 - interval


class QuestionOptionType(ModelIdentifier, db.Model):
    query_class = QueryWithSoftDelete

    value = db.Column(db.Integer, unique=False, nullable=False)

    deleted = db.Column(db.DateTime, unique=False, nullable=True)

    def to_dict(self) -> Dict:
        qot = {"value": self.value}
        if self.deleted is not None:
            qot["deleted"] = self.deleted

        return {**qot, **self.pack_identifier()}

    def delete(self) -> None:
        self.deleted = datetime.utcnow()

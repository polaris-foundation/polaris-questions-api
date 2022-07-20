from datetime import datetime
from typing import Dict

from flask_batteries_included.sqldb import ModelIdentifier, db

from dhos_questions_api.queries.softdelete import QueryWithSoftDelete

# Question types
# 0 - free text
# 1 - integer
# 2 - checkbox
# 3 - radio
# 4 - drop down
# 5 - range
# 6 - multi-select


class QuestionType(ModelIdentifier, db.Model):
    query_class = QueryWithSoftDelete

    value = db.Column(db.Integer, unique=False, nullable=False)

    deleted = db.Column(db.DateTime, unique=False, nullable=True)

    def to_dict(self) -> Dict:
        qt = {"value": self.value}
        if self.deleted is not None:
            qt["deleted"] = self.deleted
        return {**qt, **self.pack_identifier()}

    def delete(self) -> None:
        self.deleted = datetime.utcnow()

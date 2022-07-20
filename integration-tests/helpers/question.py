from enum import Enum
from typing import Dict, Optional

from faker import Faker


class QuestionTypes(Enum):
    FREE_TEXT = 0
    INTEGER = 1
    CHECKBOX = 2
    RADIO = 3
    DROPDOWN = 4
    RANGE = 5
    MULTI_SELECT = 6


class QuestionOptionTypes(Enum):
    FIXED = 0
    FREE_TEXT = 1
    RANGE_START = 2
    RANGE_END = 3
    INTERVAL = 4


def get_body(**kwargs: Optional[Dict]) -> Dict:
    fake: Faker = Faker()
    default_body: dict = {
        "question_type": {"value": QuestionTypes.FREE_TEXT.value},
        "question": fake.sentence(),
        "groups": [{"group": "testing"}],
    }
    return {**default_body, **kwargs}

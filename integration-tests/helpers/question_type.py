from typing import Dict, Optional

from faker import Faker


def get_body(**kwargs: Optional[Dict]) -> Dict:
    fake: Faker = Faker()
    default_body: dict = {
        "value": fake.random_int(min=10),
        "uuid": fake.uuid4(),
    }
    return {**default_body, **kwargs}

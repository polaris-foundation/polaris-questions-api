from typing import Dict, List

from flask_batteries_included.sqldb import db

from dhos_questions_api.models.question import Question


def reset_database() -> None:
    session = db.session
    session.execute("TRUNCATE TABLE question cascade")
    session.execute("TRUNCATE TABLE question_option cascade")
    session.execute("TRUNCATE TABLE question_type cascade")
    session.execute("TRUNCATE TABLE question_option_type cascade")
    session.execute('TRUNCATE TABLE "group" cascade')
    session.execute("TRUNCATE TABLE question_group cascade")
    session.execute("TRUNCATE TABLE survey cascade")
    session.execute("TRUNCATE TABLE answer cascade")
    session.commit()
    session.close()


def get_questions() -> List[Dict]:
    questions: List[Question] = Question.query.all()
    return [question.to_dict() for question in questions]

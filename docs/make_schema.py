import codecs
import subprocess

import sadisplay

from dhos_questions_api.models import (
    answer,
    group,
    question,
    question_option,
    question_option_type,
    question_type,
    survey,
)

desc = sadisplay.describe(
    [
        answer.Answer,
        group.Group,
        question.Question,
        question_option.QuestionOption,
        question_option_type.QuestionOptionType,
        question_type.QuestionType,
        survey.Survey,
    ]
)
with codecs.open("docs/schema.plantuml", "w", encoding="utf-8") as f:
    f.write(sadisplay.plantuml(desc).rstrip() + "\n")

with codecs.open("docs/schema.dot", "w", encoding="utf-8") as f:
    f.write(sadisplay.dot(desc).rstrip() + "\n")

my_cmd = ["dot", "-Tpng", "docs/schema.dot"]
with open("docs/schema.png", "w") as outfile:
    subprocess.run(my_cmd, stdout=outfile)

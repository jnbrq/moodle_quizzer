from moodle_helper import *
from typing import *
import os

if __name__ == "__main__":
    package_names = filter(os.path.isdir, os.listdir(os.curdir))
    print("<?xml version=\"1.0\" ?>\n<quiz>")
    for package_name in package_names:
        m = __import__(f"questions_test.generate", fromlist=["generate"])
        questions: List[QuestionBase] = getattr(m, "generate_questions")()
        for question in questions:
            question.res_dir = f"./" + package_name
            print(question.render())
    print("</quiz>")

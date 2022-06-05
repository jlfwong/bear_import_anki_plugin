import re
import sqlite3
from typing import List, NamedTuple

# TODO: Move this into config
bear_db_path = "/Users/jlfwong/Library/Group Containers/9K33E3U3T4.net.shinyfrog.bear/Application Data/database.sqlite"

qa_pattern = re.compile('\nQ:(.*?)\nA:(.*?)\n(?:\n|$|[^a-zA-Z0-9"])')


class Prompt(NamedTuple):
    question: str
    answer: str
    context: str


def get_prompts_from_bear() -> List[Prompt]:
    con = sqlite3.connect(bear_db_path)
    prompts = []
    for (text, title) in con.execute("select ZTEXT, ZTITLE from ZSFNOTE"):
        for (question, answer) in qa_pattern.findall(text):
            prompts.append(Prompt(question.strip(), answer.strip(), title))
    return prompts


if __name__ == "__main__":
    print(get_prompts_from_bear())

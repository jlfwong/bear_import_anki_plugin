from inspect import getclosurevars
import re
import sqlite3
from typing import List, NamedTuple

# TODO: Move this into config
bear_db_path = "/Users/jlfwong/Library/Group Containers/9K33E3U3T4.net.shinyfrog.bear/Application Data/database.sqlite"

qa_pattern = re.compile(
    r'(?<=\n)Q: (.*?)\nA:(.*?)(?:\n)(?:\n|$|[^a-zA-Z0-9-. "])')

cq_pattern = re.compile(
    r'(?<=\n)CQ: (.*?)(?:\n\n|\n$|\n[^a-zA-Z0-9-. "])', re.DOTALL)


class Prompt(NamedTuple):
    question: str
    answer: str
    context: str


class Cloze(NamedTuple):
    text: str
    context: str


def get_prompts_from_bear() -> List[Prompt]:
    con = sqlite3.connect(bear_db_path)
    prompts = []
    for (text, title) in con.execute("select ZTEXT, ZTITLE from ZSFNOTE"):
        for (question, answer) in qa_pattern.findall(text):
            prompts.append(Prompt(question.strip(), answer.strip(), title))
    return prompts


cloze_pattern = re.compile("{{")


def replace_newlines(text):
    return text.replace("\n", "<br/>")


def get_cloze_from_bear() -> List[Cloze]:
    con = sqlite3.connect(bear_db_path)
    prompts = []
    for (text, title) in con.execute("select ZTEXT, ZTITLE from ZSFNOTE"):
        for (cloze) in cq_pattern.findall(text):
            card_front_body = cloze.strip()

            # Replace all instances of "{{" with "{{cN" where "N" increments, and starts at 1 after
            parts = []
            for (n, p) in enumerate(card_front_body.split("{{")):
                if n > 0:
                    parts.append("{{c" + str(n) + "::")
                parts.append(p)

            card_front_body = replace_newlines("".join(parts))

            prompts.append(Cloze(card_front_body, title))
    return prompts


ex = """
Q: How many lbs per kg?
A: ~2.2

Q: How much caffeine is in a cup of tea?
A: 50mg

Q: How much caffeine is in a cup of coffee?
A: 100mg

Q: What is Jeff Nippard's recommendation for volume caffeine intake pre-workout?
A: 4mg/kg of body weight (this is 260mg at 145lbs)
"""

ex = """
CQ: The ingredients of a White Russian are
- {{2 parts vodka}}
- {{1 part Kahlua}}
- {{Splash of heavy cream}}

CQ: The ingredients of an Elderflower spritz are
- {{1.5 parts St-Germain}}
- {{2 parts white wine}}
- {{2 parts club soda}}

CQ: The ingredients of a Moscow Mule are
- {{2 parts vodka}}
- {{1/2oz lime juice}}
- {{3 parts ginger beer}}
"""

if __name__ == "__main__":
    for c in get_cloze_from_bear():
        print(c)

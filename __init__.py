# import the main window object (mw) from aqt
import re
import time
from typing import List
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect
# import all of the Qt GUI library
from aqt.qt import QAction
from aqt import gui_hooks

from .bear import Prompt, get_cloze_from_bear, get_prompts_from_bear

from anki.notes import Note
from anki.decks import DeckId
from anki.models import NotetypeId

# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.

# TODO: Move this into config
deck_id = DeckId(1)

# Note type for "Bear Import Basic"
basic_note_type_id = NotetypeId(1654371237076)

# Note type for "Bear Import Cloze"
cloze_note_type_id = NotetypeId(1659241489874)


def note_already_exists(text) -> bool:
    if not mw:
        return True

    # find_notes takes an Anki search string, in which certain characters are
    # given special meaning. This can mean, for example, searching for the exact
    # contents of the front of the card may not find the card.
    #
    # To counter-act this, we replace all of the special characters with spaces.
    if not mw.col.find_notes(re.sub("[^a-zA-Z0-9-. ]", " ", text)):
        return False
    return True


def get_new_prompts():
    prompts_from_bear = get_prompts_from_bear()
    new_prompts = []
    for prompt in prompts_from_bear:
        if not note_already_exists(prompt.question):
            new_prompts.append(prompt)
    return new_prompts


def get_new_cloze():
    cloze_from_bear = get_cloze_from_bear()
    new_cloze = []
    for cloze in cloze_from_bear:
        if not note_already_exists(cloze.text):
            new_cloze.append(cloze)
    return new_cloze


def import_from_bear():
    if not mw:
        return

    before = time.process_time()

    new_prompts = get_new_prompts()
    for prompt in new_prompts:
        note = Note(mw.col, basic_note_type_id)
        note.fields = [prompt.question, prompt.answer, prompt.context]
        mw.col.add_note(note, deck_id)

    new_cloze = get_new_cloze()
    for cloze in new_cloze:
        note = Note(mw.col, cloze_note_type_id)
        back_extra = ""
        note.fields = [cloze.text, back_extra, cloze.context]
        mw.col.add_note(note, deck_id)

    elapsed = time.process_time() - before

    showInfo(
        f"Imported {len(new_prompts) + len(new_cloze)} new prompts from Bear in {elapsed:.1f}s. " +
        f"Topics: {', '.join(set(p.context for p in new_prompts) | set(c.context for c in new_cloze))}")


# create a new menu item, "test"
action = QAction("Import from Bear", mw)
# set it to call testFunction when it's clicked
qconnect(action.triggered, import_from_bear)
# and add it to the tools menu
if mw:
    mw.form.menuTools.addAction(action)

gui_hooks.main_window_did_init.append(import_from_bear)

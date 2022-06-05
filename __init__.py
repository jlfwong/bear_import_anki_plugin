# import the main window object (mw) from aqt
import time
from typing import List
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect
# import all of the Qt GUI library
from aqt.qt import QAction
from aqt import gui_hooks

from .bear import Prompt, get_prompts_from_bear

from anki.notes import Note
from anki.decks import DeckId
from anki.models import NotetypeId

# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.

# TODO: Move this into config
deck_id = DeckId(1)
note_type_id = NotetypeId(1654371237076)


def import_from_bear() -> List[Prompt]:
    if not mw:
        return []

    before = time.process_time()

    prompts_from_bear = get_prompts_from_bear()

    new_prompts = []

    for prompt in prompts_from_bear:
        matching_notes = mw.col.find_notes(prompt.question)
        if not matching_notes:
            new_prompts.append(prompt)

    for prompt in new_prompts:
        note = Note(mw.col, note_type_id)
        note.fields = [prompt.question, prompt.answer, prompt.context]
        mw.col.add_note(note, deck_id)

    elapsed = time.process_time() - before

    showInfo(
        f"Imported {len(new_prompts)} new prompts from Bear in {elapsed:.1f}s. " +
        f"Topics: {''.join(set(p.context for p in new_prompts))}")

    return new_prompts


# create a new menu item, "test"
action = QAction("Import from Bear", mw)
# set it to call testFunction when it's clicked
qconnect(action.triggered, import_from_bear)
# and add it to the tools menu
if mw:
    mw.form.menuTools.addAction(action)

gui_hooks.main_window_did_init.append(import_from_bear)

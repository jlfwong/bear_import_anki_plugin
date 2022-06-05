# Bear to Anki import

This repository contains an [Anki](https://apps.ankiweb.net/) [add-on](https://addon-docs.ankiweb.net/) for importing natural language prompts written in [Bear](https://bear.app/).

This allows you to write prompts inside of Bear notes that look like this:

    Q: Name an SRS system with a plug-in architecture
    A: Anki

And Anki will automatically create new notes whenever it's rebooted.

For now, it contains hard-coded file paths, Anki deck IDs, and note type IDs
that make this not re-usable out-of-the-box. I'm putting it out in the open just
in case it's a useful reference for anyone else.

## Installatiion

    python3 -m venv venv
    python3 -m pip install -r requirements.txt
    ln -s `pwd` ~/Library/Application\ Support/Anki2/addons21/bear-import

## TODO

- Move settings into config
- Add instructions for other people to use this if they want to
- Support Cloze notes
- Support updating notes somehow

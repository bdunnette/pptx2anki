# pptx2anki

Convert a PPTX file (with notes and/or annotated images) to an [Anki](https://apps.ankiweb.net/)-compatible flashcard deck.

## Installation

You'll probably want a virtualenv to install the dependencies in:

```
mkvirtualenv -p /usr/bin/python3 pptx2anki
```

Then, install those dependencies:

```
pip install -r requirements.txt
```

Finally, run the script:

```
./pptx2anki.py my_presentation.pptx
```

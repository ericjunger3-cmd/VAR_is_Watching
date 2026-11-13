# Saving and loading small texts: the saved game and the volume setting.
#
# On a computer they are normal files in the game folder (e.g. save_2d.json).
# In the web version the game runs inside the browser, where files are gone
# as soon as the page is closed. So there we use the browser's "localStorage"
# instead: a small store of texts that the browser keeps for this website,
# even after closing the page.

import os
import sys

# sys.platform is "emscripten" when Python runs inside a web browser
# (that is how pygbag runs the game). On a computer it is e.g. "win32".
IN_BROWSER = sys.platform == "emscripten"


def write_text(name, text):
    # Save a text under a name (the name is the file name, e.g. "save_2d.json").
    if IN_BROWSER:
        # In the browser, pygbag gives us the page's "window" through the
        # platform module. localStorage.setItem stores the text under the name.
        import platform
        platform.window.localStorage.setItem(name, text)
    else:
        with open(name, "w", encoding="utf-8") as file:
            file.write(text)


def read_text(name):
    # Give back the text saved under this name, or None if nothing was saved yet.
    if IN_BROWSER:
        import platform
        text = platform.window.localStorage.getItem(name)
        if text is None:
            return None
        return str(text)
    if not os.path.exists(name):
        return None
    with open(name, "r", encoding="utf-8") as file:
        return file.read()

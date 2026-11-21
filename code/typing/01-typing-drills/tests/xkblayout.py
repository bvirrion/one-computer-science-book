"""Read key legends from the system's xkb symbol files (read-only, local).

load("us") returns {xkb key name: [level-1 keysym, level-2 keysym, ...]}, following the
`include` lines of the layout's default section. Only what the typing drills need.
"""

import re
from pathlib import Path

ROOT = Path("/usr/share/X11/xkb/symbols")

# keysym names used by the us, fr and de layouts, as the characters they type
NAMED = {
    "space": " ", "exclam": "!", "at": "@", "numbersign": "#", "dollar": "$", "percent": "%",
    "asciicircum": "^", "ampersand": "&", "asterisk": "*", "parenleft": "(", "parenright": ")",
    "minus": "-", "underscore": "_", "equal": "=", "plus": "+", "bracketleft": "[",
    "bracketright": "]", "braceleft": "{", "braceright": "}", "semicolon": ";", "colon": ":",
    "apostrophe": "'", "quotedbl": '"', "grave": "`", "asciitilde": "~", "backslash": "\\",
    "bar": "|", "comma": ",", "less": "<", "period": ".", "greater": ">", "slash": "/",
    "question": "?", "eacute": "é", "egrave": "è", "agrave": "à", "ccedilla": "ç",
    "ugrave": "ù", "odiaeresis": "ö", "adiaeresis": "ä", "udiaeresis": "ü", "Odiaeresis": "Ö",
    "Adiaeresis": "Ä", "Udiaeresis": "Ü", "ssharp": "ß", "section": "§", "degree": "°",
    "sterling": "£", "mu": "µ", "twosuperior": "²",
}


def char(keysym):
    """The character a keysym types, or None (dead keys and the like)."""
    if len(keysym) == 1:
        return keysym
    return NAMED.get(keysym)


def _sections(text):
    out, default = {}, None
    for m in re.finditer(r'((?:\w+\s+)*)xkb_symbols\s+"([^"]+)"\s*\{', text):
        start = i = m.end()
        depth = 1
        while depth:
            depth += (text[i] == "{") - (text[i] == "}")
            i += 1
        out[m.group(2)] = text[start:i - 1]
        if default is None and "default" in m.group(1):
            default = m.group(2)
    return out, default or next(iter(out))


def load(spec, root=ROOT):
    m = re.match(r"([\w-]+)(?:\(([\w-]+)\))?", spec)
    text = re.sub(r"//[^\n]*", "", (root / m.group(1)).read_text())
    secs, default = _sections(text)
    keys = {}
    for tok in re.finditer(r'include\s+"([^"]+)"|key\s+<(\w+)>\s*\{([^}]*)\}', secs[m.group(2) or default]):
        if tok.group(1):
            for part in tok.group(1).split("+"):
                keys.update(load(part, root))
            continue
        # [Group1] and [group1] are indices (type[group1]="..."), not legends: xkeyboard-config 2.41 writes the
        # lower-case form, and after the legends.
        lists = [x for x in re.findall(r"\[([^\]]*)\]", tok.group(3))
                 if not re.fullmatch(r"\s*group\d+\s*", x, re.IGNORECASE)]
        if lists:
            keys[tok.group(2)] = [x.strip() for x in lists[-1].split(",")]
    return keys

from typing import Set

from talon import Module, Context, actions
import sys

default_alphabet = "air bat cap drum each fine gust harp sit jury crunch look made near odd pit quench red sun trap urge vest whale plex yank zip".split(
    " "
)
letters_string = "abcdefghijklmnopqrstuvwxyz"

default_digits = "zero one two three four five six seven eight nine".split(" ")
numbers = [str(i) for i in range(10)]
default_f_digits = "one two three four five six seven eight nine ten eleven twelve".split(
    " "
)

mod = Module()
mod.list("letter", desc="The spoken phonetic alphabet")
mod.list("symbol", desc="All symbols from the keyboard")
mod.list("arrow", desc="All arrow keys")
mod.list("number", desc="All number keys")
mod.list("modifier", desc="All modifier keys")
mod.list("function", desc="All function keys")
mod.list("special", desc="All special keys")


@mod.capture
def modifiers(m) -> str:
    "One or more modifier keys"


@mod.capture
def modifier_list(m) -> str:
    "A list of zero or more modifier keys"


@mod.capture
def arrow(m) -> str:
    "One directional arrow key"


@mod.capture
def arrows(m) -> str:
    "One or more arrows separate by a space"


@mod.capture
def number(m) -> str:
    "One number key"


@mod.capture
def letter(m) -> str:
    "One letter key"


@mod.capture
def letters(m) -> list:
    "Multiple letter keys"


@mod.capture
def symbol(m) -> str:
    "One symbol key"


@mod.capture
def function(m) -> str:
    "One function key"


@mod.capture
def special(m) -> str:
    "One special key"


@mod.capture
def unmodified_key(m) -> str:
    "A single key with no modifiers"


@mod.capture
def key(m) -> str:
    "A single key with optional modifiers"


@mod.capture
def keys(m) -> str:
    "A sequence of one or more keys with optional modifiers"


ctx = Context()
ctx.lists["self.modifier"] = {
    #"alt": "alt",
    #"command": "cmd",
    "control": "ctrl",  'troll':   'ctrl',
    #"option": "alt",
    "shift": "shift",  'shin': 'shift',
    "super": "super",
    "fly": "alt",
    "kid": "ctrl", "kit": "ctrl",
}
alphabet = dict(zip(default_alphabet, letters_string))
ctx.lists["self.letter"] = alphabet
ctx.lists["self.symbol"] = {
    "back tick": "`",
    "`": "`",
    "quasi": '`',
    "comma": ",",
    ",": ",",
    "dot": ".",
    "point": ".",
    "period": ".",
    "semi": ";",
    "semicolon": ";",
    "ticky": "'", #"quote": "'",
    #"L square": "[",
    #"left square": "[",
    "square": "[",
    #"R square": "]",
    "close square": "]", #"right square": "]",
    "forward slash": "/",
    "slash": "/",
    "backslash": "\\",
    "minus": "-",
    "dash": "-",
    "equals": "=",
    "plus": "+",
    "question mark": "?",
    "questo": "?",
    #"query": "?",
    "tilde": "~",
    "bang": "!",
    "exclamation point": "!",
    "dollar": "$",
    "dollar sign": "$",
    "down score": "_",
    "under score": "_",
    "colon": ":",
    "deckle": ":",
    "round": "(",
    #"L paren": "(",
    #"left paren": "(",
    #"R paren": ")",
    "close round": ")", #"right paren": ")",
    "curly": "{", #"brace": "{",
    #"left brace": "{",
    #"R brace": "}",
    "close curly": "}", #"right brace": "}",
    #"angle": "<",
    #"left angle": "<",
    "less than": "<",
    "langle": "<",
    "rangle": ">",
    #"R angle": ">",
    #"right angle": ">",
    "greater than": ">",
    "star": "*",
    "asterisk": "*",
    "pound": "#",
    "hash": "#",
    "hash sign": "#",
    "number sign": "#",
    "octo": "#",
    "percent": "%",
    "percent sign": "%",
    "carrot": "^",
    "at sign": "@",
    "and sign": "&",
    "ampersand": "&",
    "amper": "&",
    "pipe": "|",
    "ditto": '"', #"dubquote": '"',
    "double quote": '"',
    'open fancy': '“', 'close fancy': '”',
}


ctx.lists["self.number"] = dict(zip(default_digits, numbers))
ctx.lists["self.arrow"] = {
    "south": "down",
    "left": "left",
    "right": "right",
    "north": "up",
}

simple_keys = [
    "end",
    "enter",
    "escape",
    #"home",
    #"insert",
    "pagedown",
    "pageup",
    "space",
    "tab",
]

# try using ace for space if the new models ever get fast enough.
alternate_keys = {
    "head": "home", "tail": "end", "foot": "end",
#    'send': 'end',
    "delete": "backspace",
    "forward delete": "delete",
    'junk': 'backspace',
    'deli': 'delete',
    'pliny': 'end',
    'tap insert': 'insert',
    'swim': 'space',
    'void': 'space',
    "shock": "enter",
}
keys = {k: k for k in simple_keys}
keys.update(alternate_keys)
keys.update({'tap ' + x: x for x in ctx.lists['self.modifier']})
ctx.lists['self.special'] = keys
ctx.lists["self.function"] = {
    f"F {default_f_digits[i]}": f"f{i + 1}" for i in range(12)
}

@ctx.capture(rule="{self.modifier}+")
def modifiers(m):
    return "-".join(m.modifier_list)


@ctx.capture(rule="{self.modifier}*")
def modifier_list(m):
    try:
        return m.modifier_list
    except:
        return []


@ctx.capture(rule="{self.arrow}")
def arrow(m) -> str:
    return m.arrow


@ctx.capture(rule="<self.arrow>+")
def arrows(m) -> str:
    return str(m)


@ctx.capture(rule="{self.number}")
def number(m):
    return m.number


@ctx.capture(rule="{self.letter}")
def letter(m):
    return m.letter


@ctx.capture(rule="{self.special}")
def special(m):
    return m.special


@ctx.capture(rule="{self.symbol}")
def symbol(m):
    return m.symbol


@ctx.capture(rule="{self.function}")
def function(m):
    return m.function


@ctx.capture(
    rule="(<self.arrow> | <self.number> | <self.letter> | <self.symbol> | <self.function> | <self.special>)"
)
def unmodified_key(m) -> str:
    return str(m)


@ctx.capture(rule="<self.modifier_list> <self.unmodified_key>")
def key(m) -> str:
    return "-".join(m.modifier_list + [m.unmodified_key])


@ctx.capture(rule="<self.key>+")
def keys(m) -> str:
    return " ".join(m.key_list)


@ctx.capture(rule="{self.letter}+")
def letters(m):
    return m.letter_list


@mod.action_class
class Actions:
    def keys_uppercase_letters(m: list):
        """Inserts uppercase letters from list"""
        actions.insert("".join(m).upper())

    def get_alphabet() -> dict:
        """Provides the alphabet dictionary"""
        return alphabet


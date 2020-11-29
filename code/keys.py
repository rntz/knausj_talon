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
mod.list("symbol_key", desc="All symbols from the keyboard")
mod.list("arrow_key", desc="All arrow keys")
mod.list("number_key", desc="All number keys")
mod.list("modifier_key", desc="All modifier keys")
mod.list("function_key", desc="All function keys")
mod.list("special_key", desc="All special keys")
mod.list("punctuation", desc="words for inserting punctuation into text")


@mod.capture(rule="{self.modifier_key}+")
def modifiers(m) -> str:
    "One or more modifier keys"
    return "-".join(m.modifier_key_list)


@mod.capture(rule="{self.arrow_key}")
def arrow_key(m) -> str:
    "One directional arrow key"
    return m.arrow_key


@mod.capture(rule="<self.arrow_key>+")
def arrow_keys(m) -> str:
    "One or more arrow keys separated by a space"
    return str(m)


@mod.capture(rule="{self.number_key}")
def number_key(m) -> str:
    "One number key"
    return m.number_key


@mod.capture(rule="{self.letter}")
def letter(m) -> str:
    "One letter key"
    return m.letter


@mod.capture(rule="{self.special_key}")
def special_key(m) -> str:
    "One special key"
    return m.special_key


@mod.capture(rule="{self.symbol_key}")
def symbol_key(m) -> str:
    "One symbol key"
    return m.symbol_key


@mod.capture(rule="{self.function_key}")
def function_key(m) -> str:
    "One function key"
    return m.function_key


@mod.capture(
    rule="( <self.letter> | <self.number_key> | <self.symbol_key> "
    "| <self.arrow_key> | <self.function_key> | <self.special_key> )"
)
def unmodified_key(m) -> str:
    "A single key with no modifiers"
    return str(m)


@mod.capture(rule="{self.modifier_key}* <self.unmodified_key>")
def key(m) -> str:
    "A single key with optional modifiers"
    try:
        mods = m.modifier_key_list
    except AttributeError:
        mods = []
    return "-".join(mods + [m.unmodified_key])


@mod.capture(rule="<self.key>+")
def keys(m) -> str:
    "A sequence of one or more keys with optional modifiers"
    return " ".join(m.key_list)


@mod.capture(rule="{self.letter}+")
def letters(m) -> str:
    "Multiple letter keys"
    return "".join(m.letter_list)


ctx = Context()
ctx.lists["self.modifier_key"] = {
    # If you find 'alt' is often misrecognized, try using 'alter'.
    "alt": "alt",  #'alter': 'alt',
    #"command": "cmd",
    "control": "ctrl",  #'troll':   'ctrl',
    #"option": "alt",
    "shift": "shift",  'ship': 'shift',  #'sky': 'shift',
    "super": "super",
    "fly": "alt", "kiss": "ctrl",
    "alter": "alt", #"alley": "alt",
}
alphabet = dict(zip(default_alphabet, letters_string))
ctx.lists["self.letter"] = alphabet

# The `punctuation` list is for punctuation words that you want available both
# in dictation and as key names in command mode. The `symbol_key` list is for
# key names that should be available in command mode, but not during dictation.
punctuation_words = {
    # TODO: I'm not sure why we need these, I think it has something to do with
    # Dragon. Possibly it has been fixed by later improvements to talon? -rntz
    "`": "`", ",": ",", # <== these things
    "back tick": "`",
    "comma": ",",
    "period": ".",
    "semicolon": ";",
    "colon": ":",
    "forward slash": "/",
    "minus sign": "-",
    "plus sign": "+",
    "equal sign": "=", "equals sign": "=",
    "question mark": "?",
    "exclamation mark": "!",
    "exclamation point": "!",
    "dollar sign": "$",
    "left parenthesis": "(", "right parenthesis": ")",
    "left bracket": "[", "right bracket": "]",
    "left brace": "{", "right brace": "}",
    "less than sign": "<", "greater than sign": ">",
    "asterisk": "*",
    "hash sign": "#",
    "number sign": "#",
    "percent sign": "%",
    "at sign": "@",
    "and sign": "&",
    "ampersand": "&",
    "single quote": "'",
    "double quote": '"',
}
symbol_key_words = {
    "quasi": '`',
    "dot": ".",
    "point": ".",
    "semi": ";",
    "tick": "'", "ticky": "'", #"quote": "'",
    #"L square": "[",
    #"left square": "[",
    #"square": "[",
    #"R square": "]",
    #"close square": "]", #"right square": "]",
    "slash": "/",
    "stroke": "/", # seems to get recognized better at high speeds
    "backslash": "\\",
    "backer": "\\",
    "minus": "-",
    "dash": "-",
    "equals": "=",
    "plus": "+",
    "question": "?",
    "tilde": "~",
    "bang": "!",
    "dollar": "$",
    "down score": "_", "downs score": "_", "underscore": "_",
    "under": "_",
    "deckle": ":",
    #"L paren": "(",
    #"left paren": "(",
    #"R paren": ")",
    #"close round": ")", #"right paren": ")",
    #"curly": "{", #"brace": "{",
    #"left brace": "{",
    #"R brace": "}",
    #"close curly": "}", #"right brace": "}",
    #"angle": "<",
    #"left angle": "<",
    "less than": "<", "lesser": "<",
    #"R angle": ">",
    #"right angle": ">",
    "greater than": ">", "greater": ">",
    "star": "*",
    "pound": "#",
    "hash": "#",
    "octo": "#",
    #"percent": "%",
    "percy": "%",
    "carrot": "^",
    "amper": "&",
    "pipe": "|",
    "ditto": '"', #"dubquote": '"',
    "open single": "‘", "close single": "’",
    'open double': '“', 'close double': '”',
    "apostrophe": "’",
    "lub": "(", "rub": ")", #"leper": "(", "repper": ")",
    "lace": "{", "race": "}",
    "lack": "[", "rack": "]",
    "langle": "<", "wrangle": ">",
}
symbol_key_words.update(punctuation_words)

ctx.lists["self.punctuation"] = punctuation_words
ctx.lists["self.symbol_key"] = symbol_key_words
ctx.lists["self.number_key"] = dict(zip(default_digits, numbers))
ctx.lists["self.arrow_key"] = {
    "south": "down",
    "left": "left",
    "right": "right",
    "north": "up",
}

simple_keys = [
    "end",
    "enter",
    "escape",
    "home",
    #"insert",
    "pagedown",
    "pageup",
    "space",
    "tab",
]

# try using ace for space if the new models ever get fast enough.
alternate_keys = {
    "head": "home", "tail": "end", #"foot": "end",
    #"homer": "home", "end line": "end",
    'junk': 'backspace',
    'deli': 'delete',
    'overwrite': 'insert',
    "bar": "space",
    "break": "space",
    #'void': 'space',
    "slap": "enter",
    #"shock": "enter",
}
keys = {k: k for k in simple_keys}
keys.update(alternate_keys)
ctx.lists["self.special_key"] = keys
ctx.lists["self.function_key"] = {
    f"F {default_f_digits[i]}": f"f{i + 1}" for i in range(12)
}


@mod.action_class
class Actions:
    def get_alphabet() -> dict:
        """Provides the alphabet dictionary"""
        return alphabet


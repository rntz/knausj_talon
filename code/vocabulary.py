from talon import Context, Module, actions, grammar, registry
from .user_settings import bind_list_to_csv, bind_word_map_to_csv
from typing import Tuple, Optional

mod = Module()
ctx = Context()

mod.list("vocabulary", desc="additional vocabulary words")

@mod.capture(rule="({user.vocabulary} | <word>)")
def word(m) -> str:
    try:
        return m.vocabulary
    except AttributeError:
        return " ".join(actions.dictate.replace_words(actions.dictate.parse_words(m.word)))

@mod.capture(rule="({user.vocabulary} | <phrase>)+")
def text(m) -> str: return format_phrase(m)

@mod.capture(rule="({user.vocabulary} | {user.punctuation} | <phrase>)+")
def prose(m) -> str: return format_phrase(m)

# TODO: unify this formatting code with the dictation formatting code, so that
# user.prose behaves the same way as dictation mode.
def format_phrase(m):
    words = capture_to_word_list(m)
    result = ""
    for i, word in enumerate(words):
        if i > 0 and needs_space_between(words[i-1], word):
            result += " "
        result += word
    return result

def capture_to_word_list(m):
    words = []
    for item in m:
        words.extend(
            actions.dictate.replace_words(actions.dictate.parse_words(item))
            if isinstance(item, grammar.vm.Phrase) else
            item.split(" "))
    return words

no_space_before = set("\n .,!?;:-/%)]}")
no_space_after = set("\n -/#([{$£€¥₩₽₹")
def needs_space_between(before: str, after: str) -> bool:
    """TODO"""
    return (before != "" and after != ""
            and before[-1] not in no_space_after
            and after[0] not in no_space_before)

@mod.action_class
class FormattingActions:
    needs_space_between = needs_space_between

    def auto_capitalize(sentence_start: bool, text: str) -> Tuple[bool, str]:
        """
        Auto-capitalizes `text`. Pass sentence_start=True iff `text` starts at the
        beginning of a sentence should be capitalized. Returns
        (new_sentence_start, capitalized_text). new_sentence_start is True iff
        the end of text is the beginning of a new sentence.
        """
        # Imagine a metaphorical "capitalization charge" travelling through the
        # string left-to-right.
        charge = sentence_start
        output = ""
        for c in text:
            # Sentence endings create a charge.
            if c in ".!?":
                charge = True
            # Alphanumeric characters and commas absorb charge & try to
            # capitalize (for numbers & punctuation this does nothing, which is
            # what we want).
            elif charge and (c.isalnum() or c in ","):
                charge = False
                c = c.capitalize()
            # Otherwise the charge passes through (we do nothing).
            output += c
        return charge, output


# ---------- LISTS (punctuation, additional/replacement words) ----------
# Default words that will need to be capitalized (particularly under w2l).
_capitalize_defaults = [
    "I",
    "I'm",
    "I've",
    "I'll",
    "I'd",
    "Monday",
    "Mondays",
    "Tuesday",
    "Tuesdays",
    "Wednesday",
    "Wednesdays",
    "Thursday",
    "Thursdays",
    "Friday",
    "Fridays",
    "Saturday",
    "Saturdays",
    "Sunday",
    "Sundays",
    "January",
    "February",
    # March omitted because it's a regular word too
    "April",
    # May omitted because it's a regular word too
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

# Default words that need to be remapped.
_word_map_defaults = {
    # E.g:
    # "cash": "cache",
    # "centre": "center",
}
_word_map_defaults.update({word.lower(): word for word in _capitalize_defaults})

# "dictate.word_map" is used by `actions.dictate.replace_words` to rewrite words
# Talon recognized. Entries in word_map don't change the priority with which
# Talon recognizes some words over others.
bind_word_map_to_csv(
    "words_to_replace.csv",
    csv_headers=("Replacement", "Original"),
    default_values=_word_map_defaults,
)


# Default words that should be added to Talon's vocabulary.
_simple_vocab_default = ["admin", "LCD", "VPN", "DNS", "USB", "FAQ", "PhD", "Minecraft"]

# Defaults for different pronounciations of words that need to be added to
# Talon's vocabulary.
_default_vocabulary = {
    "N map": "nmap",
    "under documented": "under-documented",
}
_default_vocabulary.update({word: word for word in _simple_vocab_default})

# "user.vocabulary" is used to explicitly add words/phrases that Talon doesn't
# recognize. Words in user.vocabulary (or other lists and captures) are
# "command-like" and their recognition is prioritized over ordinary words.
bind_list_to_csv(
    "user.vocabulary",
    "additional_words.csv",
    csv_headers=("Word(s)", "Spoken Form (If Different)"),
    default_values=_default_vocabulary,
)

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
def prose(m) -> str:
    # registry.lists["user.punctuation"] returns a priority-ordered list of all
    # definitions of user.punctuation in active contexts; we want the currently
    # active value, so we take the last (highest priority).
    text = format_phrase(m, registry.lists.get("user.punctuation", [{}])[-1])
    _, text = actions.user.auto_capitalize(False, text)
    return text

# TODO: unify this formatting code with the dictation formatting code, so that
# user.prose behaves the same way as dictation mode.
def format_phrase(m, replacements=None):
    words = capture_to_word_list(m)
    if replacements:
        assert isinstance(replacements, dict)
        words = replace_word_sequences(replacements, words)
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

def replace_word_sequences(replacements, words):
    # bucket replacements by how many words they contain
    buckets = {}
    for pattern, replacement in replacements.items():
        pattern = tuple(pattern.split())
        buckets.setdefault(len(pattern), {})[pattern] = replacement
    # go through `words` position by position, replacing matching sequences
    result = []
    i = 0
    while i < len(words):
        consumed, emitted = 1, [words[i]]
        for (n, bucket) in buckets.items():
            if i + n > len(words): continue
            fragment = tuple(words[i:i+n])
            if fragment in bucket:
                consumed, emitted = n, bucket[fragment].split(" ")
                break
        i += consumed
        result.extend(emitted)
    return result

no_space_before = set(" .,/-!?;:)]}")
no_space_after = set("\n /-#$([{")
def needs_space_between(before: str, after: str) -> bool:
    return (before != "" and after != ""
            and before[-1] not in no_space_after
            and after[0] not in no_space_before)

@mod.action_class
class FormattingActions:
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
            # Alphanumeric characters absorb charge & try to capitalize (for
            # numbers this will do nothing, which is what we want).
            elif charge and c.isalnum():
                charge = False
                c = c.capitalize()
            # Otherwise the charge passes through (we do nothing).
            output += c
        return charge, output

    # TODO: perhaps this should be in dictation.py?
    def adjust_surrounding_space(text: str,
                                 pre: Optional[str],
                                 post: Optional[str]) -> str:
        """
        Adjusts the spacing at the beginning and end of `text` as appropriate for
        its surroundings, given by `pre` and `post`. If the text before/after is
        not known, pass None for pre/post respectively, and the spacing at
        beginning/end respectively will not get modified.
        """
        if pre is not None:
            # Avoid space at the beginning of a document or line; avoid more
            # than one space in a row.
            if pre == "" or pre[-1] in "\n ":
                # Only strip spaces; new lines etc should remain unchanged.
                text = text.lstrip(" ")
            # Otherwise, insert a space if necessary.
            elif needs_space_between(pre, text + (post or "")):
                text = " " + text
        if post is not None:
            if post == "" or post[0] in "\n ":
                text = text.rstrip(" ")
            elif needs_space_between((pre or "") + text, post):
                text = text + " "
        return text


# ---------- LISTS (punctuation, additional/replacement words) ----------
# Default words that will need to be capitalized (particularly under w2l).
capitalize = [
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
default_word_map = {
    # E.g:
    # "cash": "cache",
    # "centre": "center",
}
default_word_map.update({word.lower(): word for word in capitalize})

# "dictate.word_map" is used by `actions.dictate.replace_words` to rewrite words
# Talon recognized. Entries in word_map don't change the priority with which
# Talon recognizes some words over others.
bind_word_map_to_csv(
    "words_to_replace.csv",
    csv_headers=("Replacement", "Original"),
    default_values=default_word_map,
)


# Default words that should be added to Talon's vocabulary.
simple_vocabulary = ["admin", "LCD", "VPN", "DNS", "USB", "FAQ", "PhD", "Minecraft"]

# Defaults for different pronounciations of words that need to be added to
# Talon's vocabulary.
default_vocabulary = {
    "N map": "nmap",
    "under documented": "under-documented",
}
default_vocabulary.update({word: word for word in simple_vocabulary})

# "user.vocabulary" is used to explicitly add words/phrases that Talon doesn't
# recognize. Words in user.vocabulary (or other lists and captures) are
# "command-like" and their recognition is prioritized over ordinary words.
bind_list_to_csv(
    "user.vocabulary",
    "additional_words.csv",
    csv_headers=("Word(s)", "Spoken Form (If Different)"),
    default_values=default_vocabulary,
)

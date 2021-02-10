# Descended from https://github.com/dwiel/talon_community/blob/master/misc/dictation.py
from talon import Module, Context, ui, actions, clip, app, grammar
from typing import Optional, Tuple

mod = Module()
ctx = Context()

setting_dictation_context_sensitive = mod.setting(
    "dictation_context_sensitive",
    type=bool,
    default=False,
    desc="Look at surrounding text to improve auto-capitalization/spacing in dictation mode. By default, this works by selecting that text & copying it to the clipboard, so it may be slow or fail in some applications.",
)

@mod.capture(rule="({user.vocabulary} | <word>)")
def word(m) -> str:
    """A single word, including user-defined vocabulary."""
    try:
        return m.vocabulary
    except AttributeError:
        return " ".join(actions.dictate.replace_words(actions.dictate.parse_words(m.word)))

@mod.capture(rule="({user.vocabulary} | <phrase>)+")
def text(m) -> str:
    """A sequence of words, including user-defined vocabulary."""
    return format_phrase(m)

@mod.capture(rule="({user.vocabulary} | {user.punctuation} | <phrase>)+")
def prose(m) -> str:
    """Mixed words and punctuation, auto-spaced & capitalized."""
    text, _caps = auto_capitalize(format_phrase(m), False)
    return text


# ---------- FORMATTING ---------- #
def format_phrase(m):
    words = capture_to_words(m)
    result = ""
    for i, word in enumerate(words):
        if i > 0 and needs_space_between(words[i-1], word):
            result += " "
        result += word
    return result

def capture_to_words(m):
    words = []
    for item in m:
        words.extend(
            actions.dictate.replace_words(actions.dictate.parse_words(item))
            if isinstance(item, grammar.vm.Phrase) else
            item.split(" "))
    return words

no_space_before = set("\n .,!?;:-/%)]}\"")
no_space_after = set("\n -/#@([{$£€¥₩₽₹\"")
def needs_space_between(before: str, after: str) -> bool:
    return (before != "" and after != ""
            and before[-1] not in no_space_after
            and after[0] not in no_space_before)

def auto_capitalize(text: str, sentence_start: bool) -> Tuple[str, bool]:
    """
    Auto-capitalizes `text`. Pass sentence_start=True iff `text` starts at the
    beginning of a sentence should be capitalized. Returns
    (new_sentence_start, capitalized_text). new_sentence_start is True iff
    the end of text is the beginning of a new sentence.
    """
    # Imagine a metaphorical "capitalization charge" travelling through the
    # string left-to-right.
    charge = sentence_start
    newline = False # see BUG, below
    output = ""
    for c in text:
        # Sentence endings & double newlines create a charge.
        if c in ".!?" or (newline and c == "\n"):
            charge = True
        # Alphanumeric characters and commas absorb charge & try to
        # capitalize (for numbers & punctuation this does nothing, which is
        # what we want).
        elif charge and (c.isalnum() or c in ","):
            charge = False
            c = c.capitalize()
        # Otherwise the charge passes through (we do nothing).
        output += c
        newline = c == "\n"
    return output, charge

# BUG: auto_capitalize violates the following principle:
#
#     return auto_capitalize(text1 + text2, caps)
#
# should produce the same result as:
#
#     text1, caps = auto_capitalize(text1, caps)
#     text2, caps = auto_capitalize(text2, caps)
#     return text1 + text2, caps
#
# It violates this because we can let text1 = text2 = "\n". Then the first
# example will return True but the second will return the original value of
# caps. This bug will manifest if the user inserts two newlines separately, with
# context sensitivity disabled.
#
# The underlying problem is that if we ignore double-newlines we only need to
# look at characters one-by-one to determine how our state (the capitalization
# charge) changes. But double newlines are two characters. A better solution
# would need more states or more lookbehind.


# ---------- DICTATION AUTO FORMATTING ---------- #
class DictationFormat:
    def __init__(self):
        self.reset()

    def reset(self, before=None):
        self.before = ""
        # capitalization defaults to True
        self.caps = True

    def update_context(self, before):
        if before is None: return
        self.before = before
        _text, self.caps = auto_capitalize(before, True)

    def format(self, text):
        if needs_space_between(self.before, text):
            text = " " + text
        text, self.caps = auto_capitalize(text, self.caps)
        self.before = text or self.before
        return text

    def pass_through(self, text):
        # TODO: should this affect self.caps? I think so, but I'm not sure.
        _, self.caps = auto_capitalize(text, self.caps)
        self.before = text or self.before

dictation_formatter = DictationFormat()
ui.register("app_deactivate", lambda app: dictation_formatter.reset())
ui.register("win_focus", lambda win: dictation_formatter.reset())

@mod.action_class
class Actions:
    def dictation_format_reset():
        """Resets the dictation formatter"""
        return dictation_formatter.reset()

    def dictation_insert_raw(text: str):
        """Inserts text as-is, without invoking the dictation formatter."""
        dictation_formatter.pass_through(text)
        actions.insert(text)

    def dictation_insert(text: str) -> str:
        """Inserts dictated text, formatted appropriately."""
        # Whether we should try to be context-sensitive. Since whitespace is not
        # affected by formatter state, if text.isspace() is True we don't need
        # context-sensitivity.
        do_the_dance = (setting_dictation_context_sensitive.get()
                        and not text.isspace())
        if do_the_dance:
            dictation_formatter.update_context(
                actions.user.dictation_peek_left(clobber=True))
        text = dictation_formatter.format(text)
        actions.user.add_phrase_to_history(text)
        actions.insert(text)
        # Add a space after cursor if necessary.
        if not do_the_dance or not needs_space_between(text, "A"):
            # needs_space_between(text, "A") is an optimization to avoid calling
            # dictation_peek_right() if we definitely don't need to insert a
            # space. "A" is an arbitrary character chosen b/c it definitely
            # needs space before it.
            return
        char = actions.user.dictation_peek_right()
        if char is not None and needs_space_between(text, char):
            actions.insert(" ")
            actions.edit.left()

    def dictation_peek_left(clobber: bool = False) -> Optional[str]:
        """
        Tries to get some text before the cursor, ideally a word or two, for the
        purpose of auto-spacing & -capitalization. Results are not guaranteed;
        dictation_peek_left() may return None to indicate no information. (Note
        that returning the empty string "" indicates there is nothing before
        cursor, ie. we are at the beginning of the document.)

        If there is currently a selection, dictation_peek_left() must leave it
        unchanged unless `clobber` is true, in which case it may clobber it.
        """
        # Get rid of the selection if it exists.
        if clobber: actions.user.clobber_selection_if_exists()
        # Otherwise, if there's a selection, fail.
        elif "" != actions.edit.selected_text(): return None

        # In principle the previous word should suffice, but some applications
        # have a funny concept of what the previous word is (for example, they
        # may only take the "`" at the end of "`foo`"). To be double sure we
        # take two words left. I also tried taking a line up + a word left, but
        # edit.extend_up() = key(shift-up) doesn't work consistently in the
        # Slack webapp (sometimes escapes the text box).
        actions.edit.extend_word_left()
        actions.edit.extend_word_left()
        text = actions.edit.selected_text()
        # if we're at the beginning of the document/text box, we may not have
        # selected any text, in which case we shouldn't move the cursor.
        if text:
            # Unfortunately, in web Slack, if our selection ends at newline,
            # this will go right over the newline. Argh.
            actions.edit.right()
        return text

    def clobber_selection_if_exists():
        """Deletes the currently selected text if it exists; otherwise does nothing."""
        actions.key("space backspace")
        # This space-backspace trick is fast and reliable but has the
        # side-effect of cluttering the undo history. Other options:
        #
        # 1. Call edit.cut() inside a clip.revert() block. This assumes
        #    edit.cut() is supported AND will be a no-op if there's no
        #    selection. Unfortunately, sometimes one or both of these is false,
        #    eg. the notion webapp makes ctrl-x cut the current block by default
        #    if nothing is selected.
        #
        # 2. Test whether a selection exists by asking whether
        #    edit.selected_text() is empty; if it does, use edit.delete(). This
        #    usually uses the clipboard, which can be quite slow. Also, not sure
        #    how this would interact with switching edit.selected_text() to use
        #    the selection clipboard on linux, which can be nonempty even if no
        #    text is selected in the current application.
        #
        # Perhaps this ought to be configurable by a setting.

    def dictation_peek_right() -> Optional[str]:
        """
        Tries to get the character after the cursor for auto-spacing purposes.
        Results are not guaranteed; dictation_peek_right() may return None to
        indicate no information. (Note that returning the empty string ""
        indicates there is nothing after cursor, ie. we are at the end of the
        document.)
        """
        actions.edit.extend_right()
        char = actions.edit.selected_text()
        if char: actions.edit.left()
        return char

# Use the dictation formatter in dictation mode.
dictation_ctx = Context()
dictation_ctx.matches = r"""
mode: dictation
"""

@dictation_ctx.action_class("main")
class main_action:
    def auto_insert(text): actions.user.dictation_insert(text)

@dictation_ctx.action_class("user")
class main_action:
    def clear_last_phrase():
        # TODO: update dictation state using a history cache
        actions.next()

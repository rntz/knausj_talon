# Courtesy of https://github.com/dwiel/talon_community/blob/master/misc/dictation.py
# Port for Talon's new api + wav2letter
from talon import Module, Context, ui, actions
from typing import Optional

mod = Module()
ctx = Context()

# ---------- THE DICTATION CAPTURE ----------
@mod.capture(rule="<self.dictation_chunk>+")
def dictation(m) -> str:
    """
    A string of dictated text. Needs to be passed through user.dictation_format
    or similar for formatting.
    """
    return " ".join(m.dictation_chunk_list)

@mod.capture(rule="<user.text> | {user.dictation_map} | cap <user.word>")
def dictation_chunk(m) -> str:
    "An atomic chunk of dictated text."
    if m[0] == "cap":
        return actions.user.formatted_word(m.word, "CAPITALIZE_FIRST_WORD")
    else:
        return str(m)

## TODO: remove this junk code ##
# @mod.capture
# def dictation_chunk(m) -> str:
#     "An atomic chunk of dictated text."

# @ctx.capture("self.dictation_chunk", rule="<user.text> | {user.dictation_map}")
# def dictation_chunk_basic(m):
#     return str(m)

# # You can add complex actions to <user.dictation> by extending the
# # dictation_chunk capture, like so:
# @ctx.capture("self.dictation_chunk", rule="cap <user.word>")
# def dictation_chunk_capitalize_word(m):
#     return actions.user.formatted_text(m.word, "CAPITALIZE_FIRST_WORD")
## TODO: remove the above junk code ##

# You can add simple commands to <user.dictation> using this list. For more
# complex commands, you can extend the <user.dictation_chunk> capture; see
# above.
mod.list("dictation_map", desc="dictation mode text commands, for punctuation etc")
ctx.lists["user.dictation_map"] = {
    ## new line/paragraph produce these commands rather than literal new lines
    ## because dictation formatting splits the string on white space, so it
    ## ignores new lines. This is kind of a hack.
    "new line": "new-line",  # "enter": "new-line",
    "new paragraph": "new-paragraph",
    "period": ".",
    "comma": ",",  "kama": ",", "coma": ",",
    "question mark": "?",
    "exclamation mark": "!",
    "dash": "-",
    "colon": ":",
    "semicolon": ";",
    "semi colon": ";",
    "forward slash": "/",
}

mod.list(
    "dictation_begin",
    "key words for beginning dictation, mapped to whether they add a space",
)
mod.list(
    "dictation_end",
    "key words for ending dictation, mapped to whether they add a space",
)
ctx.lists["user.dictation_begin"] = {"say": "", "continue": " "}
ctx.lists["user.dictation_end"] = {"over": "", "break": " "}


# ---------- DICTATION AUTO FORMATTING ---------- #
no_space_before = set(",:;-/)")
no_space_after = set("-/( ")
# dictionary of sentence ends. No space should appear before these.
sentence_ends = {
    ".": ".",
    "?": "?",
    "!": "!",
    "new-paragraph": "\n\n",
    "new-line": "\n",
}


class DictationFormat:
    def __init__(self, before=None):
        self.reset(before=before)
        self.last_utterance = None
        self.paused = False

    # TODO: explain how the before parameter is used. For example, a before
    # value of " " will make caps false, but an empty before value "" will make
    # it true. This is slightly counterintuitive.
    def reset(self, before=None):
        # Default configuration.
        self.caps = True
        self.space = False

        # Set configuration from characters before cursor, if any.
        if before:
            self.space = before[-1] not in no_space_after
            before = before.rstrip(" ")
            self.caps = any(before.endswith(x) for x in sentence_ends.values())

    def pause(self, paused):
        self.paused = paused

    def format(self, text):
        if self.paused:
            self.last_utterance = text
            return text

        result = ""
        for word in text.split():
            is_sentence_end = False

            if word in sentence_ends:
                word = sentence_ends[word]
                is_sentence_end = True
            elif self.space and word not in no_space_before:
                result += " "

            if self.caps:
                word = word.capitalize()

            result += word
            self.space = "\n" not in word and word[-1] not in no_space_after
            self.caps = is_sentence_end
            self.last_utterance = result

        return result


dictation_formatter = DictationFormat()
ui.register("app_deactivate", lambda app: dictation_formatter.reset())
ui.register("win_focus", lambda win: dictation_formatter.reset())


@mod.action_class
class Actions:
    def dictation_format(text: str) -> str:
        """Formats dictated text."""
        return dictation_formatter.format(text)

    def dictation_format_stateless(text: str, before: Optional[str] = None) -> str:
        """
        Formats text as if it were dictated, but without using or affecting the
        state of the dictation formatter. `before` is a hint used to determine
        capitalization and spacing; it should consist of a few characters before
        the cursor.
        """
        formatter = DictationFormat(before=before)
        return formatter.format(text)

    def dictation_format_pause():
        """Pauses the dictation formatter"""
        return dictation_formatter.pause(True)

    def dictation_format_resume():
        """Resumes the dictation formatter"""
        return dictation_formatter.pause(False)

    def dictation_format_reset():
        """Resets the dictation formatter"""
        return dictation_formatter.reset()

    def dictation_clear_last():
        """Deletes the last dictated utterance"""
        if dictation_formatter.last_utterance:
            for c in dictation_formatter.last_utterance:
                actions.edit.delete()

    def dictation_select_last():
        """Selects the last dictated utterance"""
        if dictation_formatter.last_utterance:
            for c in dictation_formatter.last_utterance:
                actions.edit.extend_left()


# Use the dictation formatter in dictation mode.
dictation_ctx = Context()
dictation_ctx.matches = r"""
mode: dictation
"""

@dictation_ctx.action_class("main")
class main_action:
    def auto_format(text):
        return actions.user.dictation_format(text)

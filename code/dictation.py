# Courtesy of https://github.com/dwiel/talon_community/blob/master/misc/dictation.py
# Port for Talon's new api + wav2letter
from talon import Module, Context, ui, actions, clip, app
from typing import Optional, Tuple

mod = Module()
ctx = Context()

setting_dictation_copy_surrounding_text = mod.setting(
    "dictation_copy_surrounding_text",
    type=bool,
    default=False,
    desc="Copy surrounding text via clipboard to improve auto-capitalization/spacing in dictation mode. This may be slow or not work in all applications.",
)

setting_dictation_clobber_behavior = mod.setting(
    "dictation_clobber_behavior",
    type=str,
    default="cut",
    desc="""When inserting dictated text and using the surrounding text to inform auto-capitalization/spacing, we need to clobber (delete) the selection if it exists before we can look at the surrounding text. We can do this in a few ways:

    - "cut" (the default) means we issue an unconditional edit.cut(), which should delete the selection if it exists and do nothing otherwise. This is a compromise between speed and safety.

    - "test" checks if there is a selection using edit.selected_text(), and if so, uses edit.delete(). This is the slowest but safest option, useful if edit.cut() is not a no-op when the selection does not exist.

    - "noop" does nothing, which is fast, but will do the wrong thing if there is a selection.
    """
)

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

# # ---------- THE DICTATION CAPTURE (DEPRECATED/UNUSED) ----------
# @mod.capture(rule="<self.dictation_chunk>+")
# def dictation(m) -> str:
#     """
#     A string of dictated text. Needs to be passed through user.dictation_format
#     or similar for formatting.
#     """
#     return " ".join(m.dictation_chunk_list)

# @mod.capture(rule="<user.text> | {user.dictation_map} | cap <user.word>")
# def dictation_chunk(m) -> str:
#     "An atomic chunk of dictated text."
#     if m[0] == "cap":
#         return actions.user.formatted_word(m.word, "CAPITALIZE_FIRST_WORD")
#     else:
#         return str(m)

# # You can add simple commands to <user.dictation> using this list. For more
# # complex commands, you can extend the <user.dictation_chunk> capture; see
# # above.
# mod.list("dictation_map", desc="dictation mode text commands, for punctuation etc")
# ctx.lists["user.dictation_map"] = {
#     ## new line/paragraph produce these commands rather than literal new lines
#     ## because dictation formatting splits the string on white space, so it
#     ## ignores new lines. This is kind of a hack.
#     #"new line": "new-line",  # "enter": "new-line",
#     #"new paragraph": "new-paragraph",
#     "new line": "\n", "new paragraph": "\n\n",
#     "period": ".",
#     "comma": ",",  "kama": ",", "coma": ",",
#     "question mark": "?",
#     "exclamation mark": "!",
#     "dash": "-",
#     "colon": ":",
#     "semicolon": ";",
#     "semi colon": ";",
#     "forward slash": "/",
# }


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
        self.caps = actions.user.auto_capitalize(True, before)[0]

    def format(self, text):
        if actions.user.needs_space_between(self.before, text):
            text = " " + text
        self.caps, text = actions.user.auto_capitalize(self.caps, text)
        self.before = text or self.before
        return text

    def pass_through(self, text):
        # TODO: should this affect self.caps? I think so, but I'm not sure.
        self.caps, _ = actions.user.auto_capitalize(self.caps, text)
        self.before = text or self.before

dictation_formatter = DictationFormat()
ui.register("app_deactivate", lambda app: dictation_formatter.reset())
ui.register("win_focus", lambda win: dictation_formatter.reset())

@mod.action_class
class Actions:
    def dictation_format(text: str) -> str:
        """Formats dictated text."""
        return dictation_formatter.format(text)

    def dictation_insert(text: str) -> str:
        """Inserts dictated text, formatted appropriately."""
        # This text.isspace() test is an optimization; whitespace neither
        # affects nor is affected by formatter state, so examining the context
        # is unnecessary.
        if not text.isspace():
            dictation_formatter.update_context(actions.user.peek_left(clobber=True))
        text = actions.user.dictation_format(text)
        actions.user.add_phrase_to_history(text)
        actions.insert(text)
        actions.user.fix_space_right(text)

    def dictation_insert_raw(text: str):
        """Inserts text as-is, without invoking the dictation formatter."""
        dictation_formatter.pass_through(text)
        actions.insert(text)

    def dictation_format_reset():
        """Resets the dictation formatter"""
        return dictation_formatter.reset()

    def dictation_format_auto():
        """Tries to update the dictation formatter state according to the text
        around the cursor."""
        dictation_formatter.update_context(actions.user.peek_left(user_request=True))

    def peek_left(user_request: bool = False, clobber: bool = False) -> Optional[str]:
        """
        Tries to get some of the text before the cursor, ideally one word, for
        the purpose of context-sensitive spacing & capitalization. Results are
        not guaranteed; peek_left() may return None to indicate no information.
        (Note that returning the empty string "" indicates there is nothing
        before cursor, ie. we are at the beginning of the document.)

        `user_request` indicates whether this peek_left() was performed
        automatically or user-requested. If true, peek_left() ignores settings
        that would otherwise disable it, like
        setting_dictation_copy_surrounding_text.

        If there is currently a selection, peek_left() must leave it unchanged
        unless `clobber` is true, in which case it may clobber it.
        """
        if not user_request and not setting_dictation_copy_surrounding_text.get():
            return None

        if clobber:
            # get rid of the selection if it exists.
            behavior = setting_dictation_clobber_behavior.get()
            if behavior == "noop": pass
            elif behavior == "test":
                if "" != actions.edit.selected_text():
                    actions.edit.delete()
            else:
                # TODO: test this doesn't affect the clipboard.
                with clip.revert(): actions.edit.cut()
        # Otherwise, if there's a selection, fail.
        elif "" != actions.edit.selected_text():
            return None

        # In principle the previous word should suffice, but some applications
        # have a funny concept of what the previous word is (for example, they
        # may only take the "`" at the end of "`foo`"). To be double sure we
        # first select a line up then a word left. TODO: perhaps this should be
        # configurable?
        #actions.edit.extend_up() # doesn't work in web slack
        actions.edit.extend_word_left()
        actions.edit.extend_word_left()
        text = actions.edit.selected_text()
        # if we're at the beginning of the document/text box, we may not have
        # selected any text, in which case we shouldn't move the cursor.
        if text:
            ## Unfortunately, this fails in Slack if our selection ends at
            ## newline. This can be fixed using ctrl-right, but ugh.
            actions.edit.right()
            #actions.key("ctrl-right")
        return text

    def peek_right() -> Optional[str]:
        """TODO"""
        if not setting_dictation_copy_surrounding_text.get():
            return None
        actions.edit.extend_right()
        char = actions.edit.selected_text()
        # ARGH, this doesn't work if we're at the end of a line in firefox/chrome!
        # selecting down seems to work _more_ often, but not if next line is empty :(
        if char: actions.edit.left()
        return char

    def fix_space_right(before: str):
        """TODO"""
        # Exit early to avoid calling peek_right() if we definitely don't need
        # to insert a space. "A" is an arbitrary character chosen b/c it
        # definitely needs space before it.
        if not actions.user.needs_space_between(before, "A"): return
        char = actions.user.peek_right()
        if char is not None and actions.user.needs_space_between(before, char):
            actions.insert(" ")
            actions.edit.left()

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

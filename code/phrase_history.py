from talon import Module, Context, actions, ui, imgui, app
from talon.grammar import Phrase
from typing import List, Union

mod = Module()
ctx = Context()

# list of recent phrases, most recent first
phrase_history = []
phrase_history_length = 40
phrase_history_display_length = 40

# Make auto_insert add the inserted text to the phrase history.
@ctx.action_class("main")
class MainActions:
    def auto_insert(text: str):
        text = actions.auto_format(text)
        actions.user.add_phrase_to_history(text)
        actions.insert(text)

@mod.action_class
class Actions:
    def get_last_phrase() -> str:
        """Gets the last phrase"""
        return phrase_history[0] if phrase_history else ""

    def get_recent_phrase(number: int) -> str:
        """Gets the nth most recent phrase"""
        if 1 <= number <= len(phrase_history):
            return phrase_history[number-1]
        return ""

    def clear_last_phrase():
        """Clears the last phrase"""
        # TODO: Currently, this removes the cleared phrase from the phrase
        # history, so that repeated calls clear successively earlier phrases,
        # which is often useful. But it would be nice if we could do this
        # without removing those phrases from the history entirely, so that they
        # were still accessible for copying, for example.
        if not phrase_history: return
        for _ in phrase_history[0]:
            actions.edit.delete()
        phrase_history.pop(0)

    def select_last_phrase():
        """Selects the last phrase"""
        if not phrase_history: return
        for _ in phrase_history[0]:
            actions.edit.extend_left()

    def add_phrase_to_history(text: str):
        """Adds a phrase to the phrase history"""
        global phrase_history
        phrase_history.insert(0, text)
        phrase_history = phrase_history[:phrase_history_length]

    def toggle_phrase_history():
        """Toggles list of recent phrases"""
        if gui.showing: gui.hide()
        else: gui.show()

@imgui.open()
def gui(gui: imgui.GUI):
    gui.text("Recent phrases")
    gui.line()
    for index, text in enumerate(phrase_history[:phrase_history_display_length], 1):
        gui.text(f"{index}: {text}")

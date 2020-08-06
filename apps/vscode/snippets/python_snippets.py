from talon import Context, actions, ui, Module, app
from ....code.snippet_watcher import snippet_watcher
import os

ctx = Context()
ctx.matches = r"""
app: Code
app: Code - OSS
app: Code
app: Visual Studio Code
app: Code.exe
mode: user.python
mode: command 
and code.language: python
"""


def update_list(watch_list):
    ctx.lists["user.snippets"] = watch_list


# there's probably a way to do this without
# if app.platform == "windows":
watcher = snippet_watcher(
    {
        os.path.expandvars(r"%AppData%\Code\User\snippets"): ["python.json"],
        os.path.expandvars(
            r"%USERPROFILE%\.vscode\extensions\ms-python.python-2020.7.96456\snippets"
        ): ["python.json"],
    },
    update_list,
)


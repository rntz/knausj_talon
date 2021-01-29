not mode: sleep
-
^dictation mode$:
    mode.disable("sleep")
    mode.disable("command")
    mode.enable("dictation")
^command mode$:
    mode.disable("sleep")
    mode.disable("dictation")
    mode.enable("command")

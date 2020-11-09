force language see sharp: user.code_set_language_mode("csharp")
force language see plus plus: user.code_set_language_mode("cplusplus")
force language go [lang|language]: user.code_set_language_mode("go")
force language java script: user.code_set_language_mode("javascript")
force language type script: user.code_set_language_mode("typescript")
force language markdown: user.code_set_language_mode("markdown")
force language python: user.code_set_language_mode("python")
force language (R | are): user.code_set_language_mode("r")
force language (tex|latex): user.code_set_language_mode("tex")
force language talon: user.code_set_language_mode("talon")
clear language modes: user.code_clear_language_mode()
[enable] debug mode:
    mode.enable("user.gdb")
disable debug mode:
    mode.disable("user.gdb")
    
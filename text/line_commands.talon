tag: user.line_commands
-
#this defines some common line commands. More may be defined that are ide-specific.
#lend: edit.line_end()
#bend: edit.line_start()
go <number>: edit.jump_line(number)
go <number> end:
    edit.jump_line(number)
    edit.line_end()
comment line <number>:
    user.select_range(number, number)
    code.toggle_comment()
comment [line] <number> until <number>:
    user.select_range(number_1, number_2)
    code.toggle_comment()
delete line <number>:
    edit.jump_line(number)
    user.select_range(number, number)
    edit.delete()
delete [line] <number> until <number>:
    user.select_range(number_1, number_2)
    edit.delete()
copy line <number>:
    user.select_range(number, number)
    edit.copy()
copy [line] <number> until <number>:
    user.select_range(number_1, number_2)
    edit.copy()
cut line <number>:
    user.select_range(number, number)
    edit.cut()
cut [line] <number> until <number>:
    user.select_range(number_1, number_2)
    edit.cut()
paste [line] <number> until <number>:
  user.select_range(number_1, number_2)
  edit.paste()
replace [line] <number> until <number>:
    user.select_range(number_1, number_2)
    edit.paste()
(select | cell | sell) line <number>: user.select_range(number, number)
(select | cell | sell) <number> until <number>: user.select_range(number_1, number_2)
indent that: edit.indent_more()
indent line <number>:
    edit.jump_line(number)
    edit.indent_more()
indent <number> until <number>:
    user.select_range(number_1, number_2)
    edit.indent_more()
dedent that: edit.indent_less()
dedent line <number>:
    user.select_range(number, number)
    edit.indent_less()
dedent <number> until <number>:
    user.select_range(number_1, number_2)
    edit.indent_less()
drag line down: edit.line_swap_down()
drag line up: edit.line_swap_up()
drag up line <number>:
    user.select_range(number, number)
    edit.line_swap_up()
drag up <number> until <number>:
    user.select_range(number_1, number_2)
    edit.line_swap_up()
drag down line <number>:
    user.select_range(number, number)
    edit.line_swap_down()
drag down <number> until <number>:
    user.select_range(number_1, number_2)
    edit.line_swap_down()
clone line: edit.line_clone()

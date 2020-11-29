tag: user.tabs
-
open tab | tab (open | new): app.tab_open()
last tab | tab last: app.tab_previous()
next tab | tab next: app.tab_next()
close tab | tab close: app.tab_close()
reopen tab | tab reopen: app.tab_reopen()
go tab <number>: user.tab_jump(number)
go tab final: user.tab_final()

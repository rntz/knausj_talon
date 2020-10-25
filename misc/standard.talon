#(jay son | jason ): "json"
#(http | htp): "http"
#tls: "tls"
#M D five: "md5"
#word (regex | rejex): "regex"
#word queue: "queue"
#word eye: "eye"
#word iter: "iter"
#word no: "NULL"
#word cmd: "cmd"
#word dup: "dup"
#word shell: "shell".
zoom in: edit.zoom_in()
zoom out: edit.zoom_out()
scroll up: key(pgup)
scroll [down]: key(pgdown)
copy that: edit.copy()
cut that: edit.cut()
paste that: edit.paste()
undo [that]: edit.undo()
redo that: edit.redo()
paste match: edit.paste_match_style()
file save: edit.save()
padding:
	insert("  ") 
	key(left)
disabled command but use tail slap to do the same thing:
	edit.line_end()
	key(enter)
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
zoom reset: edit.zoom_reset()
scroll up: key(pgup)
scroll [down]: key(pgdown)
copier | copy that: edit.copy()
cutter | cut that: edit.cut()
paster | paste that: edit.paste()
undue: skip()
(undo | undue) that:
  edit.undo()
  user.quick_macro_set("edit.undo")
redo that: edit.redo()
paste match: edit.paste_match_style()
file save: edit.save()
padding:
	insert("  ") 
	key(left)
disabled command but use push to do the same thing:
	edit.line_end()
	key(enter)
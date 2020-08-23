slap:
	edit.line_end()
	key(enter)
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
#word shell: "shell"
# args: 
# 	insert("()")
# 	key(left)
# [inside] (index | array): 
# 	insert("[]") 
# 	key(left)
# empty array: "[]"
# list in it: 
# 	insert("[]") 
# 	key(left)
# (dickt in it | inside bracket | in bracket): 
# 	insert("{}") 
# 	key(left)
# (in | inside) percent: 
# 	insert("%%") 
# 	key(left)
zoom in: edit.zoom_in()
zoom out: edit.zoom_out()
scroll up: key(pgup)
scroll [down]: key(pgdown)
copy that: edit.copy()
cut that: edit.cut()
paste that: edit.paste()
undo that: edit.undo()
redo that: edit.redo()
paste match: edit.paste_match_style()
file save: edit.save()
volume up: key(volup)
volume down: key(voldown)
volume (mute|toggle)|mute it: key(mute)
play next: key(next)
play previous: key(prev)
(play | pause) it: key(play_pause)  
#wipe: key(backspace)    
padding: 
	insert("  ") 
	key(left)

#provide both anchored and unachored commands via 'over'
<user.format_text>$: insert(format_text)
<user.format_text> (over|break): insert(format_text)
phrase <user.text>$: insert(user.text)
phrase <user.text> (break|over): insert(user.text)
(say | speak) <user.text>$: insert(user.text)
(say | speak) <user.text> (break|over): insert(user.text)
word <user.word>: insert(user.word)
run <user.word>: insert('{word} ')
list formatters: user.list_formatters()
hide formatters: user.hide_formatters()

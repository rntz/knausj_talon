word <user.word>: insert(user.word)
big word <user.word>: user.insert_formatted(word, "CAPITALIZE_FIRST_WORD")
run <user.word>: insert('{word} ')

#provide both anchored and unachored commands via 'over' and 'break'
phrase <user.text>$: user.insert_formatted(text, "NOOP")
phrase <user.text> {user.dictation_end}:
  user.insert_formatted(text + dictation_end, "NOOP")

# sentence <user.prose>$:
#   user.insert_formatted(prose, "CAPITALIZE_FIRST_WORD")
# {user.dictation_begin} <user.prose>$:
#   user.insert_formatted(dictation_begin + prose, "NOOP")
# {user.dictation_begin} <user.prose> {user.dictation_end}:
#   prose = dictation_begin + prose
#   user.insert_formatted(prose + dictation_end, "NOOP")

say <user.prose>$: user.dictation_insert(prose)
say <user.prose> over: user.dictation_insert(prose)
prose <user.prose>$: user.insert_formatted(prose, "NOOP")
prose <user.prose> over: user.insert_formatted(prose, "NOOP")

<user.format_text>+$: user.insert_many(format_text_list)
<user.format_text>+ {user.dictation_end}:
  user.insert_many(format_text_list)
  insert(dictation_end)
<user.formatters> that: user.formatters_reformat_selection(user.formatters)
format help: user.formatters_help_toggle()
^nope that was <user.formatters>$:
  user.formatters_reformat_last(user.formatters)

# Quick switch to dictation mode.
dictation mode [<user.prose>]$:
  mode.disable("sleep")
  mode.disable("command")
  mode.enable("dictation")
  user.dictation_insert(prose or "")

recent list: user.toggle_phrase_history()
recent copy <number_small>: clip.set_text(user.get_recent_phrase(number_small))
recent repeat <number_small>: auto_insert(user.get_recent_phrase(number_small))

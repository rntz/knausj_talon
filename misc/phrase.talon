word <user.word>: insert(user.word)
upper word <user.word>: user.insert_formatted(word, "CAPITALIZE_FIRST_WORD")
run <user.word>: insert('{word} ')

#provide both anchored and unachored commands via 'over' and 'break'
phrase <user.text>$: user.insert_formatted(text, "NOOP")
phrase <user.text> {user.dictation_end}:
  user.insert_formatted(text + dictation_end, "NOOP")

{user.dictation_begin} <user.dictation>$:
  text = user.dictation_format_stateless(dictation, " ")
  user.insert_formatted(dictation_begin + text, "NOOP")
{user.dictation_begin} <user.dictation> {user.dictation_end}:
  text = user.dictation_format_stateless(dictation, " ")
  text = text + dictation_end
  insert(user.formatted_text(dictation_begin + text, "NOOP"))

<user.format_text>+$: user.insert_many(format_text_list)
<user.format_text>+ {user.dictation_end}:
  user.insert_many(format_text_list)
  insert(dictation_end)
<user.formatters> that: user.formatters_reformat_selection(user.formatters)
format help: user.formatters_help_toggle()
^nope that was <user.formatters>$:
  user.formatters_reformat_last(user.formatters)

# Quick switch to dictation mode.
dictation mode [<user.dictation>]$:
  mode.disable("sleep")
  mode.disable("command")
  mode.enable("dictation")
  insert(user.dictation_format(dictation or ""))

scratch that | ^nope that$: user.clear_last_phrase()
recent list: user.toggle_phrase_history()
recent copy <number_small>: clip.set_text(user.get_recent_phrase(number_small))
recent repeat <number_small>: auto_insert(user.get_recent_phrase(number_small))

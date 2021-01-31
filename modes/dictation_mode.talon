mode: dictation
-
^press <user.keys>: key("{keys}")
<user.prose>: auto_insert(prose)
new line: "\n"
new paragraph:
  "\n\n"
  # A hack. Currently the formatter ignores new lines, so it will only start
  # capitalizing if the previous paragraph ended with a period or other sentence
  # ending. This forces it to capitalize.
  user.dictation_format_reset()
cap <user.word>:
  result = user.formatted_text(word, "CAPITALIZE_FIRST_WORD")
  auto_insert(result)

# #navigation
# go up <number_small> lines:
#     edit.up()
#     repeat(number_small - 1)
# go down <number_small> lines:
#     edit.down()
#     repeat(number_small - 1)
# go left <number_small> words: 
#     edit.word_left()
#     repeat(number_small - 1)
# go right <number_small> words: 
#     edit.word_right()
#     repeat(number_small - 1)
# go line start: edit.line_start()
# go line end: edit.line_end()

#selection
select left <number_small> words:
    edit.extend_word_left()
    repeat(number_small - 1)
select right <number_small> words:
    edit.extend_word_right()
    repeat(number_small - 1)
select left <number_small> characters:
    edit.extend_left()
    repeat(number_small - 1)
select right <number_small> characters:
    edit.extend_right()
    repeat(number_small - 1)
# clear left <number_small> words:
#     edit.extend_word_left()
#     repeat(number_small - 1)
#     edit.delete()
# clear right <number_small> words:
#     edit.extend_word_right()
#     repeat(number_small - 1)
#     edit.delete()
clear left <number_small> characters:
    edit.extend_left()
    repeat(number_small - 1)
    edit.delete()
clear right <number_small> characters:
    edit.extend_right()
    repeat(number_small - 1)
    edit.delete()

#formatting 
formatted <user.format_text>:
    user.dictation_insert_raw(format_Text)
^format selection <user.formatters>$:
    user.formatters_reformat_selection(formatters)

#corrections
scratch selection: edit.delete()
spell that <user.letters>: auto_insert(letters)
spell that <user.formatters> <user.letters>:
    result = user.formatted_text(letters, formatters)
    user.dictation_insert_raw(result)

#escape, type things that would otherwise be commands
^escape <user.text>$:
    auto_insert(user.text)

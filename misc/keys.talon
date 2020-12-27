<user.arrow_key>: key(arrow_key)
<user.letter>: key(letter)
(shift | ship | uppercase) <user.letters> [(lowercase | sunk | over)]:
    user.insert_formatted(letters, "ALL_CAPS")
<user.symbol_key>: key(symbol_key)
<user.function_key>: key(function_key)
<user.special_key>: key(special_key)
<user.modifiers> <user.unmodified_key>: key("{modifiers}-{unmodified_key}")
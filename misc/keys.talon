<user.arrows>: key(arrows)
#disabled due to https://github.com/talonvoice/beta/issues/90
#<user.number>: key(number)
<user.letter>: key(letter)
(shift | ship | uppercase) <user.letters> [(lowercase | sunk | over)]:
    user.keys_uppercase_letters(letters)
<user.symbol>: key(symbol)
<user.function_key>: key(function_key)
<user.special_key>: key(special_key)
<user.modifiers> <user.unmodified_key>: key("{modifiers}-{unmodified_key}")

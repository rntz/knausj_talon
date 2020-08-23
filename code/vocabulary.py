from talon import Context, Module, actions, grammar


simple_vocabulary = [
    "nmap",
    "admin",
    "Cisco",
    "Citrix",
    "VPN",
    "DNS",
    "minecraft",
    "emacs",
    "tuple",
    "diff",
    "timezone",
    "grep",
    "ack",
    "foo",
    "firefox",
    "git",
    "memoize", "memoizes",
    "Zulip",
    "recurs", "recurse", "recurses",
    "Datalog", "Datafun",
    "lag", "laggy",
    "pluralizable",
    "dev",
    "misc",
    "seminaive",
    "anime",
    "comonad", "modal", "coeffect", "ringoid", "ringoids",
    "poset",
    "arg", "args",
    "org", "orgs",
    "misrecognition", "misrecognitions",
]

# only include pluralizable nouns here
proper_nouns = [
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday",
    "January", "February", "April", "June", "July", "August", "September", "October", "November", "December",
]
simple_vocabulary.extend(proper_nouns + [x+"s" for x in proper_nouns])

mapping_vocabulary = {
    "i": "I",
    "i'm": "I'm",
    "i've": "I've",
    "i'll": "I'll",
    "i'd": "I'd",
    "shemacs": "emacs", "shemax": "emacs",
    "recurse center": "Recurse Center", "recur center": "Recurse Center", "r c": "RC",
    "to morrow": "tomorrow", "to day": "today",
    "underdocumented": "under-documented",
    "cel": "cell",
    "roten": "rotten",
    "r s i": "RSI", "rs si": "RSI",
    "lambda": "lambda", "lamba": "lambda", "lamda": "lambda",
    "my nick": "rntz",
    "miss recognition": "misrecognition", "miss recognitions": "misrecognitions",
}

mapping_vocabulary.update(dict(zip(simple_vocabulary, simple_vocabulary)))

mod = Module()


@mod.capture(rule="({user.vocabulary})")
def vocabulary(m) -> str:
    return m.vocabulary


@mod.capture(rule="(<user.vocabulary> | <word>)")
def word(m) -> str:
    try:
        return m.vocabulary
    except AttributeError:
        return actions.dictate.parse_words(m.word)[-1]


punctuation = set(".,-!?;:")


@mod.capture(rule="(<user.vocabulary> | <phrase>)+")
def text(m) -> str:
    words = []
    result = ""
    for item in m:
        # print(m)
        if isinstance(item, grammar.vm.Phrase):
            words = words + actions.dictate.replace_words(
                actions.dictate.parse_words(item)
            )
        else:
            words = words + item.split(" ")

    for i, word in enumerate(words):
        if i > 0 and word not in punctuation and words[i - 1][-1] not in ("/-("):
            result += " "

        result += word
    return result


mod.list("vocabulary", desc="user vocabulary")

ctx = Context()

# setup the word map too
ctx.settings["dictate.word_map"] = mapping_vocabulary
ctx.lists["user.vocabulary"] = mapping_vocabulary

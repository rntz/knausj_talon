from talon import imgui, Module, speech_system, actions

hist_len = 50
hist_short_len = 4
hist_more = False
history = []


def parse_phrase(word_list):
    return " ".join(word.split("\\")[0] for word in word_list)


def on_phrase(j):
    global hist_len
    global history

    try:
        val = parse_phrase(getattr(j["parsed"], "_unmapped", j["phrase"]))
    except:
        val = parse_phrase(j["phrase"])

    if val != "":
        history.append(val)
        history = history[-hist_len:]

        if gui.showing:
            gui.freeze()
   
#todo: dynamic rect?
@imgui.open(x=1200,y=0,software=False)
def gui(gui: imgui.GUI):
    global history
    #gui.text("Command History")
    #gui.line()
    text = history[:] if hist_more else history[-hist_short_len:]
    for line in text:
        gui.text(line)


speech_system.register("phrase", on_phrase)

mod = Module()


@mod.action_class
class Actions:
    def history_enable():
        """Enables the history"""
        gui.show()

    def history_disable():
        """Disables the history"""
        gui.hide()

    def history_clear():
        """Clear the history"""
        global history
        history = []

    def history_more():
        """Show more history"""
        global hist_more
        hist_more = True

    def history_less():
        """Show less history"""
        global hist_more
        hist_more = False

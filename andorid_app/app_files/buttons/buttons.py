from kivymd.uix.button import MDRaisedButton


class wrong_credentails_button(MDRaisedButton):
    def __int__(self,root,triggerFunction=None):
        self.root = root
        self.triggerFunction = triggerFunction

    def on_press(self):
        for widget in self.root.children:
            widget.disabled = False
        self.root.remove_widget(self)
        if self.triggerFunction != None:
            self.triggerFunction()

    def disable_other_widgets(self):
        for widget in self.root.children:
            widget.disabled = True

from kivymd.uix.button import MDIconButton
from kivy.app import App
from kivy.properties import (
    AliasProperty,
    BooleanProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    StringProperty,
)

class MDIconButtonTwoPosition(MDIconButton):
    enabled = True
    sourceEnabled = StringProperty()
    sourceDisabled = StringProperty()
    triggerFunction = ObjectProperty()
    arguments = ObjectProperty()

    def on_release(self):
        if self.enabled == True:
            self.enabled = False
        else:
            self.enabled = True

        self.change_source()

        if self.triggerFunction != None:
            self.triggerFunction(self.arguments,self.enabled)

    def change_source(self):
        if self.enabled == True:
            self.icon = self.sourceEnabled
        else:
            self.icon = self.sourceDisabled
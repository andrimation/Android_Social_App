from kivymd.uix.dialog import MDDialog
from kivy.properties import (
    AliasProperty,
    BooleanProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    StringProperty,
)
class MDDialogMod(MDDialog):
    imageId = StringProperty()

    def on_touch_down(self, touch):
        pass


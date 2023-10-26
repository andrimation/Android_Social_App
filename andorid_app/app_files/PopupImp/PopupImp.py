from kivy.uix.popup import Popup
from kivy.properties import (
    AliasProperty,
    BooleanProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    StringProperty,
)
class PopupImp(Popup):
    id = StringProperty()

    def add_widget(self, widget, *args, **kwargs):
        super(Popup, self).add_widget(widget, *args, **kwargs)
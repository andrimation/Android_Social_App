from kivymd.uix.button import MDFloatingActionButton
from kivy.app import App
from kivy.properties import (
    AliasProperty,
    BooleanProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    StringProperty,
)

class MDFloatingActionButtonImage(MDFloatingActionButton):
    imageId = StringProperty()
    def on_release(self):
        App.get_running_app().root.get_screen("PhotosGalleryScreen").display_delete_image_dialog(self.imageId)

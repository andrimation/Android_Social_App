from kivymd.uix.imagelist import MDSmartTile
from kivy.properties import (
    AliasProperty,
    BooleanProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    StringProperty,
    DictProperty,
)
from kivy.app import App

class SmartTileWithLabelImp(MDSmartTile):
    imageId = StringProperty()
    imageComment = StringProperty()
    imageAdress = StringProperty()

    def on_release(self):
        if self.imageAdress:
            App.get_running_app().root.get_screen("PhotosGalleryScreen").display_full_image(self.imageComment,self.imageAdress,self.imageId)
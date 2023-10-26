from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image,AsyncImage


class AsyncImageButton(ButtonBehavior,AsyncImage):
    pass

class ImageButton(ButtonBehavior,Image):
    pass
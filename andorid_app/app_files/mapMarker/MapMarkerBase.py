# coding=utf-8

__all__ = ["MapView", "MapMarker", "MapMarkerPopup", "MapLayer", "MarkerMapLayer"]

import webbrowser
from itertools import takewhile
from math import ceil
from os.path import dirname, join

from kivy.clock import Clock
from kivy.compat import string_types
from kivy.graphics import Canvas, Color, Rectangle
from kivy.graphics.transformation import Matrix
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import (
    AliasProperty,
    BooleanProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    StringProperty,
)
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image,AsyncImage
from kivy.uix.label import Label
from kivy.uix.scatter import Scatter
from kivy.uix.widget import Widget

from kivy_garden.mapview import Bbox, Coordinate
from kivy_garden.mapview.constants import (
    CACHE_DIR,
    MAX_LATITUDE,
    MAX_LONGITUDE,
    MIN_LATITUDE,
    MIN_LONGITUDE,
)
from kivy_garden.mapview.source import MapSource
from kivy_garden.mapview.utils import clamp

Builder.load_string(
    """
<MapMarker>:
    size_hint: None, None
    source: root.source
    size: 120,120
    allow_stretch: True
    Label:
        size: 500,500
        text: "kakdkfj"

<MapView>:
    canvas.before:
        StencilPush
        Rectangle:
            pos: self.pos
            size: self.size
        StencilUse
        Color:
            rgba: self.background_color
        Rectangle:
            pos: self.pos
            size: self.size
    canvas.after:
        StencilUnUse
        Rectangle:
            pos: self.pos
            size: self.size
        StencilPop

    ClickableLabel:
        text: root.map_source.attribution if hasattr(root.map_source, "attribution") else ""
        size_hint: None, None
        size: self.texture_size[0] + sp(8), self.texture_size[1] + sp(4)
        font_size: "10sp"
        right: [root.right, self.center][0]
        color: 0, 0, 0, 1
        markup: True
        canvas.before:
            Color:
                rgba: .8, .8, .8, .8
            Rectangle:
                pos: self.pos
                size: self.size


<MapViewScatter>:
    auto_bring_to_front: False
    do_rotation: False
    scale_min: 0.2
    scale_max: 3.

<MapMarkerPopup>:
    RelativeLayout:
        id: placeholder
        y: root.top
        center_x: root.center_x
        size: root.popup_size

"""
)



class MapMarker(ButtonBehavior, Image):
    """A marker on a map, that must be used on a :class:`MapMarker`
    """

    anchor_x = NumericProperty(0.5)
    """Anchor of the marker on the X axis. Defaults to 0.5, mean the anchor will
    be at the X center of the image.
    """

    anchor_y = NumericProperty(0)
    """Anchor of the marker on the Y axis. Defaults to 0, mean the anchor will
    be at the Y bottom of the image.
    """

    lat = NumericProperty(0)
    """Latitude of the marker
    """

    lon = NumericProperty(0)
    """Longitude of the marker
    """

    source = StringProperty(join(dirname(__file__), "icons", "marker.png"))
    """Source of the marker, defaults to our own marker.png
    """

    # (internal) reference to its layer
    _layer = None

    def __init__(self, **kwargs):
        super(MapMarker, self).__init__(**kwargs)
        self.texture_update()
        self.allow_stretch = False

    def detach(self):
        if self._layer:
            self._layer.remove_widget(self)
            self._layer = None

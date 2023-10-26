from kivy_garden.mapview import MapMarkerPopup,MapMarker,MapView,MapLayer,MapSource,MarkerMapLayer
from kivy.properties import (
    AliasProperty,
    BooleanProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    StringProperty,
    DictProperty,
)
from kivy.clock import mainthread

class MapViewBackground(MapView):
    root_property = ObjectProperty()
    def on_touch_down(self, touch):
        pass

    def on_touch_up(self, touch):
        pass


    def on_zoom(self, instance, zoom):
        if zoom == self._zoom:
            return
        x = self.map_source.get_x(zoom, self.lon) - self.delta_x
        y = self.map_source.get_y(zoom, self.lat) - self.delta_y
        self.set_zoom_at(zoom, x, y)
        self.center_on(self.lat, self.lon)
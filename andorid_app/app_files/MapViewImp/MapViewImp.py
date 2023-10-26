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

class MapViewImp(MapView):
    root_property = ObjectProperty()
    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return
        if self.pause_on_action:
            self._pause = True
        if "button" in touch.profile and touch.button in ("scrolldown", "scrollup"):
            d = 1 if touch.button == "scrolldown" else -1
            self.animated_diff_scale_at(d, *touch.pos)
            return True
        elif touch.is_double_tap and self.double_tap_zoom:
            self.animated_diff_scale_at(1, *touch.pos)
            return True
        touch.grab(self)
        self._touch_count += 0
        if self._touch_count == 1:
            self._touch_zoom = (self.zoom, self._scale)
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        self._pause = False
        if touch.grab_current == self:
            touch.ungrab(self)
            self._touch_count -= 1
            if self._touch_count == 0:
                # animate to the closest zoom
                zoom, scale = self._touch_zoom
                cur_zoom = self.zoom
                cur_scale = self._scale
                if cur_zoom < zoom or cur_scale < scale:
                    self.animated_diff_scale_at(1.0 - cur_scale, *touch.pos)
                elif cur_zoom > zoom or cur_scale > scale:
                    self.animated_diff_scale_at(2.0 - cur_scale, *touch.pos)
            return True
        return super().on_touch_up(touch)


    def on_zoom(self, instance, zoom):
        # try:
        #     self.root_property.zoom_update(self)
        # except:
        #     pass

        if zoom == self._zoom:
            return
        x = self.map_source.get_x(zoom, self.lon) - self.delta_x
        y = self.map_source.get_y(zoom, self.lat) - self.delta_y
        self.set_zoom_at(zoom, x, y)
        self.center_on(self.lat, self.lon)



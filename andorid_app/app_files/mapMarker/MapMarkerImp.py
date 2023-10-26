from kivy_garden.mapview import MapMarkerPopup,MapMarker
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivymd.uix.dialog import MDDialog
from kivy.properties import (
    AliasProperty,
    BooleanProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    StringProperty,
)
from kivy.uix.scrollview import ScrollView
from kivy.app import App
import requests
from kivy.input.motionevent import MotionEvent
from kivy.animation import Animation
# from .MapMarkerBase import MapMarker

class Test(Widget):
    pass


class MDDialogImp(MDDialog):

    def on_touch_move(self, touch):
        self.dismiss()


class MapMarkerImp(MapMarkerPopup):
    popup_size = ListProperty([1, 1])
    root = None
    header = None
    server_adress = None
    type = StringProperty()
    id = None
    user = None
    post = None
    unified_post_data = None
    MAIN_MAP = None
    onlyUser = False
    usersList = ListProperty()
    postsList = ListProperty()

    markerMapClusterNum = 0
    markerMapGroupNum = 0


    def unify_data(self):
        self.unified_post_data = {"lat": self.lat, "lon": self.lon, "id": self.id, "action": "get_specific_post","alarmPost":self.post["alarmPost"]}

    def open_dialog(self):

        sources = ["user.png", "work.png", "home.png","work_2.png"]
        if self.source not in sources:
            # if self.MAIN_MAP.zoom < 19:
            App.get_running_app().root.get_screen("MainScreen").map_marker_collision(self)
                # App.get_running_app().root.get_screen("MainScreen").choose_users_or_posts(self)

            # elif self.MAIN_MAP.zoom >=19:
            #     App.get_running_app().root.get_screen("MainScreen").map_marker_collision(self)

    def animate_marker(self):
        animation = Animation(opacity=0.5,duration=1.5)
        animation.bind(on_complete=self.reset_animation)
        animation.start(self)

    def reset_animation(self,*args):
        self.opacity = 0.9
        self.animate_marker()

    def nothing(self):
        pass

    def find_touch_size(self):
        try:
            if self.MAIN_MAP.zoom <= 13:
                touchSize =  500
            elif self.MAIN_MAP.zoom > 13 and self.MAIN_MAP.zoom <= 15:
                touchSize =  40
            elif self.MAIN_MAP.zoom == 16 or self.MAIN_MAP.zoom == 17:
                touchSize =  35
            elif self.MAIN_MAP.zoom >= 18:
                touchSize =  25
            # elif self.MAIN_MAP.zoom >= 19:
            #     touchSize = 35
            touchSize = self.size[0]
            return touchSize
        except:
            return 5

    def on_touch_down(self, touch):
        if self.source not in ["user.png","work.png","home.png","work_2.png"]:
            if App.get_running_app().root.get_screen("MainScreen").dialog_opened == False:
                if self.MAIN_MAP != None:
                    self.MAIN_MAP.do_update(1)
                # USTAWIĆ SZEROKOŚĆ TOUCHA W ZALEŻNOŚCI OD ZOOMU !
                touchSize = self.size[0]
                if App.get_running_app().root.get_screen("MainScreen").marker_in_use == None:
                    if touch.x < (self.x + touchSize) and touch.x > (self.x) and touch.y < (self.y + touchSize) and touch.y > (self.y):
                        App.get_running_app().root.get_screen("MainScreen").marker_in_use = self
                        App.get_running_app().root.get_screen("MainScreen").touchList = [touch.x, touch.y]

    def on_touch_up(self, touch):
        # Jest Akceptowalnie -
        touchX,touchY = App.get_running_app().root.get_screen("MainScreen").touchList
        touchSize = self.find_touch_size()
        if App.get_running_app().root.get_screen("MainScreen").marker_in_use == self:
            if touch.x < (touchX + touchSize) and touch.x > (touchX - touchSize) and touch.y < (touchY + touchSize) and touch.y > (touchY - touchSize):
                self.open_dialog()
                self.reset_map_markers_variables()
            else:
                self.reset_map_markers_variables()

    def reset_map_markers_variables(self):
        App.get_running_app().root.get_screen("MainScreen").marker_in_use = None
        App.get_running_app().root.get_screen("MainScreen").touchList = [0, 0]


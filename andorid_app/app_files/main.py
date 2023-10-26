from kivy.metrics import dp, sp
from PIL import Image, ImageOps, ImageDraw
import datetime
import threading
from kivy.lang import Builder
from plyer import gps
from kivy.app import App
from kivy.properties import StringProperty
from kivy.clock import mainthread
from kivy.utils import platform
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy_garden.mapview import MapMarkerPopup, MapLayer
from mapMarker.MapMarkerImp import MapMarkerImp
from plyer import gps
from kivy.uix.scrollview import ScrollView
from kivy.properties import (
    AliasProperty,
    BooleanProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    StringProperty,
    DictProperty,
)
from kivymd.uix.imagelist import MDSmartTile
from SmartTileWithLabelImp.SmartTileWithLabelImp import SmartTileWithLabelImp
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from buttons.buttons import wrong_credentails_button
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineAvatarListItem, OneLineAvatarIconListItem, OneLineIconListItem, \
    TwoLineAvatarIconListItem, ThreeLineAvatarIconListItem
from kivymd.uix.filemanager import MDFileManager
from kivy.uix.popup import Popup
from kivy.uix.image import AsyncImage
from kivy.animation import Animation
from  kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.toolbar import MDTopAppBar
from PopupImp.PopupImp import PopupImp
from kivymd.uix.label import MDLabel
from ImageButton.ImageButton import AsyncImageButton, ImageButton
from kivymd.uix.gridlayout import GridLayout,MDGridLayout
from kivymd.uix.stacklayout import StackLayout,MDAdaptiveWidget
from kivy.uix.image import Image as kivyImage
import datetime
import requests
import time
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivymd.uix.button import MDIconButton, MDRoundFlatButton, MDFillRoundFlatButton, MDRoundFlatIconButton, \
    MDFillRoundFlatIconButton
from kivymd.uix.progressbar import MDProgressBar
from kivy.config import Config
from MDFloatingActionButtonImage.MDFloatingActionButtonImage import MDFloatingActionButtonImage, MDFloatingActionButton
from MDIconButtonTwoPosition.MDIconButtonTwoPosition import MDIconButtonTwoPosition
import os
from kivymd.uix.card import MDCard
from MDTextFieldMessageBubble.MDTextFieldMessageBubble import MDTextFieldMessageBubble, MDTextFieldInput
from MapViewImp.MapViewImp import MapViewImp
import certifi
import os, sys, plyer

# This needs to be here to display the manga images on Android


# Fixing asyncImage loading ( hopefully )
os.environ['KIVY_IMAGE'] = 'pil,sdl2'
os.environ['SSL_CERT_FILE'] = certifi.where()
import requests

requests.packages.urllib3.disable_warnings()

import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

# Enable do kompilacji
primary_ext_storage = "/"
Window.size = (720 / 2, 1280 / 2)
# from android.storage import primary_external_storage_path

# primary_ext_storage = primary_external_storage_path()

# SERWER_ADRESS = "http://127.0.0.1:8000/"
#
# -> dla emulatora android !
# SERWER_ADRESS = "http://10.0.2.2:8000/"

SERWER_ADRESS = "http://afternoon-headland-3098991.herokuapp.com/"

Window.keyboard_anim_args = {"d": .2, "t": "in_out_expo"}
Window.softinput_mode = "below_target"

# Config.set('modules', 'monitor', '')

###
USERNAME = ""
USERMARKER = None
HOMEMARKER = None
WORKMARKER = None
LOGIN = False
###

TOKEN = ""
HEADER = ""

user_LAT = "53.42320"
user_LON = "14.52090"

home_LAT = "0.0"
home_LON = "0.0"

work_LAT = "0.0"
work_LON = "0.0"
########
USERS_IN_DISTANCE = []
POSTS_IN_DISTANCE = []
########
FRIENDS_ONLY = False
DISTANCE = 200
UPDATE_ALL_DATA_THREAD = []
USER_MARKER_THREAD_LIST = []
NEW_MESSAGES_THREAD = []
UPDATE_USER_ONLY = []

CURRENT_USER_DATA = ""
CURRENT_KMEANS_DATA = ""
CURRENT_KMEANS_DATA_SPLIT = {"user": "", "home": "", "work": ""}
ALARM_POSTS = ""

UPDATE_ENABLED = True

######
MAIN_MAP = None

ALL_USERS_CONTAINER = {}
ALL_POSTS_CONTAINER = {}

DICT_OF_ZOOM_POINTS_POSITIONS = {}

setattr(MapMarkerPopup, "name", "")
setattr(MDFillRoundFlatIconButton, "userData", "")
UPDATE_ALL_PROGRAM_DATA_THREAD = None
UPDATE_USER_MARKER_THREAD = None
CHECK_IF_NEW_MESSAGES_ALERT = None
UPDATE_MARKERS = None

FIRST_UPDATE = False

from kivy.clock import _default_time as kivy_time


class LoginScreen(Screen):
    firstLogin = True
    first_click = True

    login_data = None

    def on_enter(self, *args):
        if self.firstLogin == False:
            self.create_animation()

        self.firstLogin = False

    def create_animation(self):
        self.animation = Clock.schedule_interval(self.animate_background, 0.07)

    def animate_background(self, dt=0):
        map = self.ids["MainMap"]
        map.center_on(map.lat, map.lon + 0.00003)

        self.ids["MainMap"].do_update(1)
        self.check_login_data()

    def check_login_data(self):
        global TOKEN, HEADER, USERNAME, CURRENT_USER_DATA
        if self.login_data == None:

            for file in os.listdir():

                if file == "loginData.txt":
                    self.login_data = True

            if self.login_data == True:

                tokenFile = open("loginData.txt", "r")
                token = tokenFile.readline()
                USERNAME = tokenFile.readline()
                TOKEN = token[:-1]
                HEADER = {"Authorization": f"Token {TOKEN}"}

                App.get_running_app().root.get_screen("MainScreen").create_start_board()
                App.get_running_app().root.get_screen("MainScreen").create_main_widgets()

                self.animation.cancel()
                self.login_to_app()

            else:
                self.login_data = False
                self.show_all_widgets()

    def show_all_widgets(self):
        self.ids["MainMap"].opacity = 1
        self.ids["MainLoginCard"].opacity = 0.6
        self.ids["userName"].opacity = 1
        self.ids["userPassword"].opacity = 1
        self.ids["LoginButton"].opacity = 1
        self.ids["LoginButton"].disabled = False
        self.ids["RegisterButton"].opacity = 1
        self.ids["RegisterButton"].disabled = False

    def nothing(self):
        pass

    def on_leave(self, *args):
        self.animation.cancel()

    def nothing(self):
        pass

    def check_credentails(self):
        global USERNAME, CURRENT_USER_DATA

        username = self.ids['userName'].text
        password = self.ids['userPassword'].text
        # self.ids['userName'].text = "andrik"
        # self.ids['userPassword'].text = "osaosa"
        USERNAME = username
        if self.first_click:
            App.get_running_app().root.get_screen("MainScreen").create_start_board()
            App.get_running_app().root.get_screen("MainScreen").create_main_widgets()
            self.first_click = False
        try:
            token = requests.post(SERWER_ADRESS + "api_login/", data={'username': username, 'password': password})
        except:
            self.answer_button(" No answer from serwer ")
            return

        try:
            global TOKEN, HEADER
            TOKEN = token.json()['token']
            HEADER = {"Authorization": f"Token {TOKEN}"}

            saveLogin = open("loginData.txt", "w")
            data = f"{TOKEN}\n{USERNAME}"
            saveLogin.write(data)
            saveLogin.close()

            self.login_to_app()
        except:
            self.answer_button(" Try again !")
            return

    def answer_button(self, button_text, triggerFunction=None, otherSelf=None):
        wrongLogin = wrong_credentails_button()
        if otherSelf == None:
            wrongLogin.root = self
        else:
            wrongLogin.root = otherSelf
        wrongLogin.triggerFunction = triggerFunction
        wrongLogin.text = button_text
        wrongLogin.size_hint = (0.6, 0.1)
        wrongLogin.pos_hint = {"center_x": 0.5, "center_y": 0.50}
        wrongLogin.disable_other_widgets()
        wrongLogin.root.add_widget(wrongLogin)

    def register_user(self):
        self.ids["userName"].text = ""
        self.ids["userPassword"].text = ""
        self.manager.current = "RegisterScreen"

    def login_to_app(self):
        global CURRENT_USER_DATA
        App.get_running_app().root.get_screen("MainScreen").start_board_show()
        self.manager.current = "MainScreen"


class RegisterScreen(Screen):
    firstLogin = True
    first_pre_enter = True

    def on_pre_enter(self, *args):
        if self.first_pre_enter:
            self.create_screen_widgets()
            self.first_pre_enter = False

    def on_enter(self, *args):
        self.create_animation()
        self.firstLogin = False

    def create_screen_widgets(self):
        map = MapViewImp(lat=53.428, lon=14.527, zoom=15, double_tap_zoom=True, root_property=self,
                         on_zoom=lambda x: self.nothing(),
                         on_touch_down=lambda x: self.nothing(), pause_on_action=False)
        mdCard = MDCard(size_hint=(0.95, 0.95), pos_hint={"center_x": 0.5, "center_y": 0.5}, padding=25,
                        spacing=25, opacity=0.6)
        userField = MDTextField(hint_text="Login *", size_hint_x=0.7, width=mdCard.width * 0.7,
                                pos_hint={"center_x": 0.5, "center_y": 0.85})
        passwordField = MDTextField(hint_text="Password *", size_hint_x=0.7, width=mdCard.width * 0.7,
                                    pos_hint={"center_x": 0.5, "center_y": 0.75})
        fnameField = MDTextField(hint_text="First name *", size_hint_x=0.7, width=mdCard.width * 0.7,
                                 pos_hint={"center_x": 0.5, "center_y": 0.65})
        snameField = MDTextField(hint_text="Second name *", size_hint_x=0.7, width=mdCard.width * 0.7,
                                 pos_hint={"center_x": 0.5, "center_y": 0.55})
        ageField = MDTextField(hint_text="Age *", size_hint_x=0.7, width=mdCard.width * 0.7,
                               pos_hint={"center_x": 0.5, "center_y": 0.45}, input_filter="int")
        emailField = MDTextField(hint_text="E-mail adress *", size_hint_x=0.7, width=mdCard.width * 0.7,
                                 pos_hint={"center_x": 0.5, "center_y": 0.35})
        phoneField = MDTextField(hint_text="Phone number *", size_hint_x=0.7, width=mdCard.width * 0.7,
                                 pos_hint={"center_x": 0.5, "center_y": 0.25}, input_filter="int")
        registerButton = MDFillRoundFlatButton(size_hint_x=None, size_hint_y=0.07, width=mdCard.width * 0.6,
                                               text="Register", pos_hint={"center_x": 0.5, "center_y": 0.16},
                                               md_bg_color=(0.2, 0.5, 1), on_press=lambda x=1: self.register_new_user())
        backButton = MDIconButton(icon="arrow-left-thick", pos_hint={"x": 0.03, "y": 0.03},
                                  on_release=lambda x: self.back_to_login())

        self.add_widget(map)
        self.add_widget(mdCard)
        self.add_widget(userField)
        self.add_widget(passwordField)
        self.add_widget(fnameField)
        self.add_widget(snameField)
        self.add_widget(ageField)
        self.add_widget(emailField)
        self.add_widget(phoneField)
        self.add_widget(registerButton)
        self.add_widget(backButton)

        self.ids["BackgroundMap"] = map
        self.ids["MainLoginCard"] = mdCard
        self.ids["username"] = userField
        self.ids["user_password"] = passwordField
        self.ids["first_name"] = fnameField
        self.ids["second_name"] = snameField
        self.ids["age"] = ageField
        self.ids["email"] = emailField
        self.ids["phone"] = phoneField
        self.ids["RegisterButton"] = registerButton
        self.ids["BackToMainScreen"] = backButton

    def create_animation(self):
        self.animation = Clock.schedule_interval(self.animate_background, 0.07)

    def animate_background(self, dt=0):

        map = self.ids["BackgroundMap"]
        map.center_on(map.lat, map.lon + 0.00003)

        self.ids["BackgroundMap"].do_update(1)

    def nothing(self):
        pass

    def register_new_user(self, x=0):
        ids = self.ids

        username = self.ids["username"].text
        password = self.ids["user_password"].text
        first_name = self.ids["first_name"].text
        second_name = self.ids["second_name"].text
        age = self.ids["age"].text
        email = self.ids["email"].text
        phone = self.ids["phone"].text
        for field in [username, password, first_name, second_name, age, email]:
            if field == "" or field == " ":
                answer = "Fill all fields with '*' !"
                self.display_register_answer_dialog(answer)
                return
        if email.count("@") == 0:
            answer = "Please type correct email"
            self.display_register_answer_dialog(answer)
            return

        try:
            registerResponse = requests.post(SERWER_ADRESS + "api_new_user/",
                                             data={'username': username, 'password': password, "first_name": first_name,
                                                   "second_name": second_name, "age": age, "email": email,
                                                   "phone": phone})
            if registerResponse.status_code != 201:
                self.dialog = MDDialog(text=f" Name  '{username}'  is in use! ",
                                       buttons=[MDIconButton(icon="check", on_release=lambda x: self.dialog.dismiss())])
                self.dialog.open()

            else:
                App.get_running_app().root.get_screen("LoginScreen").ids['userName'].text = username
                App.get_running_app().root.get_screen("LoginScreen").ids['userPassword'].text = password
                self.dialog = MDDialog(text=f" '{username}' account created !",
                                       buttons=[MDIconButton(icon="check", on_release=lambda x: self.dialog.dismiss())])
                self.dialog.open()
                self.back_to_login()






        except:
            answer = "Something went wrong :("
            App.get_running_app().root.get_screen("Login").answer_button(answer, otherSelf=self)

    def back_to_login(self):
        self.manager.current = "Login"

        # PAmiętać o FIRST LOGIN !! - > nie potrrzeba
        # self.firstLogin = True

    def display_register_answer_dialog(self, answer):
        registerAnswerDialog = MDDialog(
            text=answer,
            buttons=[MDIconButton(icon="check-outline", on_release=lambda x: registerAnswerDialog.dismiss())]
        )
        registerAnswerDialog.open()

    def back_to_login(self):
        for key in self.ids.keys():
            if key != "RegisterButton":
                try:
                    self.ids[key].text = ""
                except:
                    pass

        self.manager.current = "LoginScreen"

    def on_leave(self, *args):
        self.animation.cancel()


class MainScreen(Screen):
    firstEnter = True
    touchList = [0, 0]
    marker_in_use = None

    markers_on_map = []

    notifications = BooleanProperty(defaultvalue=False)
    all_users_dialog_lenght = 10
    zoomUpdate = True
    Displayed_Map_Button = False
    previewDialogListStatus = [0, 8]
    pauseMarkers = False
    dialog_opened = False

    def create_main_widgets(self):
        # md_bg_color = (0.44, 0.77, 1, 1)
        mainMap = MapViewImp(lat=53.448, lon=14.537, zoom=12, double_tap_zoom=True,
                             root_property=self, pause_on_action=True)
        topToolbar = MDTopAppBar(pos_hint={"top": 1}, opacity=0.8)
        topToolbar.right_action_items = [
            ["account-circle", lambda x: self.show_my_profile(), "My Profile", "My Profile"]]
        bottomToolbar = MDTopAppBar(opacity=0.8)
        messagesButton = ["message-outline", lambda x: self.display_all_messages_threads()]
        bottomToolbar.left_action_items = [["dots-vertical", lambda x: self.open_menu(), "Open menu"],
                                           ["bell-ring-outline", lambda x: self.show_notifications_dialog(),
                                            "Pokaż powiadomienia", "Pokaż powiadomienia"], messagesButton
                                           ]
        bottomToolbar.right_action_items = [
            ["account-group", lambda x: self.show_allUsers_dialog(type="user"), "Preview all users",
             "Preview all users"],
            ["message-question-outline", lambda x: self.show_allUsers_dialog(type="post"), "Preview all posts",
             "Preview all posts"],
            ["message-plus-outline", lambda x: self.create_post(), "Create post", "Create post"]]

        findUserButton = MDFloatingActionButton(icon="crosshairs-gps", pos_hint={"top": 0.2, "right": 0.97},
                                                opacity=0.8, on_release=lambda x=1: self.show_user_marker())

        self.add_widget(mainMap)
        self.ids["MainMap"] = mainMap
        self.add_widget(topToolbar)
        self.add_widget(bottomToolbar)
        self.ids["topToolbar"] = topToolbar
        self.ids["bottomToolbar"] = bottomToolbar
        self.ids["messagesButton"] = messagesButton
        self.add_widget(findUserButton)

    def create_start_board(self):
        self.startBoard = Popup(background_color=[0, 0, 0, 0], title="",
                                separator_color=[0.2, 0.5, 1, 0])
        small_Popup = Popup(background_color=[0, 0, 0, 0], title="",
                            separator_color=[0.2, 0.5, 1, 0], size_hint_y=0.1, pos_hint={"top": 0.5})
        self.startBoard.add_widget(small_Popup)
        self.startBoard.ids["small_popup"] = small_Popup

    def start_board_show(self):
        if self.firstEnter:
            self.startBoard.open()
            progressBar = MDProgressBar(pos_hint={"right": 0, "top": 1})
            self.upgradeProgressObj = Clock.schedule_interval(self.upgradeProgress, 0.05)
            self.startBoard.ids["small_popup"].add_widget(progressBar)
            self.startBoard.ids["progress_bar"] = progressBar

    def upgradeProgress(self, dt=0):
        self.startBoard.ids["progress_bar"].value += 10

    def on_enter(self, *args):
        global USERNAME, USERMARKER, LOGIN, MAIN_MAP, SERWER_ADRESS, WORKMARKER, HOMEMARKER, DISTANCE, UPDATE_ENABLED
        UPDATE_ENABLED = True
        self.topToolbar = self.ids["topToolbar"]
        self.bottomToolbar = self.ids["bottomToolbar"]
        self.distance = DISTANCE

        # MainApp.start(10,1)
        if self.firstEnter:
            userMarker = MapMarkerImp(on_press=lambda x: userMarker.nothing())
            userMarker.name = USERNAME
            userMarker.type = "user"
            userMarker.source = 'user.png'
            userMarker.lat = user_LAT
            userMarker.lon = user_LON
            userMarker.size = (100, 100)
            MAIN_MAP = self.ids['MainMap']
            MAIN_MAP.add_widget(userMarker)
            LOGIN = True
            USERMARKER = userMarker
            # USERMARKER.animate_marker()

            homeMarker = MapMarkerImp(on_press=lambda x: workMarker.nothing(), type="home", source="home.png",
                                      opacity=0, popup_size=(60, 60))
            HOMEMARKER = homeMarker
            HOMEMARKER.size = (100, 100)
            MAIN_MAP.add_marker(homeMarker)
            MAIN_MAP.root_property = self

            workMarker = MapMarkerImp(on_press=lambda x: workMarker.nothing(), type="work", source="work_2.png",
                                      opacity=0, size=(100, 100))
            WORKMARKER = workMarker
            WORKMARKER.size = (100, 100)
            MAIN_MAP.add_marker(workMarker)
            threadHomeWorkAsk = threading.Thread(target=self.first_ask_for_home_work)
            threadHomeWorkAsk.start()
            App.get_running_app().update_all_data()
            # App.get_running_app().update_all_program_data_thread()
            self.create_app_widgets()

            self.zoom_update(MAIN_MAP)
            self.firstEnter = False
            self.checkDataStatus = Clock.schedule_interval(self.check_if_data_downloaded, 0.2)
            MAIN_MAP.zoom += 1
            MAIN_MAP.zoom -= 1

    def on_leave(self, *args):
        global UPDATE_ENABLED
        UPDATE_ENABLED = False

    def create_app_widgets(self):
        App.get_running_app().root.get_screen("MainScreen").create_Menu()
        App.get_running_app().root.get_screen("MainScreen").create_allUsers_dialog()
        App.get_running_app().root.get_screen("MainScreen").create_choose_user_post_dialog()
        App.get_running_app().root.get_screen("MainScreen").create_set_distance_dialog()
        App.get_running_app().root.get_screen("MainScreen").create_friends_only_dialog()
        App.get_running_app().root.get_screen("MainScreen").create_accept_or_deny_request_dialog()
        App.get_running_app().root.get_screen("CurrentThreadMessagesScreen").create_text_widgets_in_lists()
        App.get_running_app().root.get_screen("CurrentThreadMessagesScreen").create_download_full_conv_dialog()
        App.get_running_app().root.get_screen("CurrentThreadMessagesScreen").create_FileManager()
        App.get_running_app().root.get_screen("CurrentThreadMessagesScreen").create_image_popup()
        App.get_running_app().root.get_screen("CurrentThreadMessagesScreen").create_ask_image_add_dialog()
        App.get_running_app().root.get_screen("CurrentThreadMessagesScreen").create_start_board()
        App.get_running_app().root.get_screen("PostScreen").create_post_text_bubble()
        App.get_running_app().root.get_screen("PostScreen").create_text_input()
        App.get_running_app().root.get_screen("PostScreen").create_owner_menu()
        App.get_running_app().root.get_screen("PostScreen").create_image_dialog()
        App.get_running_app().root.get_screen("PostScreen").create_start_board()
        App.get_running_app().root.get_screen("CreatePostScreen").create_alertDialog()
        App.get_running_app().root.get_screen("CreatePostScreen").create_alertEndDialog()
        App.get_running_app().root.get_screen("CreatePostScreen").create_set_post_time_dialog()
        App.get_running_app().root.get_screen("CreatePostScreen").create_start_board()
        App.get_running_app().root.get_screen("UserScreen").create_start_board()

    def check_if_data_downloaded(self, dt=0):
        global CURRENT_USER_DATA, MAIN_MAP
        if FIRST_UPDATE == False:
            pass
        else:
            self.startBoard.ids["progress_bar"].value = 100
            self.checkDataStatus.cancel()
            self.upgradeProgressObj.cancel()
            self.startBoard.dismiss()
            self.zoom_update(MAIN_MAP)
            self.get_profile_photo()

    def get_profile_photo(self):
        if f"profile_crop_{CURRENT_USER_DATA['id']}.png" not in os.listdir("profile_mini/"):
            if CURRENT_USER_DATA["profilePhotoMini"] != None:
                url = CURRENT_USER_DATA["profilePhotoMini"]
                r = requests.get(url, allow_redirects=True)
                open(f"profile_crop_{CURRENT_USER_DATA['id']}.png", 'wb').write(r.content)


    def first_ask_for_home_work(self):
        global home_LAT, home_LON, work_LAT, work_LON
        data = {"action": "get_home_world_location"}
        request = requests.get(SERWER_ADRESS + "api_geoloc/", data=data, headers=HEADER)
        home_LAT, home_LON = request.json()["home_LAT"], request.json()["home_LON"]
        work_LAT, work_LON = request.json()["work_LAT"], request.json()["work_LON"]

    def show_my_profile(self):
        App.get_running_app().root.get_screen("UserScreen").show_start_board()
        App.get_running_app().root.get_screen("UserScreen").userData = CURRENT_USER_DATA
        self.manager.current = "UserScreen"

    def create_post(self):
        self.manager.current = "CreatePostScreen"

    def create_allUsers_dialog(self):
        self.homeButton = MDIconButtonTwoPosition(icon="home.png", sourceEnabled="home.png",
                                                  sourceDisabled="home_disabled.png",
                                                  triggerFunction=self.execute_exclude_objects,
                                                  )

        self.workButton = MDIconButtonTwoPosition(icon="work.png", sourceEnabled="work.png",
                                                  sourceDisabled="work_disabled.png",
                                                  triggerFunction=self.execute_exclude_objects,
                                                  )

        self.positionButton = MDIconButtonTwoPosition(icon="user.png", sourceEnabled="user.png",
                                                      sourceDisabled="user_disabled.png",
                                                      triggerFunction=self.execute_exclude_objects,
                                                      )
        displayUsersButton = MDFillRoundFlatIconButton(text="Display users on map", icon="map-check-outline",
                                                       on_release=lambda x: self.display_users_from_selected_container(
                                                           self.allUsersDialog.listOfUsers),
                                                       pos_hint={"x": 0.1, "y": -1}, anchor_x="left")

        self.allUsersDialog = MDDialogEdited(
            type="custom",
            content_cls=UsersScrollView(),
            buttons=[self.positionButton,
                     self.homeButton,
                     self.workButton,
                     MDIconButton(icon="close", on_release=lambda x: self.allUsersDialog.dismiss())])

        #
        displayUsersButton.opacity = 0
        displayUsersButton.disabled = True
        self.allUsersDialog.ids["spacer_bottom_box"].add_widget(displayUsersButton)

        self.allUsersDialog.ids["displayUsersButton"] = displayUsersButton
        self.allUsersDialog.ids["positionButton"] = self.positionButton
        self.allUsersDialog.ids["homeButton"] = self.homeButton
        self.allUsersDialog.ids["workButton"] = self.workButton

    def show_allUsers_dialog(self, list_of_users=[], list_of_posts=[], globalUsers=True, globalPosts=True,
                             fromMarker=False, marker=None,
                             remember_position=False, otherSelf=None, friendsList=False, type=None):

        global USERS_IN_DISTANCE, MAIN_MAP, POSTS_IN_DISTANCE
        self.listOfExcludedAreas = []

        if otherSelf != None:
            self = otherSelf
        if type == "user":
            if globalUsers:
                list_of_users = USERS_IN_DISTANCE

            mainList = list_of_users

        elif type == "post":
            if globalPosts:
                list_of_posts = POSTS_IN_DISTANCE

            mainList = list_of_posts

        elif type == "message":
            mainList = CURRENT_USER_DATA["messagesThreads"]

        elif type == "notifications":
            mainList = CURRENT_USER_DATA["friendsRequests"]

        buttonDisabled = False
        buttonOpacity = 1

        if fromMarker == True or globalUsers != True or friendsList == True or type == "message" or type == "notifications":
            buttonDisabled = True
            buttonOpacity = 0

        if type == "user":
            self.allUsersDialog.listOfUsers = mainList
        elif type == "post":
            self.allUsersDialog.listOfPosts = mainList

        self.allUsersDialog.ids[
            "displayUsersButton"].opacity = 1 if fromMarker and MAIN_MAP.zoom >= 18 and self.Displayed_Map_Button == False else 0
        self.allUsersDialog.ids[
            "displayUsersButton"].disabled = False if fromMarker and MAIN_MAP.zoom >= 18 and self.Displayed_Map_Button == False else True

        # self.allUsersDialog.ids[
        #     "displayUsersButton"].opacity = 1 if fromMarker and MAIN_MAP.zoom >= 1 and self.Displayed_Map_Button == False else 0
        # self.allUsersDialog.ids[
        #     "displayUsersButton"].disabled = False if fromMarker and MAIN_MAP.zoom >= 0 and self.Displayed_Map_Button == False else True

        self.allUsersDialog.ids["positionButton"].opacity = buttonOpacity
        self.allUsersDialog.ids["positionButton"].disabled = buttonDisabled
        self.allUsersDialog.ids["homeButton"].opacity = buttonOpacity
        self.allUsersDialog.ids["homeButton"].disabled = buttonDisabled
        self.allUsersDialog.ids["workButton"].opacity = buttonOpacity
        self.allUsersDialog.ids["workButton"].disabled = buttonDisabled

        if fromMarker == False:
            self.allUsersDialog.ids["positionButton"].arguments = ["user", mainList, type]
            self.allUsersDialog.ids["homeButton"].arguments = ["home", mainList, type]
            self.allUsersDialog.ids["workButton"].arguments = ["work", mainList, type]

        self.allUsersDialog.otherSelf = otherSelf

        if self.Displayed_Map_Button:
            mainList = [marker.user if type == "user" else marker.post for marker in mainList]

        if type == "user":
            self.allUsersDialog.title = f"All users in area ({len(mainList)})"
            scrollview = self.allUsersDialog.children[0].children[2].children[0].children[0]

            scrollview.data = [{"text": user["username"],
                                "source": "person.png" if user["profilePhotoMini"] == None else user[
                                    "profilePhotoMini"],
                                "userData": user,
                                "fromMarker": fromMarker,
                                "secondary_text": "Online/Offline",
                                "type": "user"} for user in mainList]

            self.allUsersDialog.ids["displayUsersButton"].on_release = lambda \
                x=1: self.display_users_from_selected_container(self.allUsersDialog.listOfUsers)
            scrollview.refresh_from_data()

        elif type == "post":
            self.allUsersDialog.title = f"All posts in area ({len(mainList)})"
            scrollview = self.allUsersDialog.children[0].children[2].children[0].children[0]
            scrollview.data = [{"text": f"{post['postOwnerName'].title()}",
                                "secondary_text": f"{post['postDate'][:10]} {post['postDate'][11:19]}",
                                "tertiary_text": post["postShort"],
                                "source": "post.png" if post["alarmPost"] == False and post[
                                    "sellPost"] == False else "alarm.png" if post["sellPost"] == False else "money.png",
                                "postData": post,
                                "fromMarker": fromMarker,
                                "type": "post"} for post in mainList]

            self.allUsersDialog.ids["displayUsersButton"].on_release = lambda \
                x=1: self.display_users_from_selected_container(mainList, type="post")
            scrollview.refresh_from_data()

        elif type == "message":
            self.allUsersDialog.title = f"All conversations ({len(mainList)})"
            scrollview = self.allUsersDialog.children[0].children[2].children[0].children[0]
            scrollview.data = [{"text": f"{thread['senderName']}" if thread['senderName'] != CURRENT_USER_DATA[
                "username"] else f"{thread['recieverName']}",
                                "secondary_text": f"{thread['lastMessageDate'][:10]} {thread['lastMessageDate'][11:19]}",
                                "source": "post_unread.png" if thread["is_read"] == False and thread["lastSender"] !=
                                                               CURRENT_USER_DATA["username"] else "post.png",
                                "thread": thread,
                                "type": "message"} for thread in mainList]
            scrollview.refresh_from_data()

        elif type == "notifications":
            self.allUsersDialog.title = f"Notifications ({len(mainList)})"
            scrollview = self.allUsersDialog.children[0].children[2].children[0].children[0]
            scrollview.data = [{"text": f"{notification['requestingUserName']} zaprasza Cię do znajomych.",
                                "source": "personAdd.png",
                                "requestingUserData": notification,
                                "type": "notifications"} for notification in mainList]
            scrollview.refresh_from_data()

        self.allUsersDialog.open()
        self.dialog_opened = True

    def execute_exclude_objects(self, arguments, enabled):
        area = arguments[0]
        listOfPoints = arguments[1]
        type = arguments[2]
        if enabled == False:
            self.listOfExcludedAreas.append(area)
        else:
            try:
                self.listOfExcludedAreas.remove(area)
            except:
                pass

        self.update_preview_dialog("begin", listOfPoints, type)

    def update_preview_dialog(self, side, list_of_users, type, otherSelf=None):
        # Remove items
        if type == "post" or type == "user":
            list_of_users = [user for user in list_of_users if user["locationName"] not in self.listOfExcludedAreas]

        if type == "user":
            self.allUsersDialog.title = f"All users in area ({len(list_of_users)})"
            scrollview = self.allUsersDialog.children[0].children[2].children[0].children[0]
            scrollview.data = [{"text": user["username"],
                                "source": "person.png" if user["profilePhotoMini"] == None else user[
                                    "profilePhotoMini"],
                                "userData": user,
                                "fromMarker": False,
                                "secondary_text": "tu będzie status usera",
                                "type": "user"} for user in list_of_users]
            scrollview.refresh_from_data()
        elif type == "post":
            self.allUsersDialog.title = f"All posts in area ({len(list_of_users)})"
            scrollview = self.allUsersDialog.children[0].children[2].children[0].children[0]
            scrollview.data = [{"text": f"{post['postOwnerName'].title()}",
                                "secondart_text": f"{post['postDate'][:10]} {post['postDate'][11:19]}",
                                "tertiary_text": post["postShort"],
                                "source": "post.png" if post["alarmPost"] == False and post[
                                    "sellPost"] == False else "alarm.png" if post[
                                                                                 "sellPost"] == False else "money.png",
                                "postData": post,
                                "fromMarker": False,
                                "secondary_text": "Online/Offline",
                                "type": "post"} for post in list_of_users]
            scrollview.refresh_from_data()

    def create_choose_user_post_dialog(self):
        self.choose_user_post_dialog = MDDialogEdited(type="simple", items=[
            field_one := users_post_Choose_dialog(source="person.png", text="", usersList=[], marker=None,
                                                  choose="user"),
            field_two := users_post_Choose_dialog(source="post.png", text="", postsList=[], choose="post")
        ])

        self.choose_user_post_dialog.ids["field_one"] = field_one
        self.choose_user_post_dialog.ids["field_two"] = field_two

    def display_choose_user_post_dialog(self, list_of_users, list_of_posts, marker):
        self.passObject = None

        self.choose_user_post_dialog.ids["field_one"].text = f"See users        ({len(list_of_users)})"
        self.choose_user_post_dialog.ids["field_one"].source = f"users_pack.png"
        self.choose_user_post_dialog.ids["field_one"].usersList = list_of_users
        self.choose_user_post_dialog.ids["field_one"].marker = marker
        self.choose_user_post_dialog.ids["field_one"].choose = "user"
        self.choose_user_post_dialog.ids["field_one"].opacity = 1

        self.choose_user_post_dialog.ids["field_two"].text = f"See posts        ({len(list_of_posts)})"
        self.choose_user_post_dialog.ids["field_two"].source = f"posts_pack.png"
        self.choose_user_post_dialog.ids["field_two"].postsList = list_of_posts
        self.choose_user_post_dialog.ids["field_two"].choose = "post"
        self.choose_user_post_dialog.ids["field_two"].opacity = 1

        self.passObject = self.choose_user_post_dialog
        self.choose_user_post_dialog.open()
        self.dialog_opened = True

    def map_marker_collision(self, marker):
        global MAIN_MAP
        try:
            check_collision_result, collision_users, collision_posts = self.check_marker_collision(marker)
            if check_collision_result != None:

                list_of_collision_Containers = check_collision_result

                self.choose_users_or_posts(marker, list_of_collision_Containers, collision_users, collision_posts)

            elif check_collision_result == None:
                self.choose_users_or_posts(marker)
        except:
            pass

    def check_marker_collision(self, marker):
        try:
            list_of_collision_Users = []
            list_of_collision_Posts = []
            list_of_collision_Containers = []
            sources = ["user.png", "work.png", "home.png", "alarm.png", "work_2.png"]

            childNum = 0
            # if self.Displayed_Map_Button == True:
            #     childNum = 1

            for other_marker in MAIN_MAP.children[childNum].children:
                if other_marker == marker or marker.source in sources:
                    continue
                else:
                    if marker.collide_widget(other_marker) and isinstance(other_marker,
                                                                          MapMarkerImp) and other_marker != USERMARKER:
                        list_of_collision_Containers.append(other_marker)

                        if other_marker.type == "post":
                            list_of_collision_Posts.append(other_marker)
                        elif other_marker.type == "user" and other_marker.user["username"] != CURRENT_USER_DATA[
                            "username"]:
                            list_of_collision_Users.append(other_marker)

            if list_of_collision_Containers:
                return list_of_collision_Containers, list_of_collision_Users, list_of_collision_Posts
            else:
                return None, None, None
        except:
            pass

    def choose_users_or_posts(self, marker, list_of_collision_Containers=[], collisionUsers=[], collisionPosts=[]):
        if marker.onlyUser == False:
            if list_of_collision_Containers:
                newListOf_Users = []
                newListOf_Posts = []
                newListOf_Users.extend(CURRENT_KMEANS_DATA[str(marker.markerMapClusterNum)]['all_users_container'][
                                           str(marker.markerMapGroupNum)])
                for collideMarker in list_of_collision_Containers:
                    try:
                        newListOf_Users.extend(
                            CURRENT_KMEANS_DATA[str(collideMarker.markerMapClusterNum)]['all_users_container'][
                                str(collideMarker.markerMapGroupNum)])
                    except:
                        pass

                newListOf_Posts.extend(CURRENT_KMEANS_DATA[str(marker.markerMapClusterNum)]['all_posts_container'][
                                           str(marker.markerMapGroupNum)])
                for collideMarker in list_of_collision_Containers:
                    try:
                        newListOf_Posts.extend(
                            CURRENT_KMEANS_DATA[str(collideMarker.markerMapClusterNum)]['all_posts_container'][
                                str(collideMarker.markerMapGroupNum)])
                    except:
                        pass

                self.display_choose_user_post_dialog(newListOf_Users, newListOf_Posts, marker)

            else:
                self.display_choose_user_post_dialog(
                    CURRENT_KMEANS_DATA[str(marker.markerMapClusterNum)]['all_users_container'][
                        str(marker.markerMapGroupNum)],
                    CURRENT_KMEANS_DATA[str(marker.markerMapClusterNum)]['all_posts_container'][
                        str(marker.markerMapGroupNum)], marker)
        else:
            if collisionUsers or collisionPosts:
                if marker.type == "user":
                    collisionUsers.append(marker)
                elif marker.type == "post":
                    collisionPosts.append(marker)

                self.display_choose_user_post_dialog(collisionUsers, collisionPosts, marker)
            else:
                self.display_user_or_post(marker)

    def display_user_or_post(self, marker):
        if marker.type == "user":
            App.get_running_app().root.get_screen("UserScreen").show_start_board()
            App.get_running_app().root.current = "UserScreen"
            App.get_running_app().root.get_screen("UserScreen").userData = marker.user
            App.get_running_app().root.get_screen("UserScreen").fromMarker = True
            self.marker_in_use = None

        elif marker.type == "post":
            marker.unify_data()
            App.get_running_app().root.get_screen("PostScreen").show_start_board()
            App.get_running_app().root.get_screen("PostScreen").data = marker.unified_post_data
            App.get_running_app().root.get_screen("PostScreen").requestData = marker.unified_post_data
            App.get_running_app().root.get_screen("PostScreen").fromMarker = True
            App.get_running_app().root.current = "PostScreen"
            self.marker_in_use = None

    def show_notifications_dialog(self):
        global CURRENT_USER_DATA
        if CURRENT_USER_DATA:
            self.show_allUsers_dialog(type="notifications")

    def create_accept_or_deny_request_dialog(self):
        itemOne = MenuIconListItem(text="accept", icon="account-check")
        itemTwo = MenuIconListItem(text="deny", icon="account-cancel")
        itemThree = MenuIconListItem(icon="account")
        itemFour = MenuIconListItem(text="later...", icon="account-clock", )
        self.accept_deny_Dialog = MDDialogEdited(
            type="simple",
            items=[itemOne, itemTwo, itemThree, itemFour]
        )

        self.accept_deny_Dialog.ids["itemOne"] = itemOne
        self.accept_deny_Dialog.ids["itemTwo"] = itemTwo
        self.accept_deny_Dialog.ids["itemThree"] = itemThree
        self.accept_deny_Dialog.ids["itemFour"] = itemFour

    def accept_or_deny_friend_request_dialog(self, requestSender):
        self.accept_deny_Dialog.ids["itemOne"].on_release = lambda x=1: self.accept_friends_request(requestSender)
        self.accept_deny_Dialog.ids["itemTwo"].on_release = lambda x=1: self.deny_friends_request(requestSender)
        self.accept_deny_Dialog.ids["itemThree"].on_release = lambda x=1: self.display_user_request(requestSender)
        self.accept_deny_Dialog.ids["itemThree"].text = f"see {requestSender['requestingUserName']}'s profile"
        self.accept_deny_Dialog.ids["itemFour"].on_release = lambda x=1: self.pass_friends_request()

        self.accept_deny_Dialog.text = f"Accept friend request from {requestSender['requestingUserName']}?"
        self.accept_deny_Dialog.open()
        self.dialog_opened = True

    def display_user_request(self, user):
        self.accept_deny_Dialog.dismiss()
        self.allUsersDialog.dismiss()
        self.dialog_opened = False
        App.get_running_app().root.get_screen("UserScreen").show_start_board()
        data = {"action": "get_specific_user", "id": user["requestingUserId"]}
        userData = request = requests.get(SERWER_ADRESS + "api_geoloc/", data=data, headers=HEADER).json()
        App.get_running_app().root.get_screen("UserScreen").userData = userData
        App.get_running_app().root.current = "UserScreen"
        App.get_running_app().root.get_screen("UserScreen").fromMarker = True

    def accept_friends_request(self, requestSender):
        self.send_accept(requestSender)
        self.accept_deny_Dialog.dismiss()
        self.remove_used_request_locally(requestSender)
        self.show_notifications_dialog()
        App.get_running_app().check_if_new_messages_alert()

    def send_accept(self, requestSender):
        data = {"action": "accept_friends_request", "requestingUserId": requestSender["requestingUserId"]}
        acceptRequest = requests.post(SERWER_ADRESS + "api_geoloc/", data=data, headers=HEADER)

    def deny_friends_request(self, requestSender):
        self.send_deny(requestSender)
        self.accept_deny_Dialog.dismiss()
        self.remove_used_request_locally(requestSender)
        self.show_notifications_dialog()
        App.get_running_app().check_if_new_messages_alert()

    def send_deny(self, requestSender):
        data = {"action": "deny_friends_request", "requestingUserId": requestSender["requestingUserId"]}
        denyRequest = requests.post(SERWER_ADRESS + "api_geoloc/", data=data, headers=HEADER)

    def remove_used_request_locally(self, requestSender):
        global CURRENT_USER_DATA
        CURRENT_USER_DATA["friendsRequests"] = [request for request in CURRENT_USER_DATA["friendsRequests"] if
                                                request["requestingUserId"] != requestSender["requestingUserId"]]

        for item in self.allUsersDialog.items:
            if item.requestingUserData == requestSender:
                item.text = ""
                item.requestingUserData = ""
                item.source = ""

    def pass_friends_request(self):
        self.accept_deny_Dialog.dismiss()
        self.show_notifications_dialog()

    # Messages

    def display_all_messages_threads(self):
        if CURRENT_USER_DATA:
            self.show_allUsers_dialog(type="message")

    # Map markers
    def zoom_update(self, mapObject):
        if mapObject != None:
            if self.zoomUpdate == True:
                App.get_running_app().root.get_screen("MainScreen").marker_in_use = None
                App.get_running_app().root.get_screen("MainScreen").touchList = [0, 0]
                self.add_markers_depending_on_zoom(mapObject.zoom)

    def add_markers_depending_on_zoom(self, zoom):
        self.remove_current_markers()  # Zamienić później na layersy ??
        self.add_markers_kmeans(zoom)
        self.update_work_home()

    def update_work_home(self):
        global WORKMARKER, HOMEMARKER, work_LAT, work_LON, home_LAT, home_LON
        try:
            if work_LAT != "0.0":
                WORKMARKER.lat, WORKMARKER.lon = work_LAT, work_LON
                WORKMARKER.opacity = 1

        except:
            pass
        try:
            if home_LAT != "0.0":
                HOMEMARKER.lat, HOMEMARKER.lon = home_LAT, home_LON
                HOMEMARKER.opacity = 1
        except:
            pass
        # MAIN_MAP.do_update(1)

    def remove_current_markers(self):
        global MAIN_MAP
        for marker in [x for x in self.markers_on_map]:
            try:
                MAIN_MAP.remove_marker(marker)
            except:
                pass
        self.markers_on_map = []

    def add_markers_kmeans(self, zoom):
        if self.pauseMarkers == False:
            global MAIN_MAP, ALL_USERS_CONTAINER, ALL_POSTS_CONTAINER, USERS_IN_DISTANCE, CURRENT_KMEANS_DATA, ALARM_POSTS
            self.touchList = [0, 0]
            # if zoom <= 10:
            #     cluster = 2
            # elif zoom >= 11 and zoom <= 12:
            #     cluster = 2
            # elif zoom >= 13 and zoom <= 14:
            #     cluster = 2
            # elif zoom >= 15:
            #     cluster = 1
            # else:
            #     cluster = 2
            cluster = 2
            # if zoom == 19:
            #     cluster = 2

            if CURRENT_KMEANS_DATA:
                # Zrobić to inaczej - za każdym pobraniem od razu tworzę zestaw

                try:
                    for count, point in enumerate(CURRENT_KMEANS_DATA[str(cluster)]["resultPoints"]):
                        try:
                            marker = MapMarkerImp()
                            marker.markerMapClusterNum = cluster
                            marker.markerMapGroupNum = count
                            marker.lat, marker.lon = float(
                                CURRENT_KMEANS_DATA[str(cluster)]['all_objects_container'][str(count)][0][
                                    "lat"]) - 90, float(
                                CURRENT_KMEANS_DATA[str(cluster)]['all_objects_container'][str(count)][0]["lon"]) - 180
                            marker.source = "user_post.png"
                            if cluster == 1:
                                if CURRENT_KMEANS_DATA[str(cluster)]['all_objects_container'][str(count)][0][
                                    "type"] == "post":
                                    marker.source = "post.png"

                            marker.opacity = 0.85
                            marker.size = self.find_marker_size(cluster, count)
                            marker.MAIN_MAP = MAIN_MAP

                            MAIN_MAP.add_marker(marker)
                            self.markers_on_map.append(marker)
                        except:
                            pass
                except:
                    pass

                self.add_alarmPost()

    def add_alarmPost(self):
        global ALARM_POSTS
        for alarmPost in ALARM_POSTS:
            marker = MapMarkerImp()
            marker.post = alarmPost
            marker.username = alarmPost["username"]
            marker.type = alarmPost["type"]
            marker.lat, marker.lon = float(alarmPost["lat"]) - 90, float(alarmPost["lon"]) - 180
            marker.source = "alarm.png"
            marker.id = alarmPost["id"]
            marker.opacity = 0.85
            marker.onlyUser = True
            marker.size = (120, 120)
            marker.MAIN_MAP = MAIN_MAP
            label = MDFillRoundFlatIconButton(text=alarmPost["postShort"], md_bg_color=(1, 0.0, 0, 1),
                                              icon="alert-octagram-outline")
            marker.add_widget(label)
            marker.is_open = True
            MAIN_MAP.add_marker(marker)
            self.markers_on_map.append(marker)

    def display_users_from_selected_container(self, list_of_users, type="user"):
        global MAIN_MAP
        if type == "user":
            dialog = self.allUsersDialog
        else:
            dialog = self.allUsersDialog

        self.remove_current_markers()
        self.touchList = [0, 0]
        self.create_markesr_from_small_list(list_of_users, type)
        self.zoomUpdate = False
        x, y = Window.size
        # self.resetViewButton = MDFillRoundFlatIconButton(
        #     text="Show-back all users" if type == "user" else "Show-back all posts", icon="account-box-multiple",
        #     pos=(x * 0.25, y * 0.12), on_release=lambda x=1: self.show_back_all_users())
        # MAIN_MAP.add_widget(self.resetViewButton)
        # MAIN_MAP.zoom -= 1
        self.ids["bottomToolbar"].left_action_items = [["arrow-left", lambda x: self.show_back_all_users()]]
        self.ids["bottomToolbar"].right_action_items = []
        self.Displayed_Map_Button = True
        dialog.dismiss()

    def show_back_all_users(self):
        global MAIN_MAP
        # print(self.resetViewButton.parent)
        # self.resetViewButton.opacity = 0
        # MAIN_MAP.remove_widget(self.resetViewButton)

        self.zoomUpdate = True
        self.zoom_update(MAIN_MAP)
        self.Displayed_Map_Button = False

        messagesButton = ["message-outline", lambda x: self.display_all_messages_threads()]
        self.ids["bottomToolbar"].left_action_items = [["dots-vertical", lambda x: self.open_menu(), "Open menu"],
                                                       ["bell-ring-outline", lambda x: self.show_notifications_dialog(),
                                                        "Show notifications", "Show notifications"], messagesButton
                                                       ]
        self.ids["bottomToolbar"].right_action_items = [
            ["account-group", lambda x: self.show_allUsers_dialog(type="user"), "Preview all users",
             "Preview all users"],
            ["message-question-outline", lambda x: self.show_allUsers_dialog(type="post"), "Preview all posts",
             "Preview all posts"],
            ["message-plus-outline", lambda x: self.create_post(), "Create post", "Create post"]]

        self.ids["messagesButton"] = messagesButton

    def create_markesr_from_small_list(self, list_of_users, type="user"):
        global MAIN_MAP
        for user in list_of_users:
            if type == "post":
                if user["alarmPost"] == True:
                    continue

            marker = MapMarkerImp()
            marker.user = user
            marker.username = user["username"]
            marker.type = user["type"]
            marker.lat, marker.lon = float(user["lat"]) - 90, float(user["lon"]) - 180
            marker.id = user["id"]
            if type == "user":
                if user["profilePhotoMini"] != None:
                    img_data = requests.get(user["profilePhotoMini"]).content

                    with open(f'profile_mini/{user["id"]}.jpg', 'wb') as handler:
                        handler.write(img_data)

                marker.source = "person.png" if user["profilePhotoMini"] == None else f"profile_mini/{user['id']}.jpg"
            elif type == "post":
                marker.source = "post.png" if user["sellPost"] == False else "money.png"
                marker.post = user
            marker.size = (80, 80)
            marker.opacity = 0.85
            marker.onlyUser = True
            marker.MAIN_MAP = MAIN_MAP
            MAIN_MAP.add_marker(marker)
            self.markers_on_map.append(marker)

        self.add_alarmPost()

    def find_marker_size(self, cluster, count):
        global MAIN_MAP
        markerSize = (len(CURRENT_KMEANS_DATA[str(cluster)]["all_users_container"][str(count)]) * 7,
                      len(CURRENT_KMEANS_DATA[str(cluster)]["all_users_container"][str(count)]) * 7)
        if markerSize[0] < 180:
            return (180, 180)
        elif markerSize[0] > 240:
            return (240, 240)
        else:
            return markerSize

    def fix_small_list_of_points(self, smallListOfPoints):
        fixedList = [[float(str(x[0] - 90)[:7]), float(str(x[1] - 180)[:7])] for x in smallListOfPoints]
        return fixedList

    def show_user_marker(self):
        global MAIN_MAP, user_LAT, user_LON
        MAIN_MAP.center_on(float(user_LAT), float(user_LON))
        MAIN_MAP.zoom = 18

    ####Set_WORK_&_HOME_LOLATIONS
    def create_Menu(self):
        self.Menu = MDDialogEdited(type="simple", items=[
            MenuIconListItem(text="Add Home localization", icon="home",
                             on_release=lambda x=1: self.setWorkOrHome("home")),
            MenuIconListItem(text="Add Work localization", icon="tie",
                             on_release=lambda x=1: self.setWorkOrHome("work")),
            MenuIconListItem(text="Set distance", icon="signal-distance-variant",
                             on_release=lambda x=1: self.set_distance()),
            MenuIconListItem(text="Display Friends only", icon="account-group",
                             on_release=lambda x=1: self.friends_only()),
        ])

    def open_menu(self):
        self.dialog_opened = True
        self.Menu.open()

    def setWorkOrHome(self, type):
        global MAIN_MAP
        self.Menu.dismiss()

        change_aviable, time, last_time = self.check_change_possibility(type)
        if change_aviable:
            self.display_add_place_information_widget()
            self.pauseMarkers = True
            MAIN_MAP.double_tap_zoom = False
            self.remove_current_markers()
            self.enable_disable_all_buttons("disable")
            self.add_accept_buttons()
            self.choose_layer = MapLayer(on_touch_down=lambda *args: self.placeIconOnMap(*args, type=type))
            MAIN_MAP.add_layer(self.choose_layer)
        else:
            self.display_change_not_aviable(type, time, last_time)

    def display_change_not_aviable(self, type, time, last_date):
        self.change_not_aviable = MDDialogEdited(
            text=f"You need to wait {30 - time} days to change your {type} localization. Last the change was made: {last_date}",
            buttons=[MDIconButton(icon="check-outline", on_release=lambda x: self.change_not_aviable.dismiss())]
        )
        self.change_not_aviable.open()
        self.dialog_opened = True

    def check_change_possibility(self, type):
        if type == "work":
            lastTime = CURRENT_USER_DATA["last_time_work_set"]
        elif type == "home":
            lastTime = CURRENT_USER_DATA["last_time_home_set"]
        # lastTime = "2022-07-03T13:07:55.826650Z"    #TEST DATE
        lastTime = lastTime.replace("T", " ")
        lastTime = lastTime.replace("Z", " ")
        lastTime = lastTime[2:19]
        lastTime = datetime.datetime.strptime(lastTime, '%y-%m-%d %H:%M:%S')
        result = datetime.datetime.now() - lastTime
        if result.days >= 30:
            return True, result.days, lastTime
        else:
            return False, result.days, lastTime

    def placeIconOnMap(self, *args, **kwargs):
        global HOMEMARKER, WORKMARKER, MAIN_MAP
        if kwargs["type"] == "home":
            self.markerToMove = HOMEMARKER
            self.markerToMove.type = "home"
        elif kwargs["type"] == "work":
            self.markerToMove = WORKMARKER
            self.markerToMove.type = "work"

        touch = args[1]
        if touch.is_double_tap:
            lat, lon = MAIN_MAP.get_latlon_at(touch.x, touch.y)
            self.markerToMove.lat, self.markerToMove.lon = lat, lon
            self.markerToMove.opacity = 1

    def add_accept_buttons(self):
        global MAIN_MAP
        self.acceptButton = MDFloatingActionButton(
            text="Accept",
            icon="check-outline",
            opacity=0.89,
            on_release=lambda x=1: self.accept_choose()
        )
        self.denyButton = MDFloatingActionButton(
            text="Abandon",
            icon="cancel",
            md_bg_color=(1, 1, 1),
            text_color=(0.2, 0.5, 1),
            icon_color=(0.2, 0.5, 1),
            opacity=0.89,
            on_release=lambda x=1: self.abandon_choose()
        )
        MAIN_MAP.add_widget(self.acceptButton)
        MAIN_MAP.add_widget(self.denyButton)
        self.acceptButton.pos_hint = {"x": 0.1, "y": 0.1}
        x, y = Window.size
        self.acceptButton.pos = (x * 0.1, y * 0.12)
        self.denyButton.pos = (x * 0.8, y * 0.12)

    def accept_choose(self):

        global WORKMARKER, HOMEMARKER, home_LAT, home_LON, work_LAT, work_LON, MAIN_MAP
        if self.markerToMove.type == "home":
            home_LAT, home_LON = HOMEMARKER.lat, HOMEMARKER.lon
        elif self.markerToMove.type == "work":
            work_LAT, work_LON = WORKMARKER.lat, WORKMARKER.lon
        MAIN_MAP.remove_widget(self.acceptButton)
        MAIN_MAP.remove_widget(self.denyButton)
        MAIN_MAP.remove_layer(self.choose_layer)
        MAIN_MAP.double_tap_zoom = True
        self.enable_disable_all_buttons("enable")
        self.pauseMarkers = False
        self.send_home_work_data_to_serwer(self.markerToMove.type)

    def send_home_work_data_to_serwer(self, type):
        data = {"home_LAT": home_LAT, "home_LON": home_LON, "work_LAT": work_LAT, "work_LON": work_LON,
                "action": "set_work_home", "type": type}
        setWorkHome = requests.post(SERWER_ADRESS + "api_geoloc/", data=data, headers=HEADER)

    def abandon_choose(self):
        global MAIN_MAP, work_LAT, work_LON, home_LAT, home_LON
        # MAIN_MAP.remove_marker(self.markerToMove)
        MAIN_MAP.remove_widget(self.acceptButton)
        MAIN_MAP.remove_widget(self.denyButton)
        MAIN_MAP.remove_layer(self.choose_layer)
        MAIN_MAP.double_tap_zoom = True
        self.update_work_home()
        if self.markerToMove.type == "work":
            self.markerToMove.lat, self.markerToMove.lon = work_LAT, work_LON
        elif self.markerToMove.type == "home":
            self.markerToMove.lat, self.markerToMove.lon = home_LAT, home_LON
        # HOMEMARKER = None
        # WORKMARKER = None
        self.enable_disable_all_buttons("enable")
        self.pauseMarkers = False

    def enable_disable_all_buttons(self, type):
        buttons = []
        layouts = self.children[0].children
        for layout in layouts:
            buttons.extend(layout.children)

        for button in buttons:
            try:
                if type == "disable":
                    button.disabled = True
                    button.opacity = 0
                elif type == "enable":
                    button.disabled = False
                    button.opacity = 1
            except:
                pass

    def display_add_place_information_widget(self):
        self.placeInfoDialog = MDDialogEdited(
            type="custom",
            content_cls=PlaceInfoDialogContent(),
            buttons=[MDIconButton(icon="check-outline", on_release=lambda x: self.placeInfoDialog.dismiss())]
        )
        self.placeInfoDialog.children[0].md_bg_color = 1, 0.2, 0.2, 0.5
        self.placeInfoDialog.open()
        self.dialog_opened = True

    # Distance

    def create_set_distance_dialog(self):
        self.setDistanceDialog = MDDialogEdited(
            title="Set distance in meters ( max 200, min 1 )?",
            type="custom",
            content_cls=DistanceDialogContent(),
            buttons=[MDIconButton(icon="backspace-outline", on_release=lambda x: self.setDistanceDialog.dismiss()),
                     MDIconButton(icon="check-outline", on_release=lambda x: self.accept_distance())],
        )
        self.setDistanceDialog.ids["hours"] = self.setDistanceDialog.children[0].children[2].children[0].children[0]

    def set_distance(self):
        self.setDistanceDialog.ids["hours"].hint_text = "Current set distance: " + str(self.distance)
        self.setDistanceDialog.open()
        self.Menu.dismiss()

    def accept_distance(self):
        global DISTANCE
        if self.setDistanceDialog.ids["hours"].text.isdigit():
            if int(self.setDistanceDialog.ids["hours"].text) <= 200 and int(
                    self.setDistanceDialog.ids["hours"].text) >= 1:
                DISTANCE = int(self.setDistanceDialog.ids["hours"].text)
                self.setDistanceDialog.ids["hours"].text = ""
                self.setDistanceDialog.ids["hours"].hint_text = "OK ! :)"
                self.distance = DISTANCE
                Clock.schedule_once(self.setDistanceDialog.dismiss)
                Clock.schedule_once(lambda dt: self.change_menu_dialog_text("distance", loading=True), 0)
                Clock.schedule_once(self.friendsOnlyDialog.open, 0)

                Clock.schedule_once(App.get_running_app().update_all_data, 0.2)
                Clock.schedule_once(lambda dt: self.zoom_update(MAIN_MAP), 0.5)
                Clock.schedule_once(lambda dt: self.change_menu_dialog_text("distance", loading=False), 1)
                print(DISTANCE)
            else:
                self.setDistanceDialog.ids["hours"].hint_text = "Value must be in range 1-200 :( "
                self.setDistanceDialog.ids["hours"].text = ""

    # Friends Only

    def create_friends_only_dialog(self):
        self.friendsOnlyDialog = MDDialogEdited(
            text="Now you will recieve only friends informations",
            type="simple",
            buttons=[MDFillRoundFlatIconButton(icon="check", text="ok",
                                               on_release=lambda x: self.friendsOnlyDialog.dismiss())], )

    def friends_only(self):
        global FRIENDS_ONLY, CURRENT_USER_DATA

        if FRIENDS_ONLY == False:
            FRIENDS_ONLY = True
            Clock.schedule_once(self.Menu.dismiss)
            self.Menu.items[3].text = "Display All users"
            self.friendsOnlyDialog.text = "Now you will see only friends in distance"
            Clock.schedule_once(lambda dt: self.change_menu_dialog_text("friendsOnly", loading=True))

            Clock.schedule_once(self.friendsOnlyDialog.open, 0)

            Clock.schedule_once(App.get_running_app().update_all_data, 0.2)
            Clock.schedule_once(lambda dt: self.zoom_update(MAIN_MAP), 0.5)
            Clock.schedule_once(lambda dt: self.change_menu_dialog_text("friendsOnly", loading=False), 1)

        else:
            FRIENDS_ONLY = False
            Clock.schedule_once(self.Menu.dismiss)
            self.Menu.items[3].text = "Display Friends only"
            self.friendsOnlyDialog.text = "Now you will see all users in distance"
            Clock.schedule_once(lambda dt: self.change_menu_dialog_text("friendsOnly", loading=True))

            Clock.schedule_once(self.friendsOnlyDialog.open, 0)

            Clock.schedule_once(App.get_running_app().update_all_data, 0.2)
            Clock.schedule_once(lambda dt: self.zoom_update(MAIN_MAP), 0.5)
            Clock.schedule_once(
                lambda dt: self.change_menu_dialog_text("friendsOnly", loading=False, friendsOnly=FRIENDS_ONLY), 1)

    def change_menu_dialog_text(self, type, loading=False, friendsOnly=True, dt=0):
        if type == "friendsOnly":
            if friendsOnly == True and loading == False:
                self.friendsOnlyDialog.buttons[0].opacity = 1
                self.friendsOnlyDialog.text = "Now you will see only friends in distance"
            elif friendsOnly == False and loading == False:
                self.friendsOnlyDialog.buttons[0].opacity = 1
                self.friendsOnlyDialog.text = "Now you will see all users in distance"
            else:
                self.friendsOnlyDialog.buttons[0].opacity = 0
                self.friendsOnlyDialog.text = "One second... ( Or two, eventually ;) "
        elif type == "distance":
            if loading == False:
                self.friendsOnlyDialog.buttons[0].opacity = 1
                self.friendsOnlyDialog.text = "Distance set"
            else:
                self.friendsOnlyDialog.buttons[0].opacity = 0
                self.friendsOnlyDialog.text = "One second... ( Or two, eventually ;) "

    # Logout

    def logout(self):
        self.Menu.dismiss()
        self.logout_dialog = MDDialogEdited(
            text="Do you really want to logout ?",
            buttons=[MDFillRoundFlatIconButton(icon="logout", text="Yes", on_release=lambda x: self.confirm_logout()),
                     MDFillRoundFlatIconButton(icon="backspace-reverse-outline", text="No",
                                               on_release=lambda x: self.logout_dialog.dismiss()),
                     ]
        )
        self.logout_dialog.open()

    def confirm_logout(self):
        global USERNAME, USERMARKER, HOMEMARKER, WORKMARKER, LOGIN, TOKEN, HEADER, user_LAT, user_LON, home_LAT, home_LON, work_LAT, work_LON, USERS_IN_DISTANCE, POSTS_IN_DISTANCE, UPDATE_ALL_DATA_THREAD, USER_MARKER_THREAD_LIST, NEW_MESSAGES_THREAD, CURRENT_USER_DATA, CURRENT_KMEANS_DATA, ALARM_POSTS, UPDATE_ENABLED, MAIN_MAP, ALL_USERS_CONTAINER, ALL_POSTS_CONTAINER, DICT_OF_ZOOM_POINTS_POSITIONS
        os.remove("loginData.txt")
        self.logout_dialog.dismiss()
        self.remove_current_markers()

        self.firstEnter = True

        self.firstEnter = True
        self.touchList = [0, 0]
        self.marker_in_use = None

        self.markers_on_map = []

        self.notifications = BooleanProperty(defaultvalue=False)

        self.all_users_dialog_lenght = 10
        self.zoomUpdate = True
        self.Displayed_Map_Button = False

        self.previewDialogListStatus = [0, 8]

        self.pauseMarkers = False

        self.dialog_opened = False
        try:
            MAIN_MAP.remove_marker(HOMEMARKER)
        except:
            pass
        try:
            MAIN_MAP.remove_marker(WORKMARKER)
        except:
            pass
        try:
            MAIN_MAP.remove_marker(USERMARKER)
        except:
            pass

        App.get_running_app().root.get_screen("LoginScreen").ids['userName'].text = ""
        App.get_running_app().root.get_screen("LoginScreen").ids['userPassword'].text = ""

        self.manager.current = "LoginScreen"

        # self.checkDataStatus.cancel()

        USERNAME = ""
        USERMARKER = None
        HOMEMARKER = None
        WORKMARKER = None
        LOGIN = False

        TOKEN = ""
        HEADER = ""

        user_LAT = "53.42430"
        user_LON = "14.52040"

        home_LAT = "0.0"
        home_LON = "0.0"

        work_LAT = "0.0"
        work_LON = "0.0"
        ########
        USERS_IN_DISTANCE = []
        POSTS_IN_DISTANCE = []
        ########
        UPDATE_ALL_DATA_THREAD = []
        USER_MARKER_THREAD_LIST = []
        NEW_MESSAGES_THREAD = []

        CURRENT_USER_DATA = ""
        CURRENT_KMEANS_DATA = ""
        ALARM_POSTS = ""

        UPDATE_ENABLED = True

        ######
        MAIN_MAP = None

        ALL_USERS_CONTAINER = {}
        ALL_POSTS_CONTAINER = {}

        DICT_OF_ZOOM_POINTS_POSITIONS = {}


class PostScreen(Screen):
    marker = None
    data = None
    postUsername = StringProperty()
    currentUser = StringProperty()
    postContent = StringProperty()
    postComments = None
    text_Field = None
    commentWidget = None
    postDate = None
    displayUserAndDate = StringProperty()
    back_to_main = False
    fromMarker = False
    comment_mode = False
    requestData = DictProperty()
    first_enter = True
    first_pre_enter = True
    new_comment = False
    post_update_thread = []
    current_postComments = []

    # Poprawić że po wysłaniu posta nie pojawia się napis że post wysłano !!
    # Poprawić że popup zdjęcia pojawia sie przy powrocie do main screena !!

    def on_pre_enter(self, *args):
        global UPDATE_ENABLED
        UPDATE_ENABLED = False
        if self.first_pre_enter:
            self.main_widgets_add()
        self.update_post()

    def create_start_board(self):
        self.startBoard = Popup(background_color=[0, 0, 0, 0], title="",
                                separator_color=[0.2, 0.5, 1, 0])
        small_Popup = Popup(background_color=[0, 0, 0, 0], title="",
                            separator_color=[0.2, 0.5, 1, 0], size_hint_y=0.1, pos_hint={"top": 0.5})
        self.startBoard.add_widget(small_Popup)
        self.startBoard.ids["small_popup"] = small_Popup

    def show_start_board(self):
        if self.first_pre_enter:
            self.startBoard.open()
            progressBar = MDProgressBar(pos_hint={"right": 0, "top": 1})
            self.upgradeProgressObj = Clock.schedule_interval(self.upgradeProgress, 0.05)
            self.startBoard.ids["small_popup"].add_widget(progressBar)
            self.startBoard.ids["progress_bar"] = progressBar

    def main_widgets_add(self):
        # bgImage = kivyImage(source="xxx.png", size=(self.size[0], self.size[1]), allow_stretch=True, keep_ratio=False)

        mdToolbar = MDTopAppBar(pos_hint={"top": 1})
        mdToolbar.right_action_items = [
            ["trash-can-outline", lambda x: self.delete_post(), "Delete post", "Delete post"]]
        labelBox = BoxLayout(size_hint_y=0.15)
        gridLayout = GridLayout(rows=7, cols=1, spacing=10, pos_hint={"x": 0.1, "center_y": 0.49}, size_hint_y=0.7,
                                size_hint_x=0.8, height=self.height * 0.8)
        mdLabel = MDLabel(pos_hint={"x": 0.05, "y": 1}, size_hint_y=0.05, theme_text_color="Custom",
                          text_color=(0.2, 0.5, 1), text=self.displayUserAndDate)
        asyncImage = AsyncImageButton(source="", size_hint_x=0.6, size_hint_y=0.6, size=(0, 0), opacity=0,
                                      on_release=lambda x: self.display_post_gallery())
        roundIconButton = MDFillRoundFlatIconButton(on_release=lambda x: self.display_owner_menu(self.postOwnerData),
                                                    halign="left", size_hint_x=1)
        commentsGrid = MDGridLayout(cols=1, rows=1)
        toolbarBottom = MDTopAppBar(type="top", opacity=1)
        toolbarBottom.right_action_items = [
            ["message-reply-text-outline", lambda x: self.comment_post(), "Odpowiedz", "Odpowiedz"]]
        toolbarBottom.left_action_items = [
            ["arrow-left-thick", lambda x: self.back_to_main_screen(back_to_main=True), "Wróć", "Wróć"]]
        # self.add_widget(bgImage)
        self.add_widget(mdToolbar)

        self.add_widget(gridLayout)
        self.ids["mainGrid"] = gridLayout
        labelBox.add_widget(mdLabel)
        self.ids["mainGrid"].add_widget(labelBox)
        self.ids["mainGrid"].add_widget(asyncImage)
        self.ids["mainGrid"].add_widget(roundIconButton)
        self.ids["mainGrid"].add_widget(commentsGrid)
        self.add_widget(toolbarBottom)
        self.ids["topToolbar"] = mdToolbar
        # self.ids["Background_image_post"] = bgImage
        self.ids["infoLabel"] = mdLabel
        self.ids["postImage"] = asyncImage
        self.ids["postTextBubble"] = roundIconButton
        self.ids["contentGridLayout"] = commentsGrid

    def upgradeProgress(self, dt=0):
        self.startBoard.ids["progress_bar"].value += 10

    def on_enter(self, *args):

        self.currentUser = CURRENT_USER_DATA["username"].title()
        self.displayImage()
        if self.first_enter:
            self.add_comments_widget()
            self.first_enter = False

        self.update_post_text_bubble()
        self.add_comments_to_comment_widget()

        self.update_comments_clock_obj = Clock.schedule_interval(self.update_post_thread, 4)
        self.check_if_new_comment_obj = Clock.schedule_interval(self.check_if_new_comment, 5)

        if self.first_pre_enter:
            self.upgradeProgressObj.cancel()
            self.startBoard.ids["progress_bar"].value = 100
            self.first_pre_enter = False
            self.startBoard.dismiss()

        self.ids["infoLabel"].text = self.displayUserAndDate

        Window.bind(on_key_down=self._on_keyboard_down)

    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        try:
            if self.ids["textField"].focus and keycode == 40:  # 40 - Enter key pressed
                self.send_comment()
        except:
            pass

    def update_post(self):
        self.postContent, self.postComments, self.postUsername, self.postDate, self.postImage, self.photosCount, self.postOwnerData = self.request_post_content()
        if self.postImage:
            self.postImagePath = self.postImage

        self.displayUserAndDate = f"\nphotos: ({self.photosCount}) "

    #
    def create_post_text_bubble(self):
        # Tu gdzie jest "" - dodać właściciela postu !
        # self.bubble = MDTextFieldMessageBubble(theme_text_color= "Custom",text_color = (0,0,0,1),background_color=(0.2,0.6,1, 0.9),
        #                                        multiline=True,icon_right="account",icon_right_color=(0,0,1,1),
        #                                        on_release= lambda x: self.display_owner_menu(self.bubble,self.postOwnerData),halign="left")
        # # self.bubble.disabled = True
        # self.bubble.canvas.before.children[14].radius = [(10, 10), (10, 10), (10, 10), (10, 10)]
        # self.ids["contentGridLayout"].add_widget(self.bubble)
        # self.ids["postTextBubble"] = self.bubble
        pass

    def update_post_text_bubble(self):
        self.ids["topToolbar"].title = self.postUsername + "`s post: "
        self.ids["postTextBubble"].size_hint_x = 1
        self.ids["postTextBubble"].text = "   " + self.postDate.replace("T", "  ")[
                                                  :20] + "\n" + f"            {self.postContent}"

        self.ids["postTextBubble"].icon = "post.png"

        # Do naprawy !!
        # if self.postOwnerData["profilePhotoMini"] != None:
        #     try:
        #         self.ids["postTextBubble"].icon = self.download_or_return_mini_profile(photoSmallAdress=self.postOwnerData["profilePhotoMini"][1:])
        # else:
        #     self.ids["postTextBubble"].icon = "post.png"

    # def download_or_return_mini_profile(self,photoSmallAdress):
    #     photoAdress = SERWER_ADRESS + "media/" + photoSmallAdress
    #     photoName = photoAdress.split("/")[-1]
    #     for file in os.listdir("gallery_images_cache/"):
    #         if file == photoName:
    #             try:
    #                 self.ids["postTextBubble"].icon = f"gallery_images_cache/{photoName}"
    #                 return f"gallery_images_cache/{photoName}"
    #             except:
    #                 os.remove(f"gallery_images_cache/{photoName}")
    #                 continue
    #     # If not return:
    #     try:
    #         photoRequest = requests.get(photoAdress, headers=HEADER, stream=True)
    #
    #         with open(f"gallery_images_cache/{photoName}", "wb") as photoToSave:
    #             photoToSave.write(photoRequest.content)
    #
    #         return f"gallery_images_cache/{photoName}"
    #     except:
    #         return "post.png"

    def update_post_thread(self, dt=0):
        self.post_update_thread = [thread for thread in self.post_update_thread if thread.is_alive()]
        if NEW_MESSAGES_THREAD == []:
            thread = threading.Thread(target=self.request_post_comments_only)
            self.post_update_thread.append(thread)
            self.post_update_thread[-1].start()
        else:
            pass

    #
    def request_post_content(self, **kwargs):
        global HEADER

        postContent = requests.request("GET", data=self.requestData, headers=HEADER,
                                       url=SERWER_ADRESS + "api_geoloc/").json()
        self.data = postContent
        content, comments, postUsername, postDate, postImage, imagesCount, postOwnerData = postContent["postContent"], \
                                                                                           postContent["comments"], \
                                                                                           postContent["postOwnerName"], \
                                                                                           postContent["postDate"], \
                                                                                           postContent["postImage"], \
                                                                                           postContent[
                                                                                               "relatedPhotosCount"], \
                                                                                           postContent["postOwnerData"]
        self.post_id = postContent["id"]
        if self.current_postComments != None and self.current_postComments != comments:
            self.postComments = comments
            self.new_comment = True

        return (content, comments, postUsername, postDate, postImage, imagesCount, postOwnerData)

    #
    def request_post_comments_only(self):
        global HEADER
        data = {"action": "request_post_comments_only", "post_id": self.post_id}
        comments = requests.request("GET", data=data, headers=HEADER, url=SERWER_ADRESS + "api_geoloc/").json()[
            "comments"]

        if self.current_postComments != comments:
            self.postComments = comments
            self.new_comment = True

    def displayImage(self):
        imageWidget = self.ids["postImage"]
        imageWidget.opacity = 1

        if self.postImage != "/media/photo" and self.postImage != None:
            imageWidget.source = self.postImagePath
        else:
            if self.data["alarmPost"] == False and self.data["sellPost"] == False:
                imageWidget.source = "post.png"
            elif self.data["alarmPost"] == True:
                imageWidget.source = "alarm.png"
            elif self.data["sellPost"] == True:
                imageWidget.source = "money.png"
        imageWidget.size_hint_x = 1
        imageWidget.size_hint_y = 1

    def create_image_dialog(self):
        popupImageContent = AsyncImage()
        self.popupImage = Popup(title=self.displayUserAndDate, background_color=[0, 0, 0, 0],
                                separator_color=[0.2, 0.5, 1, 1], content=popupImageContent,
                                on_touch_move=lambda *args: self.close_popup_image())
        self.popupImage.ids["image"] = popupImageContent

    def display_image_dialog(self):
        imageWidget = self.ids["postImage"]
        if imageWidget.source not in ["post.png", "alarm.png", "money.png"]:
            self.popupImage.ids["image"].source = imageWidget.source
            self.popupImage.open()

    def display_post_gallery(self):
        if self.photosCount > 1:
            self.on_leave()
            self.data["username"] = self.postUsername
            App.get_running_app().root.get_screen("PhotosGalleryScreen").previewingPost = True
            App.get_running_app().root.get_screen("PhotosGalleryScreen").mainData = self.data
            self.manager.current = "PhotosGalleryScreen"
        else:
            self.display_image_dialog()

    def close_popup_image(self):
        self.popupImage.source = ""
        self.popupImage.dismiss()

    def hide_image(self):
        imageWidget = self.ids["postImage"]
        imageWidget.opacity = 0
        imageWidget.source = ""
        imageWidget.size_hint_x = None
        imageWidget.size_hint_y = None

    def add_comments_widget(self):
        mainlayout = self.ids["contentGridLayout"]
        self.scrollView = ScrollView()
        self.scrollView.size = self.size
        self.scrollView.size_hint_y = 0.5
        self.commentGrid = MDGridLayout(cols=1, adaptive_height=True, padding=(dp(10), dp(10)), spacing=dp(15))
        self.commentGrid.adaptive_height = True
        self.commentGrid.height = self.commentGrid.minimum_height
        self.scrollView.add_widget(self.commentGrid)
        mainlayout.add_widget(self.scrollView)

    def create_comment_bubble(self, comment):
        commentBubble = MDFillRoundFlatIconButton(theme_text_color="Custom", text_color=(0, 0, 0, 1),
                                                  md_bg_color=(0.2, 0.8, 0.6, 0.9),
                                                  on_release=lambda x: self.display_owner_menu(comment["userData"]))
        commentBubble.rounded_button = False

        self.ids["postTextBubble"].icon = "post.png"

        # if comment["commentOwnerPhoto"] != None:
        #     commentBubble.icon = self.download_or_return_mini_profile(photoSmallAdress=comment["commentOwnerPhoto"][1:])
        # else:
        #     self.ids["postTextBubble"].icon = "post.png"

        time = comment["commentDate"][:19].replace("T", "  ")
        commentOwnerDate = comment['commentOwnerName'].title() + "       " + time
        commentText = comment['commentContent']

        commentBubble.text = f"{commentOwnerDate}\n\n   {commentText}"

        return commentBubble

    def add_comments_to_comment_widget(self):
        self.current_postComments = self.postComments.copy()
        for comment in self.postComments:
            commentBubble = self.create_comment_bubble(comment)

            self.commentGrid.add_widget(commentBubble)
        try:
            self.scrollView.scroll_to(commentBubble)
        except:
            pass

    def check_if_new_comment(self, dt=0):
        if self.new_comment == True:
            self.update_comments_widgets()
            self.new_comment = False

    def update_comments_widgets(self):

        for comment in self.postComments:
            unique = True

            for check in self.current_postComments:
                if comment["id"] == check["id"]:
                    unique = False
            if unique:

                commentBubble = self.create_comment_bubble(comment)

                if len(self.commentGrid.children) < 15:
                    self.commentGrid.add_widget(commentBubble)
                else:
                    widgetToRemove = self.commentWidget.children[-1]
                    self.commentGrid.remove_widget(widgetToRemove)
                    self.commentGrid.add_widget(commentBubble)

        self.current_postComments = self.postComments.copy()

        try:
            self.scrollView.scroll_to(commentBubble)
        except:
            pass

    def remove_comments_widget(self):
        layout = self.children[1]
        layout.remove_widget(self.commentGrid)

    def comment_post(self):
        self.comment_mode = True
        self.add_text_input()
        self.add_send_button()

    def abandon_comment(self):
        if self.comment_mode:
            layout = self.children[1]
            layout.remove_widget(self.text_Field)
            self.text_Field.text = ""
            bottomToolbar = self.children[0]
            bottomToolbar.right_action_items = [
                ["message-reply-text-outline", lambda x: self.comment_post(), "Odpowiedz", "Odpowiedz"]]
            self.comment_mode = False

    def create_text_input(self):
        self.text_Field = MDTextField(multiline=True, max_text_length=300, hint_text="Wpisz komentarz:")

    def add_text_input(self):
        self.layout = self.children[1]
        self.layout.add_widget(self.text_Field)
        self.ids["textField"] = self.text_Field

    def add_send_button(self):
        bottomToolbar = self.children[0]
        bottomToolbar.right_action_items = [["backspace-reverse", lambda x: self.abandon_comment(), "Abandon comment",
                                             "Abandon comment"],
                                            ["send", lambda x: self.send_comment(), "Odpowiedz", "Odpowiedz"]]

    def send_comment(self):
        global HEADER, user_LON, user_LAT, USERNAME
        commentText = self.text_Field.text + "\n"
        if commentText != "":
            data = {"id_post": self.data["id"],
                    "action": "comment_post", "id_user": CURRENT_USER_DATA["id"],
                    "lat_user": user_LAT, "lon_user": user_LON, "username": USERNAME, "commentText": commentText}
            sendComment = requests.post(SERWER_ADRESS + "api_geoloc/", data=data, headers=HEADER)
            self.abandon_comment()

    def back_to_main_screen(self, **kwargs):
        self.abandon_comment()
        self.manager.current = "MainScreen"
        if kwargs["back_to_main"] == True:
            self.back_to_main = True

    def on_leave(self, *args):
        global UPDATE_ENABLED
        UPDATE_ENABLED = True
        if self.back_to_main == True and self.fromMarker == False:
            # App.get_running_app().root.get_screen("MainScreen").show_allUsers_dialog(type="post")
            self.back_to_main = False
        else:
            self.fromMarker = False
        self.ids["postTextBubble"].text = ""
        self.commentGrid.clear_widgets()
        self.update_comments_clock_obj.cancel()
        self.check_if_new_comment_obj.cancel()

        self.postUsername = ""
        self.postContent = ""
        self.hide_image()

        # self.remove_comments_widget()

        if self.comment_mode:
            layout = self.children[1]
            layout.remove_widget(self.text_Field)
            try:
                layout.remove_widget(self.commentWidget)
            except:
                pass
            try:
                layout.remove_widget(self.text_Field)
            except:
                pass

    def pass_func(self):
        pass

    def delete_post(self):
        if self.postUsername == self.currentUser:
            self.noDeleteDialog = MDDialogEdited(
                text="Do you really want to delete your post?",
                buttons=[MDFillRoundFlatButton(text="yes", on_release=lambda x: self.send_delete_request()),
                         MDRoundFlatButton(text="No", on_release=lambda x: self.noDeleteDialog.dismiss())]
            )
            self.noDeleteDialog.open()

        else:
            self.noDeleteDialog = MDDialogEdited(
                text="It`s not your post :( you cant delete it :("
            )
            self.noDeleteDialog.open()
            pass

    def send_delete_request(self):
        request_data = {"post_id": self.data["id"], "action": "delete_post"}
        markPost_deleted = requests.post(SERWER_ADRESS + "api_geoloc/", data=request_data, headers=HEADER)
        self.noDeleteDialog.dismiss()
        self.back_to_main_screen(back_to_main=False)

    def create_owner_menu(self):
        itemOne = MenuIconListItem()
        itemTwo = MenuIconListItem()
        self.Menu = MDDialogEdited(type="simple", items=[itemOne, itemTwo])
        self.Menu.ids["itemOne"] = itemOne
        itemOne.icon = "account"
        self.Menu.ids["itemTwo"] = itemTwo
        itemTwo.icon = "message-reply-text-outline"

        # Mogę najpierw stworzyć menu a itemsy dodać self.Menu.items = [kkkk]

    def display_owner_menu(self, user):
        itemOne = self.Menu.ids["itemOne"]
        itemTwo = self.Menu.ids["itemTwo"]

        itemOne.text = f"{user['username'].title()}`s profile"
        itemOne.on_release = lambda x=1: self.open_users_profile(user)

        itemTwo.text = f"Message to {user['username'].title()}"
        itemTwo.on_release = lambda x=1: self.send_private_message(user)

        self.Menu.open()

    def open_users_profile(self, user):
        App.get_running_app().root.get_screen("UserScreen").show_start_board()
        App.get_running_app().root.get_screen("UserScreen").userData = user
        App.get_running_app().root.get_screen("UserScreen").fromMarker = False
        App.get_running_app().root.current = "UserScreen"
        self.Menu.dismiss()

    def send_private_message(self, user):
        if user["username"] != CURRENT_USER_DATA["username"]:
            thread = {"reciever": user["id"], "recieverName": user["username"], "sender": CURRENT_USER_DATA["id"],
                      "senderName": CURRENT_USER_DATA["username"], "lastSender": ""}
            App.get_running_app().root.get_screen("CurrentThreadMessagesScreen").show_start_board()
            App.get_running_app().root.get_screen("CurrentThreadMessagesScreen").thread = thread
            App.get_running_app().root.get_screen("CurrentThreadMessagesScreen").backToUser = False
            App.get_running_app().root.get_screen("CurrentThreadMessagesScreen").userData = user
            self.manager.current = "CurrentThreadMessagesScreen"
            self.Menu.dismiss()


class CreatePostScreen(Screen):
    usersPhotos = []
    first_enter = True
    first_pre_enter = True
    alarmPost = False

    def main_widgets_add(self):
        bgImage = kivyImage(source="", size=(self.size[0], self.size[1]), allow_stretch=True, keep_ratio=True)
        mdToolbar = MDTopAppBar(pos_hint={"top": 1})
        gridLayout = GridLayout(rows=2, cols=1, spacing=10, pos_hint={"x": 0.1, "center_y": 0.49}, size_hint_y=0.8,
                                size_hint_x=0.8)
        imageButton = ImageButton(source=None, size_hint_x=None, size_hint_y=None, size=(0, 0))
        boxLayout = BoxLayout(spacing=10, pos_hint={"x": 0.1, "center_y": 0.49}, size_hint_y=0.7, size_hint_x=0.8,
                              height=self.height * 0.8)
        textField = MDTextField(icon_right="comment-text", multiline=True, mode="fill",
                                hint_text="Wpisz wiadomosć", pos_hint={"y": 0.5}, size_hint_x=0.8,
                                line_color_normal=(0.2, 0.5, 1))
        textField.fill_color_normal = (0.2, 0.5, 1, 0.3)
        textField.fill_color_focus = (0.2, 0.5, 1, 0.2)
        # textField.icon_right_color = "app.theme_cls.primary_color"
        textField.text_color_normal = (0, 0, 0, 0.9)
        textField.text_color_focus = (0, 0, 0, 0.9)
        textField.hint_text_color_normal = (0, 0, 0, 0.5)

        bottomToolbar = MDTopAppBar(type="top")
        bottomToolbar.left_action_items = [["arrow-left-thick", lambda x: self.back_to_main_screen(), "Wróć", "Wróć"]]
        bottomToolbar.right_action_items = [
            ["currency-usd", lambda x: self.mark_post_as_sell(), "Mark post as sell", "Mark post as sell"],
            ["clock-time-three-outline", lambda x: self.set_post_time(), "Czas wyświetlania postu",
             "Czas wyświetlania postu"],
            ["bell-alert-outline", lambda x: self.alert_post(), "Post alarmowy", "Post alarmowy"],
            ["camera-plus-outline", lambda x: self.add_photo(), "Dodaj zdjęcia", "Dodaj zdjęcia"],
            ["send", lambda x: self.send_post(), "Wyślij", "Wyślij"]]

        self.add_widget(bgImage)
        self.ids["bgImage"] = bgImage
        self.add_widget(mdToolbar)
        self.add_widget(gridLayout)

        self.ids["MainGridLayout"] = gridLayout
        self.ids["MainGridLayout"].add_widget(imageButton)
        self.ids["ImageToSend"] = imageButton
        self.ids["MainGridLayout"].add_widget(boxLayout)
        self.ids["MainBoxLayout"] = boxLayout
        self.ids["MainBoxLayout"].add_widget(textField)
        self.ids["textField"] = textField
        self.add_widget(bottomToolbar)

    def create_start_board(self):
        self.startBoard = Popup(background_color=[0, 0, 0, 0], title="",
                                separator_color=[0.2, 0.5, 1, 0])
        small_Popup = Popup(background_color=[0, 0, 0, 0], title="",
                            separator_color=[0.2, 0.5, 1, 0], size_hint_y=0.1, pos_hint={"top": 0.5})
        self.startBoard.add_widget(small_Popup)
        self.startBoard.ids["small_popup"] = small_Popup

    def show_start_board(self):
        if self.first_pre_enter:
            self.startBoard.open()
            progressBar = MDProgressBar(pos_hint={"right": 0, "top": 1})
            self.upgradeProgressObj = Clock.schedule_interval(self.upgradeProgress, 0.05)
            self.startBoard.ids["small_popup"].add_widget(progressBar)
            self.startBoard.ids["progress_bar"] = progressBar

    def on_pre_enter(self, *args):
        if self.first_pre_enter:
            self.show_start_board()
            self.main_widgets_add()

    def upgradeProgress(self, dt=0):
        self.startBoard.ids["progress_bar"].value += 10

    def on_enter(self, *args):
        if self.first_pre_enter:
            self.upgradeProgressObj.cancel()
            self.startBoard.ids["progress_bar"].value = 100
            self.startBoard.dismiss()
            self.first_pre_enter = False

        if self.first_enter:
            self.first_enter = False

        self.hoursField = "0"
        self.minutesField = "30"
        # self.alarmPost = False
        self.textField = self.children[1].children[0].children[0]  # prawdopodobnie nie trafiam w text field
        self.textField.disabled = False
        self.textField.hint_text = "Wpisz post"
        self.photoToSendPath = None
        self.photoToSendObject = {"photo": None}
        self.sell_post = False

    def on_leave(self, *args):
        self.cancel_alarm(on_leave=True)
        self.reset_photo()
        self.textField.hint_text = ""

    def send_post(self):
        self.listOfPhotos = []
        counter = 0
        for photo in self.usersPhotos:
            objectToSend = photo["photoGalleryImage"]
            self.listOfPhotos.append(objectToSend)
            counter += 1

        postContent = self.textField.text
        if postContent != "":
            data = {"lat": user_LAT, "lon": user_LON, "text": postContent, "action": "create_post",
                    "username": USERNAME, "postDisplayTime": f"{self.hoursField}.{self.minutesField}",
                    "alarmPost": self.alarmPost, "sellPost": self.sell_post}
            sendPost = requests.post(SERWER_ADRESS + "api_geoloc/", data=data, headers=HEADER)

            # try:
            if sendPost.json()["response"] == "Ok":
                self.send_post_images(sendPost.json()["id"])

                self.textField.text = ""
                self.textField.hint_text = "Post wysłany !"
                self.textField.icon_right = "check-bold"
                self.textField.disabled = True
                self.cancel_alarm(on_leave=False, on_send=True)
            else:
                self.textField.hint_text = "Nie udało się wysłać !"

    def send_post_images(self, postId):

        for photo in self.usersPhotos:
            # może spróbować otwirerać tu ten plik jeszcze raz, np za pomocą image ?
            photoData = {"photoObject": open(photo["photoPath"], "rb")}
            data = {"action": "add_post_image", "postId": postId}
            sendPost = requests.post(SERWER_ADRESS + "api_geoloc/", data=data, headers=HEADER, files=photoData)

    def create_set_post_time_dialog(self):
        self.timeDialog = MDDialogEdited(
            title="Podaj czas:",
            type="custom",
            content_cls=PostTimeDialogContent(),
            buttons=[MDIconButton(icon="backspace-outline", on_release=lambda x: self.timeDialog.dismiss()),
                     MDIconButton(icon="check-outline", on_release=lambda x: self.accept_post_time())],
        )

    def set_post_time(self):
        if self.hoursField != "0" or self.minutesField != "30":
            self.timeDialog.content_cls.ids["hours"].hint_text = "Hours already set: " + self.hoursField
            self.timeDialog.content_cls.ids["minutes"].hint_text = "Minutes already set: " + self.minutesField
        self.timeDialog.open()

    def accept_post_time(self):
        if self.timeDialog.content_cls.ids["hours"].text.isdigit():
            self.hoursField = self.timeDialog.content_cls.ids["hours"].text
        if self.timeDialog.content_cls.ids["minutes"].text.isdigit():
            self.minutesField = self.timeDialog.content_cls.ids["minutes"].text
        self.timeDialog.dismiss()

    def alert_post(self):
        if self.alarmPost == False:
            self.display_alarm_dialog()
        else:
            self.alarmPost = True
            self.cancel_alarm()

    def create_alertDialog(self):
        self.alertDialog = MDDialogEdited(
            type="custom",
            content_cls=AlertDialogContent(),
            buttons=[MDIconButton(icon="backspace-outline", on_release=lambda x: self.alertDialog.dismiss()),
                     MDIconButton(icon="check-outline", on_release=lambda x: self.alarmStart_Stop())]
        )
        self.alertDialog.children[0].md_bg_color = 1, 0.2, 0.2, 0.5

    def display_alarm_dialog(self):
        if self.sell_post == False:
            self.alertDialog.children[0].md_bg_color = 1, 0.2, 0.2, 0.5
            self.alertDialog.open()
        else:
            self.alertDialog.text = "You cant mark sell post as alarm post!"
            self.alertDialog.buttons = [MDRoundFlatButton(text="Ok", on_release=lambda x: self.alertDialog.dismiss())]
            self.alertDialog.open()

    def alarmStart_Stop(self):
        if self.alarmPost == False:
            self.makeAlarmPost()
        else:
            self.cancel_alarm()

    def makeAlarmPost(self):
        texField = self.ids["textField"]
        texField.color_mode = "custom"

        self.ids["bgImage"].source = "alarm.png"

        texField.line_color_focus = (1, 0, 0)
        texField.line_color_normal = (1, 0, 0)
        texField.text_color = (1, 0, 0)
        self.alarmPost = True
        self.alertDialog.dismiss()

    def create_alertEndDialog(self):
        self.alertEndDialog = MDDialogEdited(
            type="custom",
            title="Wyłączono post alarmowy",
            buttons=[MDIconButton(icon="check-outline", on_release=lambda x: self.alertEndDialog.dismiss())]
        )
        self.alertEndDialog.children[0].md_bg_color = 0.2, 0.5, 1, 1

    def cancel_alarm(self, on_leave=False, on_send=False):

        App.get_running_app().theme_cls.primary_palette = "Blue"
        texField = self.children[1].children[0].children[0]
        texField.color_mode = "custom"
        texField.line_color_focus = 0.2, 0.5, 1
        texField.line_color_normal = 0.2, 0.5, 1
        texField.text_color = 0, 0, 0
        if on_leave == False:
            if on_send == False:
                self.alertEndDialog.open()
            self.ids["bgImage"].source = ""
            self.alarmPost = False
        else:
            pass
            # self.alarmPost = True
            # self.ids["bgImage"].source = "alarm.png"

    def back_to_main_screen(self, ):
        self.on_leave()
        self.manager.current = "MainScreen"
        self.usersPhotos = []
        self.listOfPhotos = []

    def add_photo(self):
        App.get_running_app().root.get_screen("PhotosGalleryScreen").creatingPost = True
        App.get_running_app().root.get_screen("PhotosGalleryScreen").mainData = CURRENT_USER_DATA
        App.get_running_app().root.get_screen("PhotosGalleryScreen").usersPhotos = self.usersPhotos
        self.manager.current = "PhotosGalleryScreen"
        # self.create_FileManager()
        # self.fileManager.show("/")

    def create_FileManager(self):
        self.fileManager = MDFileManager(
            select_path=self.fileManager_select_path,
            exit_manager=lambda x: self.fileManager.close(),
            preview=True, mipmap=False
        )

    def fileManager_select_path(self, path):
        self.fileManager.close()
        self.photoToSendPath = path
        self.create_photo_object(path)
        self.display_message_photo()

    def create_photo_object(self, path):
        photoFile = {"photo": open(path, "rb")}
        self.photoToSendObject = photoFile

    def display_message_photo(self):
        if self.photoToSendPath != None:
            imageWidget = self.children[1].children[1]
            imageWidget.source = self.photoToSendPath
            imageWidget.size_hint_x = 1
            imageWidget.size_hint_y = 1

    def reset_photo(self):
        imageWidget = self.children[1].children[1]
        imageWidget.source = ""
        imageWidget.size_hint_x = None
        imageWidget.size_hint_y = None
        imageWidget.size = (0, 0)

    def mark_post_as_sell(self):
        if self.alarmPost == False:
            self.sell_post_dialog = MDDialogEdited(
                text="Do you want to mark post as sell?" if self.sell_post == False else "Your post is already marked as sell. Do you want to unmark ?",
                buttons=[MDFillRoundFlatButton(text="yes", on_release=lambda x: self.accept_sell()),
                         MDRoundFlatButton(text="No", on_release=lambda x: self.sell_post_dialog.dismiss())]
            )
            self.sell_post_dialog.open()
        else:
            self.sell_post_dialog = MDDialogEdited(
                text="You cant mark alarm post as sell post!",
                buttons=[MDRoundFlatButton(text="Ok", on_release=lambda x: self.sell_post_dialog.dismiss())]
            )
            self.sell_post_dialog.open()

    def accept_sell(self):
        texField = self.children[1].children[0].children[0]
        if self.sell_post == False:
            self.sell_post = True
            texField.color_mode = "custom"
            texField.line_color_focus = 0, 1, 0
            texField.line_color_normal = 0, 1, 0
            texField.text_color = 0, 0, 0
        else:
            self.sell_post = False
            texField.color_mode = "custom"
            texField.line_color_focus = 0.2, 0.5, 1
            texField.line_color_normal = 0.2, 0.5, 1
            texField.text_color = 0, 0, 0
        self.sell_post_dialog.dismiss()


class UserScreen(Screen):
    text = StringProperty()
    username = StringProperty()
    userData = None
    friends = BooleanProperty(defaultvalue=False)
    back_to_main = False
    first_pre_enter = True
    fromMarker = False

    def on_pre_enter(self, *args):
        if self.first_pre_enter:
            self.create_main_widgets()

    def create_start_board(self):
        self.startBoard = Popup(background_color=[0, 0, 0, 0], title="",
                                separator_color=[0.2, 0.5, 1, 0])
        small_Popup = Popup(background_color=[0, 0, 0, 0], title="",
                            separator_color=[0.2, 0.5, 1, 0], size_hint_y=0.1, pos_hint={"top": 0.5})
        self.startBoard.add_widget(small_Popup)
        self.startBoard.ids["small_popup"] = small_Popup

    def show_start_board(self):
        if self.first_pre_enter:
            self.startBoard.open()
            progressBar = MDProgressBar(pos_hint={"right": 0, "top": 1})
            self.upgradeProgressObj = Clock.schedule_interval(self.upgradeProgress, 0.05)
            self.startBoard.ids["small_popup"].add_widget(progressBar)
            self.startBoard.ids["progress_bar"] = progressBar

    def upgradeProgress(self, dt=0):
        self.startBoard.ids["progress_bar"].value += 10

    def on_enter(self, *args):
        self.profileImage = self.ids["profilePhoto"]
        self.friends = False
        self.check_if_friends()
        self.photoToSendPath = None
        self.photoToSendObject = {"photo": None}
        self.check_ProfileImage()
        self.username = self.userData["username"]
        self.ids["friendsButton"].icon = icon = "account-plus" if self.friends == False else "account-check"
        self.ids["friendsButton"].on_release = lambda \
                x=1: self.send_friends_request() if self.friends == False else self.display_remove_friends_dialog()
        self.ids["topToolbar"].title = self.username
        if self.first_pre_enter:
            self.startBoard.ids["progress_bar"].value = 100
            self.startBoard.dismiss()
            self.upgradeProgressObj.cancel()
            self.first_pre_enter = False

    def create_main_widgets(self):
        # bgImage = kivyImage(source="xxx.png", size=(self.size[0], self.size[1]), allow_stretch=True, keep_ratio=False)
        topToolbar = MDTopAppBar(pos_hint={"top": 1})
        floatLayout = FloatLayout(size_hint_y=0.8)
        self.startBoard.ids["progress_bar"].value = 5
        profileImage = AsyncImageButton(source="person.png", pos_hint={"y": 0.3}, size_hint_x=1, size_hint_y=1)
        secondFloatLayout = FloatLayout()
        profilePhoto = AsyncImageButton(opacity=0, source="person.png", size_hint_y=None, size_hint_x=None,
                                        keep_ratio=False, allow_stretch=True, size=(400, 400))
        profilePhoto.on_press = lambda x=1: self.changeProfileImage()
        messageBtn = MDFloatingActionButton(icon="message", size=(80, 80), pos_hint={"x": 0.125, "y": 0.35}, text="",
                                            on_release=lambda x=1: self.send_private_message())
        self.startBoard.ids["progress_bar"].value = 30
        friendsBtn = MDFloatingActionButton(icon="account-plus" if self.friends == False else "account-check",
                                            pos_hint={"x": 0.325, "y": 0.35},
                                            text="")
        photosBtn = MDFloatingActionButton(icon="camera", pos_hint={"x": 0.525, "y": 0.35}, text="",
                                           on_release=lambda x=1: self.open_user_gallery())
        archiveBtn = MDFloatingActionButton(icon="archive", pos_hint={"x": 0.725, "y": 0.35}, text="")
        usersFriends = MDFloatingActionButton(icon="account-group", pos_hint={"x": 0.325, "y": 0.20}, text="",
                                              on_release=lambda x=1: self.display_all_users_friends())
        bottomToolbar = MDTopAppBar(type="top")
        bottomToolbar.left_action_items = [
            ["arrow-left-thick", lambda x=1: self.back_to_main_screen(back_to_main=True), "Wróć", "Wróć"]]
        bottomToolbar.right_action_items = [["logout", lambda x=1: self.logout(), "Logout", "Logout"]]
        self.startBoard.ids["progress_bar"].value = 50

        # self.add_widget(bgImage)
        # self.ids["Background_image_user"] = bgImage

        self.add_widget(topToolbar)
        self.add_widget(floatLayout)
        self.ids["firstFloat"] = floatLayout
        self.ids["firstFloat"].add_widget(profileImage)
        self.ids["profileImage"] = profileImage
        self.ids["profileImage"].add_widget(secondFloatLayout)
        self.ids["secondFloat"] = secondFloatLayout
        self.ids["secondFloat"].add_widget(profilePhoto)
        self.ids["profilePhoto"] = profilePhoto
        self.ids["profilePhoto"].center_x = Window.size[0] / 2
        self.ids["profilePhoto"].center_y = (Window.size[1] / 3) * 2
        self.ids["firstFloat"].add_widget(messageBtn)
        self.ids["firstFloat"].add_widget(friendsBtn)
        self.ids["firstFloat"].add_widget(photosBtn)
        self.ids["firstFloat"].add_widget(archiveBtn)
        self.ids["firstFloat"].add_widget(usersFriends)
        self.ids["friendsButton"] = friendsBtn
        self.ids["topToolbar"] = topToolbar
        self.add_widget(bottomToolbar)
        self.startBoard.ids["progress_bar"].value = 70

    def send_friends_request(self):
        if self.userData["username"] != USERNAME:
            data = {"action": "send_friends_request", "friendsRequestReciever": self.userData["id"]}
            friendRequest = requests.post(SERWER_ADRESS + "api_geoloc/", data=data, headers=HEADER)
            self.display_sent_dialog()

    def display_sent_dialog(self):
        self.sendDialog = MDDialogEdited(
            text=f"Friends request was sent to {self.userData['username']}",
            buttons=[MDFillRoundFlatIconButton(text="Ok", icon="check", on_release=lambda x: self.sendDialog.dismiss())]
        )
        self.sendDialog.open()

    def check_if_friends(self):
        for friend in CURRENT_USER_DATA["friends"]:
            if str(friend['friendUserId']) == str(self.userData["id"]):
                self.friends = True
                break

    def display_remove_friends_dialog(self):
        self.friends_remove_dialog = MDDialogEdited(
            title="Remove from friends?",
            buttons=[MDFillRoundFlatIconButton(text="Yes", icon="account-minus",
                                               on_release=lambda x: self.remove_from_friendslist()),
                     MDFillRoundFlatIconButton(text="No", icon="account-check",
                                               on_release=lambda *args: self.friends_remove_dialog.dismiss())
                     ]
        )
        self.friends_remove_dialog.open()

    def remove_from_friendslist(self):
        try:
            userToRemoveID =  self.userData.id
        except:
            userToRemoveID = self.userData["id"]
        data = {"action": "remove_from_friendslist", "removedFriend": userToRemoveID}
        friendRemove = requests.post(SERWER_ADRESS + "api_geoloc/", data=data, headers=HEADER)
        self.friends = False
        self.ids["friendsButton"].icon = "account-plus"
        self.friends_remove_dialog.dismiss()

    def back_to_main_screen(self, **kwargs):
        global MAIN_MAP
        MAIN_MAP.do_update(1)
        self.manager.current = "MainScreen"
        if kwargs["back_to_main"] == True:
            self.back_to_main = True

    def on_leave(self, *args, **kwargs):
        global MAIN_MAP
        MAIN_MAP.do_update(0)
        App.get_running_app().root.get_screen("MainScreen").marker_in_use = None

        # Displayed_map_button wskazuje że jesteśmy w trybie "Show-all-users-on-map" czyli aby nie wracać do dialogu otwartego
        Displayed_Map_Button = App.get_running_app().root.get_screen("MainScreen").Displayed_Map_Button

        if self.back_to_main == True and self.fromMarker == False and self.username != CURRENT_USER_DATA[
            "username"] and Displayed_Map_Button == False:
            # App.get_running_app().root.get_screen("MainScreen").show_allUsers_dialog(type="user")
            self.back_to_main = False
        else:
            self.fromMarker = False
        self.username = ""
        self.userData = None

    def null(self):
        pass

    def send_private_message(self):
        if self.userData["username"] != USERNAME:
            thread = {"reciever": self.userData["id"], "recieverName": self.userData["username"], "x": ""}
            App.get_running_app().root.get_screen("CurrentThreadMessagesScreen").show_start_board()
            App.get_running_app().root.get_screen("CurrentThreadMessagesScreen").thread = thread
            App.get_running_app().root.get_screen("CurrentThreadMessagesScreen").backToUser = False
            App.get_running_app().root.get_screen("CurrentThreadMessagesScreen").userData = self.userData
            self.manager.current = "CurrentThreadMessagesScreen"

    # Profile Image
    def check_ProfileImage(self):
        self.ids["profileImage"].opacity = 1
        if self.username == CURRENT_USER_DATA["username"]:
            if CURRENT_USER_DATA["profilePhoto"] == None:
                self.profileImage.source = "person.png"
            else:
                imagePath = CURRENT_USER_DATA["profilePhoto"]
                self.profileImage.source = imagePath
                self.profileImage.opacity = 1
        else:
            if self.userData["profilePhoto"] == None:
                self.profileImage.source = "person.png"
            else:
                self.profileImage.source = self.userData["profilePhoto"]
                self.profileImage.opacity = 1

    def ask_for_profile_image(self, adress):
        pass

    def ask_if_change_profile_image(self):
        self.profileImageDialog = MDDialogEdited(
            text="Do you want to change your profile image?",
            buttons=[MDFillRoundFlatIconButton(icon="check", text="Yes", on_release=lambda x: self.add_photo()),
                     MDFillRoundFlatIconButton(icon="backspace-reverse-outline", text="No",
                                               on_release=lambda x: self.profileImageDialog.dismiss()),
                     MDRoundFlatIconButton(icon="trash-can-outline", text="delete",
                                           on_release=lambda x: self.delete_profile_photo())]
        )
        self.profileImageDialog.open()

    def changeProfileImage(self):
        if self.userData["username"] == CURRENT_USER_DATA["username"]:
            self.ask_if_change_profile_image()

    def add_photo(self):
        self.profileImageDialog.dismiss()
        self.create_FileManager()
        self.fileManager.show(primary_ext_storage)

    def create_FileManager(self):
        self.fileManager = MDFileManager(
            select_path=self.fileManager_select_path,
            exit_manager=lambda x: self.fileManager.close(),
            preview=True
        )

    def fileManager_select_path(self, path):
        self.fileManager.close()
        self.photoToSendPath = path
        self.photoObject = self.create_photo_object(path)
        self.send_photo()

    def create_photo_object(self, path):
        global CURRENT_USER_DATA
        self.crop_photo(path)
        photoFile = {"profilePhoto": open(f"profile_crop_{CURRENT_USER_DATA['id']}.png", "rb"),
                     "profilePhotoMini": open(f"profile_crop_mini_{CURRENT_USER_DATA['id']}.png", "rb")}
        self.photoToSendObject = photoFile
        self.profileImage.source = f"profile_crop_{CURRENT_USER_DATA['id']}.png"
        return photoFile

    def send_photo(self):
        data = {"action": "change_profile_photo", "profilePhoto": self.photoObject}
        sendPost = requests.post(SERWER_ADRESS + "api_geoloc/", data=data, headers=HEADER, files=self.photoObject)

    def crop_photo(self, path):
        imageToCrop = Image.open(path)
        imageToCrop = self.convertToRectangle(imageToCrop)
        imageToCrop = imageToCrop.resize((300, 300))
        bigSize = (360, 360)
        mask = Image.new("L", bigSize, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + bigSize, fill=255)

        mask = mask.resize(imageToCrop.size, Image.ANTIALIAS)
        mask.save("mask.png")
        imageToCrop.putalpha(mask)
        output = ImageOps.fit(imageToCrop, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)

        backCircle = Image.open("user_circle.png")

        backCircle.paste(output, (75, 75), mask)
        backCircle.save(f"profile_crop_{CURRENT_USER_DATA['id']}.png")
        backCircle.save(f"profile_crop_mini_{CURRENT_USER_DATA['id']}.png")

        # draw = ImageDraw.Draw(mask)
        # draw.ellipse((-1, -1, 300, 300), outline="rgb(20%,50%,100%)", width=20)
        #
        # output = output.resize((60, 60))
        # output.save(f"profile_crop_mini_{CURRENT_USER_DATA['id']}.png")

    def convertToRectangle(self, image):
        if image.size[0] != image.size[1]:
            if image.size[0] > image.size[1]:
                cutSide = "horizontal"
            else:
                cutSide = "vertical"

            if cutSide == "horizontal":
                dif = (image.size[0] - image.size[1]) / 2
                border = (dif, 0, dif, 0)
            else:
                dif = (image.size[1] - image.size[0]) / 2
                border = (0, dif, 0, dif)

            imageRectangle = ImageOps.crop(image, border)

            return imageRectangle

        else:
            return image

    def delete_profile_photo(self):
        self.profileImageDialog.dismiss()
        data = {"action": "delete_profile_photo"}
        sendPost = requests.post(SERWER_ADRESS + "api_geoloc/", data=data, headers=HEADER)
        self.profileImage.source = "person.png"

    # Gallery

    def open_user_gallery(self):
        self.back_to_main = False
        App.get_running_app().root.get_screen("PhotosGalleryScreen").mainData = self.userData
        self.manager.current = "PhotosGalleryScreen"

    # Frieds
    def display_all_users_friends(self):
        usersFriendsList = self.request_for_users_friends()

    def request_for_users_friends(self):
        try:
            data = {"action": "get_all_users_friends", "requestedUserId": self.userData["id"]}
            all_users_friends = requests.get(SERWER_ADRESS + "api_geoloc/", data=data, headers=HEADER).json()

            App.get_running_app().root.get_screen("MainScreen").show_allUsers_dialog(list_of_users=all_users_friends,
                                                                                     globalUsers=False, otherSelf=self,
                                                                                     friendsList=True)
        except:
            pass

    def update_preview_dialog(self, side, list_of_users, type, otherSelf=None):
        App.get_running_app().root.get_screen("MainScreen").update_preview_dialog(side=side,
                                                                                  list_of_users=list_of_users,
                                                                                  type=type, otherSelf=self)

    # Logout

    def logout(self):
        self.manager.current = "MainScreen"
        App.get_running_app().root.get_screen("MainScreen").logout()


class CurrentThreadMessagesScreen(Screen):
    thread = None
    conversationContent = None
    open = False
    reciever = None
    fullConversationMode = False
    backToUser = False
    firstRun = True
    first_download = True
    firstRun_pre = True
    downloadedMessages = []
    current_downloaded_messages = []
    userData = None
    isRead = True
    messagesThreadList = []
    photoToSendObject = None

    # Rozwiązac problem pobierania info czy jest nowa wiadomość ! - sprawdzać czy isRead

    def on_pre_enter(self, *args):
        global UPDATE_ENABLED
        UPDATE_ENABLED = False
        self.open = True

        if self.firstRun_pre:
            self.create_main_widgets()
            # print(self.ids["messagesBottomToolbar"].children[1].children[0].children)
            # self.photo_button = self.ids["messagesBottomToolbar"].children[0].children[1]

        self.messagesLayout = self.ids["photosGridLayout"]
        self.fix_sender_reciever()
        self.mark_thread_as_read()
        # self.request_for_conversation_content()

        # thread = threading.Thread(target=self.request_for_conversation_content)
        # thread.start()
        self.request_for_conversation_content()
        self.update_widgets_open()

    def upgradeProgress(self, dt=0):
        self.startBoard.ids["progress_bar"].value += 10

    def on_enter(self, *args):

        if self.firstRun == True:
            # self.create_text_widgets_in_lists()

            self.firstRun = False

        # self.update_widgets_open()

        if self.fullConversationMode != True:
            self.checkMessages = Clock.schedule_interval(self.new_messages_thread, 2)
            self.update_widgets_if_new = Clock.schedule_interval(self.check_is_read_flag, 1)
        self.upgradeProgressObj.cancel()
        self.startBoard.dismiss()
        self.firstRun_pre = False
        Window.bind(on_key_down=self._on_keyboard_down)
        self.get_interlocutor_image()
        self.update_widgets_open()

    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        if self.ids["MessageTextField"].focus and keycode == 40:  # 40 - Enter key pressed
            self.send_message()

    def get_interlocutor_image(self):
        if "sender" in self.thread.keys():
            self.interlocutor = self.thread["sender"]
        else:
            self.interlocutor = self.thread["reciever"]

        if self.interlocutor == CURRENT_USER_DATA["id"]:
            self.interlocutor = self.thread["reciever"]

        if f"{self.interlocutor}.png" not in os.listdir("profile_mini/"):
            data = {"action": "get_specific_user", "id": self.interlocutor}
            interlocutorData = request = requests.get(SERWER_ADRESS + "api_geoloc/", data=data, headers=HEADER).json()

            if interlocutorData["profilePhotoMini"] != None:
                url = interlocutorData["profilePhotoMini"]
                r = requests.get(url, allow_redirects=True)
                open(f'profile_mini/{self.interlocutor}.png', 'wb').write(r.content)

        if f"{self.interlocutor}.png" in os.listdir("profile_mini/"):
            self.ids["messagesTopToolbar"].left_action_items = [
            [f'profile_mini/{self.interlocutor}.png', lambda x: self.display_interlocutor_profile({"id":self.interlocutor}),"Show interlocutor profile","Show interlocutor profile"]]
        else:
            self.ids["messagesTopToolbar"].left_action_items = [['person.png',lambda x: self.display_interlocutor_profile({"id": self.interlocutor}),"Show interlocutor profile","Show interlocutor profile"]]

    def create_start_board(self):
        self.startBoard = Popup(background_color=[0, 0, 0, 0], title="",
                                separator_color=[0.2, 0.5, 1, 0])
        small_Popup = Popup(background_color=[0, 0, 0, 0], title="",
                            separator_color=[0.2, 0.5, 1, 0], size_hint_y=0.1, pos_hint={"top": 0.5})
        self.startBoard.add_widget(small_Popup)
        self.startBoard.ids["small_popup"] = small_Popup

    def show_start_board(self):
        if self.firstRun_pre:
            self.startBoard.open()
            progressBar = MDProgressBar(pos_hint={"right": 0, "top": 1})
            self.upgradeProgressObj = Clock.schedule_interval(self.upgradeProgress, 0.05)
            self.startBoard.ids["small_popup"].add_widget(progressBar)
            self.startBoard.ids["progress_bar"] = progressBar

    def on_leave(self, *args):
        global UPDATE_ENABLED
        UPDATE_ENABLED = True
        self.thread = None
        self.first_download = True
        self.open = False
        self.reciever = None
        self.backToUser = False
        self.checkMessages.cancel()
        self.current_downloaded_messages = []
        self.update_widgets_if_new.cancel()
        self.ids["messagesBottomToolbar"].right_action_items[0] = ["camera-plus", lambda x: self.ask_if_add_photo(),
                                                                   "add_photo", "add_photo"]
        self.photoToSendObject = None
        self.ids["MessageTextField"].text = ""
        self.move_messages_to_lists()

        App.get_running_app().check_if_new_messages_alert()

    def create_main_widgets(self):
        # bgImage = kivyImage(source="xxx.png", size=(self.size[0], self.size[1]), allow_stretch=True, keep_ratio=False)
        topToolbar = MDTopAppBar(pos_hint={"top": 1})
        topToolbar.right_action_items = [
            ["page-previous", lambda x: self.download_full_conversation(), "Preview full conversation",
             "Preview full conversation"],
            ["trash-can-outline", lambda x: self.delete_conversation(), "Delete conversation", "Delete conversation"]]
        boxLayout = BoxLayout(pos_hint={"x": 0.05, "y": 0.2}, size_hint=(0.9, 0.70))
        scrollView = ScrollView(size_hint_y=0.9, pos_hint={"y": 0.05}, do_scroll_y=True, do_scroll_x=False)


        mdGridLayout = MDGridLayout(cols=1, adaptive_height=True, padding=(dp(10), dp(10)), spacing=dp(10),size_hint_y= None)


        mdGridLayout.height = mdGridLayout.minimum_height
        textFieldInput = MDTextField(icon_right="comment-text", multiline=True, mode="fill",
                                     hint_text="Wpisz wiadomosć", pos_hint={"x": 0.1, "y": 0.12}, size_hint_x=0.8,
                                     line_color_normal=(0.2, 0.5, 1))
        textFieldInput.fill_color_normal = (0.2, 0.5, 1, 0.3)
        textFieldInput.fill_color_focus = (0.2, 0.5, 1, 0.2)
        textFieldInput.icon_right_color = "app.theme_cls.primary_color"
        textFieldInput.text_color_normal = (0, 0, 0, 0.9)
        textFieldInput.text_color_focus = (0, 0, 0, 0.9)
        textFieldInput.hint_text_color_normal = (0, 0, 0, 0.5)
        # Dodać dodawanie enterów co ileś znaków do treści wiadomości !!!

        bottomToolbar = MDTopAppBar(type="top")
        bottomToolbar.left_action_items = [["arrow-left-thick", lambda x: self.back_to_main_screen(), "Wróć", "Wróć"]]
        bottomToolbar.right_action_items = [
            ["camera-plus", lambda x: self.ask_if_add_photo(), "add_photo", "add_photo"],
            ["send", lambda x: self.send_message(), "Wyślij", "Wyślij"]]

        # self.add_widget(bgImage)
        # self.ids["Background_image"] = bgImage
        self.add_widget(topToolbar)
        self.add_widget(boxLayout)
        self.ids["BoxLayoutID"] = boxLayout
        self.ids["BoxLayoutID"].add_widget(scrollView)
        self.ids["messagesScrollView"] = scrollView
        self.ids["messagesScrollView"].add_widget(mdGridLayout)
        self.ids["photosGridLayout"] = mdGridLayout

        self.add_widget(textFieldInput)
        self.ids["MessageTextField"] = textFieldInput

        self.add_widget(bottomToolbar)
        self.ids["messagesTopToolbar"] = topToolbar
        self.ids["messagesBottomToolbar"] = bottomToolbar

    def create_text_widgets_in_lists(self):
        self.messageWidgets = []
        self.imagesWidgets = []
        for x in range(16):
            textLayout = AnchorLayout(size_hint_y=None)
            widgetText = MDFillRoundFlatIconButton(icon="person.png", md_bg_color=(1, 1, 1, 1),size_hint_y=0.8,size_hint_x=None)
            textLayout.add_widget(widgetText)

            imageLayout = AnchorLayout(size_hint_y=None)
            widgetImage = MDSmartTile(size_hint_x=None, size_hint_y=None, adaptive_size=True, size=(Window.size[0]/3, Window.size[0]/3))
            imageLayout.add_widget(widgetImage)

            self.messageWidgets.append(textLayout)
            self.imagesWidgets.append(imageLayout)

    def update_widgets_open(self):
        self.move_messages_to_lists()
        if self.downloadedMessages != "None":

            self.current_downloaded_messages = self.downloadedMessages.copy()

            for message_new in self.downloadedMessages:
                if message_new["messageText"] != "":
                    textWidget = self.messageWidgets.pop()
                    texWidgetReady = self.fill_text_widget(textWidget, message_new)

                    # layout = AnchorLayout(size_hint_y=None,anchor_x= "left")
                    # layout.add_widget(texWidgetReady)

                    # self.messagesLayout.add_widget(layout)
                    # Napisać to z użyciem Anchorlayoutu !! Anchor layout nie może mieć po prostu size hinta_y !! :)

                    # self.messagesLayout.add_widget(texWidgetReady)
                    # self.messagesLayout.remove_widget(texWidgetReady)
                    self.messagesLayout.add_widget(texWidgetReady)


                imageSource = message_new["image"]
                if imageSource != None:
                    imageWidgetToFill = self.imagesWidgets.pop()

                    imageWidgetToAdd = self.fill_image_widget(imageWidgetToFill, message_new)
                    self.messagesLayout.add_widget(imageWidgetToAdd)


        if self.messagesLayout.children:
            self.ids["messagesScrollView"].scroll_to(self.messagesLayout.children[0])

    def fill_text_widget(self, textAnchor, message):
        global USERNAME
        textWidget = textAnchor.children[0]
        sender = message["senderName"]
        time = message["messageDate"][:19].replace("T", "  ")
        text = message["messageText"]

        textWidget.text = f"           {sender.title()}       {time}  \n{text}"
        textWidget.md_bg_color = (0.2, 0.6, 1, 1) if sender == USERNAME else (0.2, 0.8, 0.6, 1)
        # textWidget.on_release = lambda x=1: self.display_interlocutor_profile(message)
        textWidget.rounded_button = False
        textWidget.multiline = True
        # textWidget.size_hint_y = 1


        if message["sender"] != CURRENT_USER_DATA["id"]:
            if f"{message['sender']}.png" in os.listdir("profile_mini/"):
                textWidget.icon = f"profile_mini/{message['sender']}.png"
        else:
            if f"profile_crop_{CURRENT_USER_DATA['id']}.png" in os.listdir():
                textWidget.icon = f"profile_crop_{CURRENT_USER_DATA['id']}.png"
            else:
                textWidget.icon = "post.png"

        textAnchor.anchor_x = "right" if sender == USERNAME else "left"

        textWidget.height = 87 + (45 * text.count("\n"))

        textAnchor.height = 87 + (55 * text.count("\n"))


        return textAnchor

    # def download_or_return_mini_profile(self,photoSmallAdress):
    #     photoAdress = SERWER_ADRESS+"media/" + photoSmallAdress
    #     photoName = photoAdress.split("/")[-1]
    #     for file in os.listdir("gallery_images_cache/"):
    #         if file == photoName:
    #             try:
    #                 image = Image.open(f"gallery_images_cache/{photoName}")
    #                 return f"gallery_images_cache/{photoName}"
    #             except:
    #                 continue
    #     # If not return:
    #     try:
    #         photoRequest = requests.get(photoAdress,headers=HEADER,stream=True)
    #
    #         with open(f"gallery_images_cache/{photoName}","wb") as photoToSave:
    #             photoToSave.write(photoRequest.content)
    #
    #         return f"gallery_images_cache/{photoName}"
    #     except:
    #         return "post.png"

    def display_interlocutor_profile(self, message):
        App.get_running_app().root.get_screen("UserScreen").show_start_board()
        data = {"action": "get_specific_user", "id": message["id"]}
        userData = request = requests.get(SERWER_ADRESS + "api_geoloc/", data=data, headers=HEADER).json()
        App.get_running_app().root.get_screen("UserScreen").userData = userData
        App.get_running_app().root.current = "UserScreen"
        App.get_running_app().root.get_screen("UserScreen").fromMarker = True

    def fill_image_widget(self, imageAnchor, message_new):
        image = imageAnchor.children[0]
        imageSource = message_new["image"]
        sender = message_new["senderName"]
        imageAdress = imageSource
        image.source = imageAdress
        image.on_release = lambda x=1: self.display_photo(imageAdress)
        imageAnchor.anchor_x = "right" if sender == USERNAME else "left"
        imageAnchor.height = image.height

        return imageAnchor

    def create_FileManager(self):
        self.fileManager = MDFileManager(
            select_path=self.fileManager_select_path,
            exit_manager=lambda x: self.fileManager.close(),
            preview=True
        )

    def create_image_popup(self, imageSource=""):
        self.asyncImage = AsyncImage()
        self.popupImage = PopupImp(background_color=[0, 0, 0, 0],
                                   separator_color=[0.2, 0.5, 1, 1], content=self.asyncImage,
                                   on_touch_move=lambda *args: self.popupImage.dismiss()
                                   )

    def create_one_message_widget(self, message):
        global USERNAME
        sender = message["senderName"]
        time = message["messageDate"][:19].replace("T", "  ")
        text = message["messageText"]

        widget = MDFillRoundFlatIconButton(text=f"           {sender.title()}       {time}  \n      {text}",
                                           halign="right" if sender == USERNAME else "left",
                                           theme_text_color="Custom",
                                           text_color=(0, 0, 0, 1)
                                           )
        widget.md_bg_color = (0.2, 0.6, 1, 1) if sender == USERNAME else (0.2, 0.8, 0.6, 1)
        widget.rounded_button = False
        widget.icon = "post.png"

        # if message["senderImageAdress"] != None:
        #     widget.icon = self.download_or_return_mini_profile(message["senderImageAdress"])
        # else:
        #     widget.icon = "post.png"

        # Adding Image widget
        imageSource = message["image"]
        if imageSource != None:
            imageAdress = imageSource
            image = MDSmartTile(source=imageAdress, size_hint_x=None, size_hint_y=None,
                                on_release=lambda x: self.display_photo(imageAdress))
        else:
            image = None

        return widget, image

    def create_ask_image_add_dialog(self):
        self.askImageAddDialog = MDDialogEdited(
            text="",
            buttons=[MDFillRoundFlatButton(text="yes", on_release=lambda x: self.add_photo()),
                     MDRoundFlatButton(text="No", on_release=lambda x: self.askImageAddDialog.dismiss())]
        )

    def update_text_widgets(self, fullConversation=False):
        if fullConversation == False:
            if self.downloadedMessages != "None":
                for message_new in self.downloadedMessages:
                    is_new = True
                    for message in self.current_downloaded_messages:
                        if message["id"] == message_new["id"]:
                            is_new = False
                    if is_new:
                        if len(self.messagesLayout.children) >= 14:
                            messageWidgetToRemove = self.messagesLayout.children[-1]
                            self.messagesLayout.remove_widget(messageWidgetToRemove)
                            if isinstance(messageWidgetToRemove.children[0], MDFillRoundFlatIconButton):
                                self.messageWidgets.append(messageWidgetToRemove)
                            elif isinstance(messageWidgetToRemove.children[0], MDSmartTile):
                                self.imagesWidgets.append(messageWidgetToRemove)

                        if message_new["messageText"] != "" and message_new["messageText"] != "\n":
                            textwidgetToFill = self.messageWidgets.pop()

                            messageWidgetToAdd = self.fill_text_widget(textwidgetToFill, message_new)

                            print(messageWidgetToAdd.height)
                            self.messagesLayout.add_widget(messageWidgetToAdd)


                        imageSource = message_new["image"]

                        if imageSource != None:
                            imageWidgetToFill = self.imagesWidgets.pop()
                            imageWidgetToAdd = self.fill_image_widget(imageWidgetToFill, message_new)
                            self.messagesLayout.add_widget(imageWidgetToAdd)

                    else:
                        continue

                self.current_downloaded_messages = self.downloadedMessages.copy()

        else:
            self.move_messages_to_lists()

            for message_new in self.downloadedMessages:
                messageWidgetToAdd, imageToAdd = self.create_one_message_widget(message_new)
                self.messagesLayout.add_widget(messageWidgetToAdd)
                if imageToAdd != None:
                    self.messagesLayout.add_widget(imageToAdd)
        try:
            self.ids["messagesScrollView"].scroll_to(messageWidgetToAdd)
        except:
            pass

    def back_to_main_screen(self):
        if self.fullConversationMode != True:

            if self.backToUser == False:
                self.manager.current = "MainScreen"
            else:
                App.get_running_app().root.get_screen("UserScreen").userData = self.userData
                self.manager.current = "UserScreen"
        else:
            warningDialog = MDDialogEdited(text="Close full-conversation preview before leave")
            warningDialog.open()
            return

    def move_messages_to_lists(self):

        for message in [x for x in self.messagesLayout.children]:
            messageWidgetToRemove = message
            self.messagesLayout.remove_widget(messageWidgetToRemove)
            if isinstance(messageWidgetToRemove.children[0], MDFillRoundFlatIconButton):
                self.messageWidgets.append(messageWidgetToRemove)
            elif isinstance(messageWidgetToRemove.children[0], MDSmartTile):
                self.imagesWidgets.append(messageWidgetToRemove)

    def fix_sender_reciever(self):
        self.reciever = self.thread["reciever"] if self.thread["reciever"] != CURRENT_USER_DATA["id"] else self.thread[
            "sender"]
        self.recieverName = self.thread["recieverName"] if self.thread["recieverName"] != CURRENT_USER_DATA[
            "username"] else self.thread["senderName"]

    def request_for_conversation_content(self):
        if self.fullConversationMode != True:
            data = {"sender": CURRENT_USER_DATA["id"], "reciever": self.reciever, "recieverName": self.recieverName,
                    "action": "get_messages_from_thread",
                    "thread_id": self.thread["id"] if "id" in self.thread.keys() else None}
            self.downloadedMessages = requests.get(SERWER_ADRESS + "api_geoloc/", data=data, headers=HEADER).json()
            # print(self.downloadedMessages)
            # self.downloadedMessages = sorted(self.downloadedMessages,key= lambda x: x["messageDate"])
        if self.firstRun != True and self.fullConversationMode != True:
            self.update_text_widgets()

    def send_message(self):
        messageText = ""
        textSplit = self.ids["MessageTextField"]._split_smart(self.ids["MessageTextField"].text)

        for line in textSplit[0]:
            messageText += f"{line}\n"

        # messageText = messageText[:-1]

        if messageText != "" or self.photoToSendObject != None:
            data = {"sender": CURRENT_USER_DATA["id"], "reciever": self.reciever, "recieverName": self.recieverName,
                    "messageText": messageText, "action": "send_private_message",
                    "thread_id": self.thread["id"] if "id" in self.thread.keys() else None,
                    "photoObject": self.photoToSendObject}

            # if len(self.thread.keys()) > 2:
            #     sendMessageThread = threading.Thread(target=requests.post,
            #                                          kwargs={"url": SERWER_ADRESS + "api_geoloc/", "data": data,
            #                                                  "headers": HEADER, "files": self.photoToSendObject})
            #     sendMessageThread.start()
            # else:
            sendMessage = requests.post(SERWER_ADRESS + "api_geoloc/", data=data, headers=HEADER,
                                        files=self.photoToSendObject)
            self.photoToSendObject = None
            self.ids["messagesBottomToolbar"].right_action_items[0] = ["camera-plus", lambda x: self.ask_if_add_photo(),
                                                                       "add_photo", "add_photo"]
            self.ids["MessageTextField"].text = ""
            self.ids["MessageTextField"].disabled = True
            self.ids["MessageTextField"].disabled = False
            self.mark_thread_as_read()
            self.request_for_conversation_content()
            self.update_text_widgets()

    def mark_thread_as_read(self):
        try:
            if len(self.thread.keys()) > 2:
                if self.thread["lastSender"] != USERNAME:
                    self.thread["is_read"] = True
                    data = {"thread_to_mark_ID": self.thread['id'], "action": "mark_thread_as_read"}
                    markThreadThread = threading.Thread(target=requests.post,
                                                        kwargs={"url": SERWER_ADRESS + "api_geoloc/", "data": data,
                                                                "headers": HEADER})
                    markThreadThread.start()
        except:
            pass

    def delete_conversation(self):
        global CURRENT_USER_DATA
        if self.fullConversationMode == False:
            self.if_delete_Dialog = MDDialogEdited(text="Do you really want to delete conversation ?",
                                                   buttons=[MDFillRoundFlatButton(text="yes", on_release=lambda
                                                       x: self.send_delete_request()),
                                                            MDRoundFlatButton(text="No", on_release=lambda
                                                                x: self.if_delete_Dialog.dismiss())])
            self.if_delete_Dialog.open()
        else:
            warningDialog = MDDialogEdited(text="Close full-conversation preview before delete")
            warningDialog.open()

    def send_delete_request(self):
        global CURRENT_USER_DATA
        # Get ALL messages in conversation -
        data = {"action": "get_full_conversation", "sender": CURRENT_USER_DATA["id"], "reciever": self.reciever,
                "recieverName": self.recieverName}
        new_downloadedMessages = requests.get(SERWER_ADRESS + "api_geoloc/", data=data, headers=HEADER).json()
        self.downloadedMessages = new_downloadedMessages
        self.fullConversationMode = True

        list_of_messages_ids = ""
        for message in self.downloadedMessages:
            list_of_messages_ids += f"{message['id']},"

        data = {"action": "mark_thread_as_deleted", "messages_to_mark_as_deleted_id": list_of_messages_ids}
        markThread_deleted = requests.post(SERWER_ADRESS + "api_geoloc/", data=data, headers=HEADER)
        # CURRENT_USER_DATA["messagesThreads"].remove(self.thread)
        self.fullConversationMode = False
        self.if_delete_Dialog.dismiss()
        self.back_to_main_screen()

    def new_messages_thread(self, dt=0):
        self.messagesThreadList = [thread for thread in self.messagesThreadList if thread.is_alive()]
        if self.messagesThreadList == []:
            thread = threading.Thread(target=self.request_if_is_read)
            self.messagesThreadList.append(thread)
            self.messagesThreadList[-1].start()
        else:
            pass

    def check_if_new_messages(self, dt=0):
        try:
            if self.fullConversationMode != True:
                if self.fullConversationMode == False:
                    data = {"sender": CURRENT_USER_DATA["id"], "reciever": self.reciever,
                            "recieverName": self.recieverName, "action": "get_messages_from_thread",
                            "thread_id": self.thread["id"]}
                    new_downloadedMessages = requests.get(SERWER_ADRESS + "api_geoloc/", data=data,
                                                          headers=HEADER).json()
                    if len(self.downloadedMessages) < len(new_downloadedMessages):
                        self.downloadedMessages = new_downloadedMessages
                        self.on_leave()
                        self.on_enter()
                else:
                    pass
            pass
        except:
            pass

    def download_full_conversation(self):
        self.ask_if_download_full_conversation()

    def create_download_full_conv_dialog(self):
        self.downloadFullConvDialog = MDDialogEdited(
            text="Do you want to download and preview full conversation?",
            buttons=[MDFillRoundFlatButton(text="yes", on_release=lambda x: self.request_for_full_conversation()),
                     MDRoundFlatButton(text="No", on_release=lambda x: self.downloadFullConvDialog.dismiss())]
        )

    def ask_if_download_full_conversation(self):
        self.downloadFullConvDialog.open()

    def request_for_full_conversation(self):
        data = {"action": "get_full_conversation", "sender": CURRENT_USER_DATA["id"], "reciever": self.reciever,
                "recieverName": self.recieverName}
        new_downloadedMessages = requests.get(SERWER_ADRESS + "api_geoloc/", data=data, headers=HEADER).json()
        self.downloadedMessages = new_downloadedMessages
        self.fullConversationMode = True
        self.update_text_widgets(fullConversation=True)

        messageText = self.ids["MessageTextField"]
        messageText.disabled = True
        messageText.hint_text = ""
        self.backButton = MDFillRoundFlatIconButton(pos_hint={"x": 0.15, "y": 0.105}, size_hint=(0.5, 0.06),
                                                    text="Close full-conversation preview", icon="arrow-left-bold",
                                                    on_release=lambda x: self.close_full_conversation_preview(
                                                        self.backButton))
        self.backButton.id = "backButton"
        self.add_widget(self.backButton)
        self.downloadFullConvDialog.dismiss()

    def close_full_conversation_preview(self, button):
        self.remove_widget(self.backButton)
        self.remove_full_conv_widgets()
        # self.create_text_widgets_in_lists()

        self.fullConversationMode = False

        self.request_for_conversation_content()

        self.update_widgets_open()

        messageText = self.ids["MessageTextField"]
        messageText.disabled = False
        messageText.hint_text = "Wpisz wiadomość"


    def remove_full_conv_widgets(self):
        # self.messagesLayout.clear_widgets()
        for message in [x for x in self.messagesLayout.children]:
            self.messagesLayout.remove_widget(message)

    def request_if_is_read(self):
        if len(self.thread.keys()) > 2:
            data = {"sender": CURRENT_USER_DATA["id"], "reciever": self.reciever, "recieverName": self.recieverName,
                    "action": "check_if_thread_is_read",
                    "thread_id": self.thread["id"] if "id" in self.thread.keys() else None}
            lastMessage = requests.get(SERWER_ADRESS + "api_geoloc/", data=data, headers=HEADER).json()["lastMessage"]

            if self.first_download:
                self.isRead = False
                self.first_download = False
                return
            if lastMessage != self.current_downloaded_messages[-1]:
                self.isRead = False

    def check_is_read_flag(self, dt=0):
        if self.isRead == False:
            self.request_for_conversation_content()
            self.isRead = True

    def fileManager_select_path(self, path):
        self.create_photo_object(path)
        self.fileManager.close()

    def ask_if_add_photo(self):
        if self.photoToSendObject == None:
            self.askImageAddDialog.text = "Do you want to add image to your message ?"
        else:
            self.askImageAddDialog.text = "Do you want to remove image from your message ?"

        self.askImageAddDialog.open()

    def add_photo(self):
        self.askImageAddDialog.dismiss()

        if self.photoToSendObject == None:
            self.fileManager.show(primary_ext_storage)
            self.ids["messagesBottomToolbar"].right_action_items[0] = ["camera-off", lambda x: self.ask_if_add_photo(),
                                                                       "remove photo", "remove photo"]
        else:
            self.remove_photo()
            self.ids["messagesBottomToolbar"].right_action_items[0] = ["camera-plus", lambda x: self.ask_if_add_photo(),
                                                                       "add_photo", "add_photo"]

    def create_photo_object(self, path):
        global CURRENT_USER_DATA
        photoName = self.resize_photo(path)
        if photoName.startswith("/"):
            photoName = photoName[1:]

        if platform != "android":
            photoFile = {"photoObject": open(f"gallery_images_cache/{photoName}", "rb")}
        else:
            photoFile = {"photoObject": open(f"gallery_images_cache/{photoName}", "rb")}
        self.photoToSendObject = photoFile

    def resize_photo(self, path):
        imageToResize = Image.open(path)

        if platform != "android":
            photoName = path.split("\\")[-1]
        else:
            photoName = path.split("/")[-1]

        # photoName = path.split("/")[-1]

        if photoName.startswith("/") or photoName.startswith("\\"):
            photoName = photoName[1:]
        if imageToResize.size[0] > 1024 or imageToResize.size[1] > 1024:
            imageToResize.thumbnail((1024, 1024), Image.ANTIALIAS)

        if platform != "android":
            imageToResize.save(f"gallery_images_cache/{photoName}")
        else:
            imageToResize.save(f"gallery_images_cache/{photoName}")
        imageToResize.close()

        return photoName

    def remove_photo(self):
        self.photoToSendObject = None

    def display_photo(self, imageSource):
        self.asyncImage.source = imageSource
        self.popupImage.open()


class PhotosGalleryScreen(Screen):
    mainData = None
    usersPhotos = []
    photoComment = None
    photoToSendObject = None

    creatingPost = False
    previewingPost = False
    first_enter_pre = True
    first_enter = True
    pass

    def on_pre_enter(self, *args):
        self.addButton = self.children[0].children[0].children[0]

        if self.mainData["username"] != USERNAME:
            self.addButton.disabled = True
            self.addButton.opacity = 0
        else:
            self.addButton.disabled = False
            self.addButton.opacity = 1

        if self.first_enter_pre:
            self.create_FileManager()
            self.first_enter_pre = False

    def on_enter(self, *args):
        # Dodać czyszczenie gallery images cache
        self.photosGridLayout = self.ids["photosGridLayout"]
        if self.first_enter:
            self.create_photos_widgets()
            self.first_enter = False

        self.clear_gallery()
        if self.creatingPost == False:
            self.usersPhotos = self.ask_for_users_photos()
        else:
            self.add_photos_from_userList()

    def add_photos_from_userList(self):
        for number, photo in enumerate(self.usersPhotos):
            photoLabel = self.photosGridLayout.children[24 - number]
            photoLabel.source = photo["photoPath"]
            photoLabel.opacity = 1
            # photoLabel = SmartTileWithLabelImp(
            #     source=photo["photoPath"],
            #     imageComment="",
            #     imageAdress=photo["photoPath"]
            # )
            # self.photosGridLayout.add_widget(photoLabel)

    def ask_for_users_photos(self):
        if self.creatingPost == False and self.previewingPost == False:
            data = {"action": "get_all_gallery_photos", "user": self.mainData["id"]}
            photosFromServer = requests.get(SERWER_ADRESS + "api_geoloc/", data=data, headers=HEADER)

        elif self.previewingPost == True:
            data = {"action": "get_all_post_photos", "post": self.mainData["id"]}
            photosFromServer = requests.get(SERWER_ADRESS + "api_geoloc/", data=data, headers=HEADER)

        self.usersPhotos = photosFromServer.json()
        self.add_photos_widgets()

    def back_to_user_screen(self):
        if self.creatingPost == False and self.previewingPost == False:
            App.get_running_app().root.get_screen("UserScreen").userData = self.mainData
            self.manager.current = "UserScreen"
        elif self.creatingPost:
            self.manager.current = "CreatePostScreen"
        elif self.previewingPost:
            App.get_running_app().root.get_screen("PostScreen").data = self.mainData
            self.manager.current = "PostScreen"
            # Tu wrócić do okna przeglądania postu

    def create_photos_widgets(self):
        for widget in range(25):
            photoLabel = SmartTileWithLabelImp(opacity=0)
            self.photosGridLayout.add_widget(photoLabel)

    def add_photos_widgets(self):
        # Niezależnie od usera, ładują sie te same zdjęcia
        for number, photo in enumerate(self.usersPhotos):
            if number < 25:
                photoLabel = self.photosGridLayout.children[24 - number]
                if self.creatingPost == False:
                    photoLabel.source = photo["photoGalleryImage"]
                    photoLabel.text = photo["photoComment"] if self.previewingPost == False else ""
                    photoLabel.imageId = str(photo["id"])
                    photoLabel.imageComment = photo["photoComment"] if self.previewingPost == False else ""
                    photoLabel.imageAdress = photo["photoGalleryImage"]
                else:
                    photoLabel.source = photo["photoPath"]
                photoLabel.opacity = 1

    def display_full_image(self, title, image, id):
        # Przerobić to żeby był tylko 1 na poczatku
        self.popupImage = PopupImp(title=title, background_color=[0, 0, 0, 0],
                                   separator_color=[0.2, 0.5, 1, 1], content=AsyncImage(source=image),
                                   on_touch_move=lambda *args: self.popupImage.dismiss(), id=id
                                   )
        if USERNAME == self.mainData["username"]:
            self.button = MDFloatingActionButtonImage(icon="trash-can-outline", pos_hint={"x": 0.5, "y": 0.1},
                                                      imageId=self.popupImage.id)
            self.popupImage.children[0].add_widget(self.button)
        self.popupImage.open()

    def remove_photo_from_gallery(self, id):
        if self.creatingPost == False:
            self.delete_image_dialog.dismiss()
            data = {"action": "remove_photo_from_gallery", "photoId": id, }
            sendPost = requests.post(SERWER_ADRESS + "api_geoloc/", data=data, headers=HEADER,
                                     files=self.photoToSendObject)
            self.popupImage.children[0].remove_widget(self.button)
            self.popupImage.dismiss()
            self.clear_gallery()
            self.ask_for_users_photos()
        # Pierdoli się podczas usuwania zdjęć w trybie tworzenia postu.

    def display_delete_image_dialog(self, id):
        self.delete_image_dialog = MDDialogEdited(imageId=id, text="Delete image?",
                                                  buttons=[MDFillRoundFlatIconButton(icon="check-outline", text="Yes",
                                                                                     on_release=lambda
                                                                                         x: self.remove_photo_from_gallery(
                                                                                         self.delete_image_dialog.imageId)),
                                                           MDRoundFlatIconButton(icon="backspace-reverse-outline",
                                                                                 text="No", on_release=lambda
                                                                   x: self.delete_image_dialog.dismiss())
                                                           ]
                                                  )
        self.delete_image_dialog.open()

    def clear_gallery(self):
        # Czyli jak iterujemy po liście, to iterujemy po wciąż zmienianej liście !!
        for photo in self.photosGridLayout.children:
            photo.source = ""
            photo.text = ""
            photo.imageId = ""
            photo.imageComment = ""
            photo.imageAdress = ""
            photo.opacity = 0

    def add_photo_to_gallery(self):
        if self.mainData["username"] == USERNAME:
            self.fileManager.show(primary_ext_storage)

    def create_FileManager(self):
        self.fileManager = MDFileManager(
            select_path=self.fileManager_select_path,
            exit_manager=lambda x: self.fileManager.close(),
            preview=True
        )

    def fileManager_select_path(self, path):
        self.fileManager.close()
        self.create_photo_object(path)
        self.display_add_comment_widget()

    def create_photo_object(self, path):
        global CURRENT_USER_DATA
        photoName = self.resize_photo(path)
        self.resized_image_path = f"gallery_images_cache/{photoName}"
        photoFile = {"photoObject": open(f"gallery_images_cache/{photoName}", "rb")}
        self.photoToSendObject = photoFile["photoObject"]
        if self.creatingPost == False:
            self.photoToSendObject = photoFile

    def resize_photo(self, path):

        imageToResize = Image.open(path)

        if platform != "android":
            photoName = path.split("\\")[-1]
        else:
            photoName = path.split("/")[-1]

        # photoName = path.split("/")[-1]

        if photoName.startswith("/") or photoName.startswith("\\"):
            photoName = photoName[1:]

        if imageToResize.size[0] > 1024 or imageToResize.size[1] > 1024:
            imageToResize.thumbnail((1024, 1024), Image.ANTIALIAS)
            imageToResize.save(f"gallery_images_cache/{photoName}")
        else:

            imageToResize.save(f"gallery_images_cache/{photoName}")
        imageToResize.close()
        return photoName

    def display_add_comment_widget(self):
        if self.creatingPost == False:
            self.add_comment_dialog = MDDialogEdited(
                type="custom",
                content_cls=PhotoGalleryDialogContent(),
                buttons=[MDFillRoundFlatIconButton(icon="check-outline",
                                                   text="Send" if self.creatingPost == False else "Add photo",
                                                   on_release=lambda x: self.accept_comment()),
                         MDRoundFlatIconButton(icon="check-outline", text="Leave",
                                               on_release=lambda x: self.abandon_add())
                         ]
            )
            self.add_comment_dialog.open()
        else:
            self.accept_comment()

    def accept_comment(self):
        if self.creatingPost == False:
            self.photoComment = self.add_comment_dialog.ids["spacer_top_box"].children[0].children[0].text
            self.add_comment_dialog.dismiss()
        self.send_photo_to_gallery()

    def send_photo_to_gallery(self):
        if self.creatingPost == False:
            data = {"action": "add_photo_to_gallery", "photoObject": self.photoToSendObject,
                    "photoComment": self.photoComment}
            sendPost = requests.post(SERWER_ADRESS + "api_geoloc/", data=data, headers=HEADER,
                                     files=self.photoToSendObject)

            self.clear_gallery()
            self.ask_for_users_photos()
        else:
            photoData = {"photoGalleryImage": self.photoToSendObject, "photoPath": self.resized_image_path}
            self.usersPhotos.append(photoData)
            # photoLabel = SmartTileWithLabelImp(
            #     source=self.resized_image_path,
            #     text="",
            #     imageComment="",
            #     imageAdress=self.resized_image_path
            # )
            # self.photosGridLayout.add_widget(photoLabel)
            # self.ask_for_users_photos()
            self.add_photos_widgets()
        # self.photoToSendObject["photoObject"].close()

    def abandon_add(self):
        self.add_comment_dialog.dismiss()
        self.photoComment = None
        self.photoToSendObject = None

    def clear_cache(self):
        for file in os.listdir("gallery_images_cache/"):
            try:
                os.remove(f"gallery_images_cache/{file}")
            except:
                pass

    def on_leave(self, *args):
        self.resized_image_path = None
        self.photoToSendObject = None
        self.photoComment = None
        self.usersPhotos = []
        self.clear_gallery()
        # self.clear_cache()
        self.creatingPost = False
        self.previewingPost = False
        self.viewingPostGallery = False
        if self.creatingPost:
            App.get_running_app().root.get_screen("CreatePostScreen").usersPhotos.extend(self.usersPhotos)


################################################

class AlertDialogContent(BoxLayout):
    pass


class PlaceInfoDialogContent(BoxLayout):
    pass


class UsersScrollView(BoxLayout):
    pass


class PostTimeDialogContent(BoxLayout):
    pass


class DistanceDialogContent(BoxLayout):
    pass


class PhotoGalleryDialogContent(BoxLayout):
    pass


##############################################
class LeftIconWidget(OneLineAvatarListItem):
    pass


class LeftImageWidget(ThreeLineAvatarIconListItem):
    pass


class LeftImageWidgetOne(OneLineAvatarListItem):
    pass


class PreviewAllPostsItem(LeftImageWidget):
    divider = None
    source = StringProperty()
    postData = DictProperty()
    fromMarker = BooleanProperty()
    markerUsersList = ListProperty()

    def on_release(self):
        global HEADER
        try:
            data = self.unify_data()
            App.get_running_app().root.get_screen("PostScreen").show_start_board()
            App.get_running_app().root.get_screen("MainScreen").allPostsDialog.dismiss()
            App.get_running_app().root.get_screen("MainScreen").dialog_opened = False
            App.get_running_app().root.get_screen("PostScreen").requestData = data
            App.get_running_app().root.get_screen("PostScreen").data = self.postData
            App.get_running_app().root.get_screen("PostScreen").fromMarker = self.fromMarker
            App.get_running_app().root.current = "PostScreen"
        except:
            pass

    def unify_data(self):
        lat, lon = self.postData["lat"].split("."), self.postData["lon"].split(".")
        lat, lon = f"{str(int(lat[0]) - 90)}.{lat[1]}", f"{str(int(lon[0]) - 180)}.{lon[1]}"
        unified_data = {"lat": lat, "lon": lon, "id": self.postData["id"], "action": "get_specific_post",
                        "alarmPost": self.postData["alarmPost"]}
        return unified_data


class MenuIconListItem(OneLineAvatarIconListItem):
    divider = None
    source = StringProperty()
    icon = StringProperty()
    postData = DictProperty()
    fromMarker = BooleanProperty()
    markerUsersList = ListProperty()


class PreviewAllUsersItem(LeftImageWidget):
    divider = None
    source = StringProperty()
    userData = DictProperty()
    fromMarker = BooleanProperty()
    otherSelf = ObjectProperty()
    secondary_text = StringProperty()
    tertiary_text = StringProperty()
    type = StringProperty()
    postData = DictProperty()
    markerUsersList = ListProperty()
    thread = ObjectProperty()
    requestingUserData = ObjectProperty()

    def on_release(self):
        if self.source != "":
            if self.type == "user":
                global HEADER
                if self.otherSelf != None:
                    self.otherSelf.allUsersDialog.dismiss()

                    App.get_running_app().root.get_screen("MainScreen").dialog_opened = False
                else:
                    App.get_running_app().root.get_screen("MainScreen").allUsersDialog.dismiss()
                    App.get_running_app().root.get_screen("MainScreen").dialog_opened = False
                App.get_running_app().root.get_screen("UserScreen").show_start_board()
                App.get_running_app().root.get_screen("UserScreen").userData = self.userData
                App.get_running_app().root.get_screen("UserScreen").fromMarker = self.fromMarker
                App.get_running_app().root.current = "UserScreen"
            elif self.type == "post":
                global HEADER
                try:
                    data = self.unify_data()
                    App.get_running_app().root.get_screen("PostScreen").show_start_board()
                    App.get_running_app().root.get_screen("MainScreen").allUsersDialog.dismiss()
                    App.get_running_app().root.get_screen("MainScreen").dialog_opened = False
                    App.get_running_app().root.get_screen("PostScreen").requestData = data
                    App.get_running_app().root.get_screen("PostScreen").data = self.postData
                    App.get_running_app().root.get_screen("PostScreen").fromMarker = self.fromMarker
                    App.get_running_app().root.current = "PostScreen"
                except:
                    pass

            elif self.type == "message":
                App.get_running_app().root.get_screen("CurrentThreadMessagesScreen").show_start_board()
                App.get_running_app().root.get_screen("MainScreen").allUsersDialog.dismiss()
                App.get_running_app().root.get_screen("CurrentThreadMessagesScreen").thread = self.thread
                App.get_running_app().root.current = "CurrentThreadMessagesScreen"

            elif self.type == "notifications":
                App.get_running_app().root.get_screen("MainScreen").accept_or_deny_friend_request_dialog(
                    self.requestingUserData)

    def unify_data(self):
        lat, lon = self.postData["lat"].split("."), self.postData["lon"].split(".")
        lat, lon = f"{str(int(lat[0]) - 90)}.{lat[1]}", f"{str(int(lon[0]) - 180)}.{lon[1]}"
        unified_data = {"lat": lat, "lon": lon, "id": self.postData["id"], "action": "get_specific_post",
                        "alarmPost": self.postData["alarmPost"]}
        return unified_data


class ShowMoreUsersItem(LeftImageWidget):
    divider = None
    source = StringProperty()
    userData = DictProperty()


class users_post_Choose_dialog(LeftImageWidgetOne):
    divider = None
    source = StringProperty()
    choose = StringProperty()
    usersList = ListProperty()
    postsList = ListProperty()
    marker = ObjectProperty()

    def on_release(self):
        if self.choose == "user":
            if len(self.usersList) > 0:
                App.get_running_app().root.get_screen("MainScreen").choose_user_post_dialog.dismiss()
                App.get_running_app().root.get_screen("MainScreen").show_allUsers_dialog(list_of_users=self.usersList,
                                                                                         globalUsers=False,
                                                                                         fromMarker=True,
                                                                                         marker=self.marker,
                                                                                         type="user")
        elif self.choose == "post":
            if len(self.postsList) > 0:
                App.get_running_app().root.get_screen("MainScreen").choose_user_post_dialog.dismiss()
                App.get_running_app().root.get_screen("MainScreen").show_allUsers_dialog(list_of_posts=self.postsList,
                                                                                         globalPosts=False,
                                                                                         fromMarker=True,
                                                                                         marker=self.marker,
                                                                                         type="post")


class MDDialogEdited(MDDialog):
    imageId = StringProperty()
    listOfUsers = ListProperty()
    listOfPosts = ListProperty()
    otherSelf = ObjectProperty()
    friends_requests = ListProperty()
    request_sender = ObjectProperty()
    messagesThreads = ListProperty()

    def on_pre_open(self):
        if App.get_running_app().root.get_screen("MainScreen").allUsersDialog.ids["positionButton"].enabled == False:
            App.get_running_app().root.get_screen("MainScreen").allUsersDialog.ids["positionButton"].on_release()
        if App.get_running_app().root.get_screen("MainScreen").allUsersDialog.ids["homeButton"].enabled == False:
            App.get_running_app().root.get_screen("MainScreen").allUsersDialog.ids["homeButton"].on_release()
        if App.get_running_app().root.get_screen("MainScreen").allUsersDialog.ids["workButton"].enabled == False:
            App.get_running_app().root.get_screen("MainScreen").allUsersDialog.ids["workButton"].on_release()

    def on_dismiss(self):
        global MAIN_MAP
        MAIN_MAP.do_update(0)
        App.get_running_app().root.get_screen("MainScreen").marker_in_use = None
        App.get_running_app().root.get_screen("MainScreen").touchList = [0, 0]
        App.get_running_app().root.get_screen("MainScreen").dialog_opened = False

        # for item in self.items:
        #     item.opacity = 0

        # App.get_running_app().root.get_screen("MainScreen").listOfExcludedAreas = []

        # App.get_running_app().root.get_screen("MainScreen").previewDialogListStatus = [0,8]


screenManager = ScreenManager()
screenManager.add_widget(LoginScreen(name='Login'))
screenManager.add_widget(MainScreen(name='MainScreen'))
screenManager.add_widget(PostScreen(name="PostScreen"))
screenManager.add_widget(UserScreen(name="UserScreen"))
screenManager.add_widget(CreatePostScreen(name="CreatePostScreen"))
screenManager.add_widget(CurrentThreadMessagesScreen(name="CurrentThreadMessagesScreen"))
screenManager.add_widget(RegisterScreen(name="RegisterScreen"))
screenManager.add_widget(PhotosGalleryScreen(name="PhotosGalleryScreen"))


class MainApp(MDApp):
    animate_run = False
    animate_friends_run = False
    animation_messages = None
    animation_friends = None
    first_update = True

    request_number = 0

    windowSize = Window.size
    listOfArear = ["user", "home", "work"]

    # MAP
    # def on_start(self):

    def update_all_data(self, dt=0):
        global USERS_IN_DISTANCE, POSTS_IN_DISTANCE, CURRENT_USER_DATA, CURRENT_KMEANS_DATA, work_LAT, work_LON, home_LAT, home_LON, ALARM_POSTS, FIRST_UPDATE, DISTANCE, FRIENDS_ONLY, UPDATE_ENABLED, CURRENT_KMEANS_DATA_SPLIT, USERMARKER
        if self.request_number > 2:
            self.request_number = 0
        if UPDATE_ENABLED:
            data = {"lat": user_LAT, "lon": user_LON, "action": "update_user_pos", "home_lat": home_LAT,
                    "home_lon": home_LON, "work_lat": work_LAT, "work_lon": work_LON, "distance": DISTANCE,
                    "friendsOnly": FRIENDS_ONLY, "firstUpdate": self.first_update, "requestNumber": self.request_number}
            start = time.time()
            print("main request send")
            data_from_server = requests.post(SERWER_ADRESS + "api_geoloc/", data=data, headers=HEADER)
            end = time.time()
            print("main request recieved")
            print(end - start, "\n")
            # print(data_from_server.text)
            USERMARKER.user = CURRENT_USER_DATA
            USERS_IN_DISTANCE = data_from_server.json()["ordered_Users"]
            POSTS_IN_DISTANCE = data_from_server.json()["ordered_Posts"]
            CURRENT_USER_DATA = data_from_server.json()["currentUserData"]
            ALARM_POSTS = data_from_server.json()["alarmPosts"]
            CURRENT_KMEANS_DATA = data_from_server.json()["currentKmeansData"]

            # USERS_IN_DISTANCE,POSTS_IN_DISTANCE = self.prepare_geoOrdered_lists(USERS_IN_DISTANCE,POSTS_IN_DISTANCE)

            home_LAT = CURRENT_USER_DATA["home_LAT"] if CURRENT_USER_DATA["home_LAT"] != '' else "0.0"
            home_LON = CURRENT_USER_DATA["home_LON"] if CURRENT_USER_DATA["home_LON"] != '' else "0.0"
            work_LAT = CURRENT_USER_DATA["work_LAT"] if CURRENT_USER_DATA["work_LAT"] != '' else "0.0"
            work_LON = CURRENT_USER_DATA["work_LON"] if CURRENT_USER_DATA["work_LON"] != '' else "0.0"
            if FIRST_UPDATE == False:
                FIRST_UPDATE = True
            # if self.first_update:
            #     self.update_markers()
            #     self.first_update = False

            # if App.get_running_app().root.get_screen("MainScreen").firstEnter:
            #     App.get_running_app().root.get_screen("MainScreen").firstEnter = False
            #     App.get_running_app().root.get_screen("MainScreen").zoom_update(MAIN_MAP)

            self.request_number += 1
            self.check_if_new_messages_alert()

    def update_all_program_data_thread(self, dt=0):
        global UPDATE_ALL_DATA_THREAD
        if TOKEN != "":
            UPDATE_ALL_DATA_THREAD = [thread for thread in UPDATE_ALL_DATA_THREAD if thread.is_alive()]
            if UPDATE_ALL_DATA_THREAD == []:
                thread = threading.Thread(target=self.update_all_data)
                UPDATE_ALL_DATA_THREAD.append(thread)
                UPDATE_ALL_DATA_THREAD[-1].start()
        else:
            pass

        try:
            App.get_running_app().root.get_screen("MainScreen").zoom_update(MAIN_MAP)
        except:
            pass
    # def prepare_geoOrdered_lists(self,serializedListOfUsers,serializedListOfPosts):
    #     global user_LAT,user_LON
    #     orderedListOfUsers = []
    #     orderedListOfPosts = []
    #     userLat,userLon = user_LAT,user_LON
    #
    #     for otherUser in serializedListOfUsers:
    #         # otherUser = self.dictOfZoomPointsPositions["1"]["all_users_container"][userKey][0]
    #         otherUserLat,otherUserLon = otherUser["lat"].split("."),otherUser["lon"].split(".")
    #         otherUserLat[0],otherUserLon[0] = str(int(otherUserLat[0]) - 90),str(int(otherUserLon[0]) - 180)
    #         otherUserLat,otherUserLon = float(f"{otherUserLat[0]}.{otherUserLat[1]}"),float(f"{otherUserLon[0]}.{otherUserLon[1]}")
    #
    #         computedDistance = geopy.distance.geodesic((userLat,userLon), (otherUserLat,otherUserLon)).m
    #         otherUser["geoDistance"] = computedDistance
    #         orderedListOfUsers.append(otherUser)
    #
    #
    #     for otherPost in serializedListOfPosts:
    #         otherPostLat, otherPostLon = otherPost["lat"].split("."), otherPost["lon"].split(".")
    #         otherPostLat[0], otherPostLon[0] = str(int(otherPostLat[0]) - 90), str(int(otherPostLon[0]) - 180)
    #         otherPostLat, otherPostLon = float(f"{otherPostLat[0]}.{otherPostLat[1]}"), float(f"{otherPostLon[0]}.{otherPostLon[1]}")
    #         computedDistance = geopy.distance.geodesic((userLat, userLon), (otherPostLat, otherPostLon)).m
    #         otherPost["geoDistance"] = computedDistance
    #         orderedListOfPosts.append(otherPost)
    #
    #     orderedListOfUsers.sort(key=lambda x: x["geoDistance"])
    #     orderedListOfPosts.sort(key=lambda x: x["geoDistance"])
    #
    #
    #     return orderedListOfUsers,orderedListOfPosts

    # Robić to w osobnym wątku !
    def update_current_user_data_only_Thread(self, dt=0):
        global UPDATE_USER_ONLY, UPDATE_ENABLED

        if TOKEN != "" and UPDATE_ENABLED:
            UPDATE_USER_ONLY = [thread for thread in UPDATE_USER_ONLY if thread.is_alive()]
            if UPDATE_USER_ONLY == []:
                thread = threading.Thread(target=self.update_current_user_data_only)
                UPDATE_ALL_DATA_THREAD.append(thread)
                UPDATE_ALL_DATA_THREAD[-1].start()
        else:
            pass

    def update_current_user_data_only(self, dt=0):
        global CURRENT_USER_DATA
        data = {"lat": user_LAT, "lon": user_LON, "distance": "200", "action": "update_current_user_data_only",
                "home_lat": home_LAT,
                "home_lon": home_LON, "work_lat": work_LAT, "work_lon": work_LON}
        data_from_server = requests.get(SERWER_ADRESS + "api_geoloc/", data=data, headers=HEADER)
        CURRENT_USER_DATA = data_from_server.json()["currentUserData"]

    def update_user_marker(self, dt=0):
        global USERMARKER, user_LAT, user_LON, MAIN_MAP
        if USERMARKER != None:
            USERMARKER.lat = user_LAT
            USERMARKER.lon = user_LON
            # MAIN_MAP.do_update(3)

        else:
            pass

    def update_user_marker_thread(self, dt=0):
        global USER_MARKER_THREAD_LIST, UPDATE_ENABLED
        if TOKEN != "" and UPDATE_ENABLED:
            USER_MARKER_THREAD_LIST = [thread for thread in USER_MARKER_THREAD_LIST if thread.is_alive()]
            if USER_MARKER_THREAD_LIST == []:
                thread = threading.Thread(target=self.update_user_marker)
                USER_MARKER_THREAD_LIST.append(thread)
                USER_MARKER_THREAD_LIST[-1].start()

    # FRIENDS AND MESSAGES
    def check_if_new_messages_alert(self,
                                    dt=0):  # messagesy powinny być updejtowane w trakcie rozmowy bardzo często - poza otwartym onem rozmowy, mogą być updejtowane wolniej
        global CURRENT_USER_DATA, UPDATE_ENABLED
        if UPDATE_ENABLED:
            try:
                messagesButton = \
                App.get_running_app().root.get_screen("MainScreen").ids["bottomToolbar"].children[1].children[
                    2].children[0]
                friends_button = \
                App.get_running_app().root.get_screen("MainScreen").ids["bottomToolbar"].children[1].children[
                    2].children[1]
                for thread in CURRENT_USER_DATA["messagesThreads"]:

                    if thread["is_read"] == False and thread["lastSender"] != CURRENT_USER_DATA["username"]:
                        messagesButton.icon = "message-plus"
                        break

                    else:
                        messagesButton.icon = "message-outline"


                if CURRENT_USER_DATA["friendsRequests"] != []:
                    friends_button.icon = "bell-plus"
                else:
                    friends_button.icon = "bell-outline"
                    pass
            except:
                pass


    ########### GPS ###########
    gps_location = StringProperty()
    gps_status = StringProperty('Click Start to get GPS location updates')

    def request_android_permissions(self):
        from android.permissions import request_permissions, Permission

        # def callback(permissions, results):
        #     if all([res for res in results]):
        #         print("callback. All permissions granted.")
        #     else:
        #         print("callback. Some permissions refused.")

        request_permissions([Permission.ACCESS_COARSE_LOCATION,
                             Permission.ACCESS_FINE_LOCATION,
                             Permission.READ_EXTERNAL_STORAGE,
                             Permission.WRITE_EXTERNAL_STORAGE])

        # # To request permissions without a callback, do:
        # request_permissions([Permission.ACCESS_COARSE_LOCATION,
        #                      Permission.ACCESS_FINE_LOCATION])

    def start(self, minTime=100, minDistance=0):
        gps.start(minTime, minDistance)

    def stop(self):
        gps.stop()

    @mainthread
    def on_location(self, **kwargs):
        global user_LAT, user_LON
        user_LAT = f"{kwargs['lat']}"
        user_LON = f"{kwargs['lon']}"
        print(user_LAT,user_LON)

    @mainthread
    def on_status(self, stype, status):
        self.gps_status = 'type={}\n{}'.format(stype, status)

    def on_pause(self):
        gps.stop()
        return True

    def on_resume(self):
        gps.start(100, 0)
        pass

    def build(self):
        global TOKEN, UPDATE_ALL_PROGRAM_DATA_THREAD, UPDATE_USER_MARKER_THREAD, CHECK_IF_NEW_MESSAGES_ALERT, UPDATE_MARKERS

        try:
            gps.configure(on_location=self.on_location, on_status=self.on_status)
        except NotImplementedError:
            import traceback
            traceback.print_exc()
            self.gps_status = 'GPS is not implemented for your platform'
        if platform == "android":
            self.request_android_permissions()

        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.material_style = "M3"

        # Tu dodać warunki że musimy być zalogowani !
        Clock.schedule_interval(self.update_all_program_data_thread, 10)
        Clock.schedule_interval(self.update_user_marker_thread, 7)
        # Clock.schedule_interval(self.check_if_new_messages_alert, 3) # Nie działa

        # Robić to w osobnym wątku !
        # Clock.schedule_interval(self.update_current_user_data_only_Thread, 3)
        # Clock.schedule_interval(self.update_markers, 35)
        # Może dodać do mapu do_update, np co minute albo 2?

        return Builder.load_file('main_.kv')


MainApp().run()

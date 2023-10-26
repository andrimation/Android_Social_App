from kivymd.uix.textfield import MDTextFieldRect, MDTextField, MDTextFieldRound
from kivy.lang import Builder
from kivy.properties import (
    AliasProperty,
    BooleanProperty,
    ColorProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    OptionProperty,
    StringProperty,
)
from kivy.uix.screenmanager import Screen

Builder.load_string("""
<RegisterScreen>
    id:RegisterScreen
    name: 'RegisterScreen'
    # MapViewImp:
    #     id: BackgroundMap
    #     lat: 53.428
    #     lon: 14.527
    #     zoom: 15
    #     double_tap_zoom: True
    #     root_property: root
    #     __init__: root.create_animation()
    #     on_zoom: root.nothing()
    #     on_touch_down: root.nothing()
    #     pause_on_action: False


#    Video:
#        id: background2
#        pos: -1,-1
#        size_hint_y: 4
#        size_hint_x:3.2
#        source:"video_.avi"
#        allow_stretch:True
#        keep_ratio: False
#        state: "play"
#        options: {'allow_stretch': True,'eos': 'loop'}
#        allow_fullscreen: True
#        fullscreen: True
#        pos_hint: {"y":-1.5,"x":-1}
    MDCard:
        id: MainLoginCard
        size_hint: 0.95,0.95
        pos_hint: {"center_x":0.5,"center_y":0.5}
        elevation: 30
        padding: 25
        spacing: 25
        opacity: 0.5

    MDTextField:
        id: username
        hint_text: "Login *"
        size_hint_x: None
        width: MainLoginCard.width *0.7
        pos_hint: {"center_x":0.5,"center_y":0.85}

    MDTextField:
        id: user_password
        hint_text: "Password *"
        size_hint_x: None
        width: MainLoginCard.width *0.7
        pos_hint: {"center_x":0.5,"center_y":0.75}

    MDTextField:
        id: first_name
        hint_text: "First name *"
        size_hint_x: None
        width: MainLoginCard.width *0.7
        pos_hint: {"center_x":0.5,"center_y":0.65}

    MDTextField:
        id: second_name
        hint_text: "Second name *"
        size_hint_x: None
        width: MainLoginCard.width *0.7
        pos_hint: {"center_x":0.5,"center_y":0.55}

    MDTextField:
        id: age
        hint_text: "Age *"
        input_filter: "int"
        size_hint_x: None
        width: MainLoginCard.width *0.7
        pos_hint: {"center_x":0.5,"center_y":0.45}

    MDTextField:
        id: email
        hint_text: "E-mail adress *"
        size_hint_x: None
        width: MainLoginCard.width *0.7
        pos_hint: {"center_x":0.5,"center_y":0.35}

    MDTextField:
        id: phone
        hint_text: "Phone number"
        input_filter: "int"
        size_hint_x: None
        width: MainLoginCard.width *0.7
        pos_hint: {"center_x":0.5,"center_y":0.25}

    MDFillRoundFlatButton
        id: RegisterButton
        size_hint_x: None
        size_hint_y: 0.07
        width: MainLoginCard.width *0.6
        text: "Register"
        pos_hint: {"center_x":0.5,"center_y":0.16}
        md_bg_color: 0.2,0.5,1
        on_press: root.register_new_user()

    MDIconButton:
        id: BackToMainScreen
        icon: "arrow-left-thick"
        pos_hint: {"x":0.03,"y":0.03}
        on_release: root.back_to_login()
<Item>
    IconLeftWidget:
        icon: root.left_icon
""")

class RegisterScreen(Screen):
    pass
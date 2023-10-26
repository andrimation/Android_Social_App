# from kivy.app import App
# from kivy.lang import Builder
# from kivy.uix.recycleview import RecycleView
# from kivy.uix.boxlayout import BoxLayout
# from kivy.properties import StringProperty, ListProperty
# from kivymd.app import MDApp
# kv = '''
# <TwoButtons>:
#
#
# BoxLayout:
#     orientation: 'vertical'
#     Button:
#         size_hint_y: None
#         height: 48
#         text: 'Add widget to RV list'
#         on_release: rv.add()
#
#     RV:                          # A Reycleview
#         id: rv
#         viewclass: 'TwoButtons'  # The view class is TwoButtons, defined above.
#         data: self.rv_data_list  # the data is a list of dicts defined below in the RV class.
#         scroll_type: ['bars', 'content']
#         bar_width: 10
#         RecycleBoxLayout:
#             # This layout is used to hold the Recycle widgets
#             default_size: None, dp(48)   # This sets the height of the BoxLayout that holds a TwoButtons instance.
#
#             default_size_hint: 1, None
#             size_hint_y: None
#             height: self.minimum_height   # To scroll you need to set the layout height.
#             orientation: 'vertical'
# '''
#
# from kivymd.uix.list import OneLineAvatarListItem
#
# class TwoButtons(OneLineAvatarListItem):  # The viewclass definitions, and property definitions.
#     left_text = StringProperty()
#     right_text = StringProperty()
#
#
# class RV(RecycleView):
#     rv_data_list = ListProperty()  # A list property is used to hold the data for the recycleview, see the kv code
#
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.rv_data_list = [{'left_text': f'Left {i}', 'right_text': f'Right {i}'} for i in range(2)]
#         # This list comprehension is used to create the data list for this simple example.
#         # The data created looks like:
#         # [{'left_text': 'Left 0', 'right_text': 'Right 0'}, {'left_text': 'Left 1', 'right_text': 'Right 1'},
#         # {'left_text': 'Left 2', 'right_text': 'Right 2'}, {'left_text': 'Left 3'},...
#         # notice the keys in the dictionary correspond to the kivy properties in the TwoButtons class.
#         # The data needs to be in this kind of list of dictionary formats.  The RecycleView instances the
#         # widgets, and populates them with data from this list.
#
#     def add(self):
#         l = len(self.rv_data_list)
#         self.rv_data_list.extend(
#             [{'left_text': f'Added Left {i}', 'right_text': f'Added Right {i}'} for i in range(l, l + 1)])
#
#
# class RVTwoApp(MDApp):
#
#     def build(self):
#         return Builder.load_string(kv)
#
#
# RVTwoApp().run()

from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen

from kivymd.icon_definitions import md_icons
from kivymd.app import MDApp
from kivymd.uix.list import OneLineIconListItem


Builder.load_string(
    '''
#:import images_path kivymd.images_path


<CustomOneLineIconListItem>

    IconLeftWidget:
        icon: root.icon


<PreviousMDIcons>

    MDBoxLayout:
        orientation: 'vertical'
        spacing: dp(10)
        padding: dp(20)

        MDBoxLayout:
            adaptive_height: True

            MDIconButton:
                icon: 'magnify'

            MDTextField:
                id: search_field
                hint_text: 'Search icon'
                on_text: root.set_list_md_icons(self.text, True)

        RecycleView:
            id: rv
            key_viewclass: 'viewclass'
            key_size: 'height'

            RecycleBoxLayout:
                padding: dp(10)
                default_size: None, dp(48)
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'
'''
)


class CustomOneLineIconListItem(OneLineIconListItem):
    icon = StringProperty()


class PreviousMDIcons(Screen):

    def set_list_md_icons(self, text="", search=False):
        '''Builds a list of icons for the screen MDIcons.'''

        def add_icon_item(name_icon):
            self.ids.rv.data.append(
                {
                    "viewclass": "CustomOneLineIconListItem",
                    "icon": name_icon,
                    "text": name_icon,
                    "callback": lambda x: x,
                }
            )

        self.ids.rv.data = []
        for name_icon in md_icons.keys():
            if search:
                if text in name_icon:
                    add_icon_item(name_icon)
            else:
                add_icon_item(name_icon)


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = PreviousMDIcons()

    def build(self):
        return self.screen

    def on_start(self):
        self.screen.set_list_md_icons()


MainApp().run()

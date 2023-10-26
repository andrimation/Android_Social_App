from kivymd.uix.textfield import MDTextFieldRect, MDTextField
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

Builder.load_string(
    """
#:import images_path kivymd.images_path


<MDTextFieldMessageBubble>        
    canvas.before:

        Clear

        # Disabled line.
        Color:
            rgba:
                (self.line_color_normal \
                if self.line_color_normal else self.theme_cls.divider_color) \
                if root.mode == "line" else (0, 0, 0, 0)
        Line:
            points: self.x, self.y + dp(16), self.x + self.width, self.y + dp(16)
            width: 1
            dash_length: dp(3)
            dash_offset: 2 if self.disabled else 0

        # Active line.
        Color:
            rgba: self.line_color_normal if root.mode in ("line", "fill") and root.active_line else (0, 0, 0, 0)
        Rectangle:
            size: self._underline_width, dp(2)
            pos: self.center_x - (self._underline_width / 2), self.y + (dp(16) if root.mode != "fill" else 0)

        # Helper text.
        Color:
            rgba: self.error_color
        Rectangle:
            texture: self._helper_text_label.texture
            size:
                self._helper_text_label.texture_size[0] - (dp(3) if root.mode in ("fill", "rectangle") else 0), \
                self._helper_text_label.texture_size[1] - (dp(3) if root.mode in ("fill", "rectangle") else 0)
            pos: self.x + (dp(8) if root.mode == "fill" else 0), self.y + (dp(3) if root.mode in ("fill", "rectangle") else 0)

        # Texture of right Icon.
        Color:
            rgba: 0,0,1,1
        Rectangle:
            texture: self._icon_right_label.texture
            size: self._icon_right_label.texture_size if self.icon_right else (0, 0)
            pos:
                (self.width + self.x) - (self._icon_right_label.texture_size[1]) - dp(8), \
                self.center[1] - self._icon_right_label.texture_size[1] / 2 + (dp(8) if root.mode != "fill" else 0) \
                if root.mode != "rectangle" else \
                self.center[1] - self._icon_right_label.texture_size[1] / 2 - dp(4)

        Color:
            rgba: root.background_color
        RoundedRectangle:
            pos: self.x, self.y
            size: self.width, self.height + dp(8)
            radius: root.radius

        Color:
            rgba:
                (self._current_line_color if self.focus and not \
                self._cursor_blink else (0, 0, 0, 0))
        Rectangle:
            pos: (int(x) for x in self.cursor_pos)
            size: 1, -self.line_height

        # Hint text.
        Color:
            rgba: self._current_hint_text_color if not self.current_hint_text_color else self.current_hint_text_color
        Rectangle:
            texture: self._hint_lbl.texture
            size: self._hint_lbl.texture_size
            pos: self.x + (dp(8) if root.mode == "fill" else 0), self.y + self.height - self._hint_y

        Color:
            rgba:
                self.disabled_foreground_color if self.disabled else\
                (self.hint_text_color if not self.text and not\
                self.focus else self.foreground_color)

        # "rectangle" mode
        Color:
            rgba:
                self.text_color

        Line:
            width: dp(1) if root.mode == "rectangle" else dp(0.00001)
            points:
                (
                self.x + root._line_blank_space_right_point, self.top - self._hint_lbl.texture_size[1] // 2,
                self.right + dp(12), self.top - self._hint_lbl.texture_size[1] // 2,
                self.right + dp(12), self.y,
                self.x - dp(12), self.y,
                self.x - dp(12), self.top - self._hint_lbl.texture_size[1] // 2,
                self.x + root._line_blank_space_left_point, self.top - self._hint_lbl.texture_size[1] // 2
                )

    # "fill" mode.
    canvas.after:       
        Color:
            rgba: root._fill_color if root.mode == "fill" else (0, 0, 0, 0)
        RoundedRectangle:
            pos: self.x, self.y
            size: self.width, self.height + dp(8)
            radius: root.radius

    font_name: "Roboto" if not root.font_name else root.font_name
    foreground_color: self.theme_cls.text_color
    bold: False
    padding:
        0 if root.mode != "fill" else "8dp", \
        "16dp" if root.mode != "fill" else "24dp", \
        0 if root.mode != "fill" and not root.icon_right else ("14dp" if not root.icon_right else self._lbl_icon_right.texture_size[1] + dp(20)), \
        "16dp" if root.mode == "fill" else "10dp"
    multiline: False
    size_hint_y: None
    height: self.minimum_height + (dp(8) if root.mode != "fill" else 0)



"""
)
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock
from kivy.config import Config
from kivy.properties import OptionProperty, ObjectProperty, \
    BooleanProperty, NumericProperty
from time import time
from kivy.animation import Animation


class MDTextFieldMessageBubble(ButtonBehavior, MDTextField):
    background_color = ColorProperty()

    # Rozkminić zobie jakąś fajną animację -
    def on_focus(self, *args):
        return

    def on_touch_down(self, touch):
        pass

    def on_touch_move(self, touch):
        pass


Builder.load_string(
    """
#:import images_path kivymd.images_path


<MDTextFieldInput>
    canvas.before:
        Clear

        # Disabled line.
        Color:
            rgba:
                (self.line_color_normal \
                if self.line_color_normal else self.theme_cls.divider_color) \
                if root.mode == "line" else (0, 0, 0, 0)
        Line:
            points: self.x, self.y + dp(16), self.x + self.width, self.y + dp(16)
            width: 1
            dash_length: dp(3)
            dash_offset: 2 if self.disabled else 0

        # Active line.
        Color:
            rgba: self._current_line_color if root.mode in ("line", "fill") and root.active_line else (0, 0, 0, 0)
        Rectangle:
            size: self._line_width, dp(2)
            pos: self.center_x - (self._line_width / 2), self.y + (dp(16) if root.mode != "fill" else 0)

        # Helper text.
        Color:
            rgba: self._current_error_color
        Rectangle:
            texture: self._msg_lbl.texture
            size:
                self._msg_lbl.texture_size[0] - (dp(3) if root.mode in ("fill", "rectangle") else 0), \
                self._msg_lbl.texture_size[1] - (dp(3) if root.mode in ("fill", "rectangle") else 0)
            pos: self.x + (dp(8) if root.mode == "fill" else 0), self.y + (dp(3) if root.mode in ("fill", "rectangle") else 0)

        # Texture of right Icon.
        Color:
            rgba: self.icon_right_color if self.focus else self._current_hint_text_color
        Rectangle:
            texture: self._lbl_icon_right.texture
            size: self._lbl_icon_right.texture_size if self.icon_right else (0, 0)
            pos:
                (self.width + self.x) - (self._lbl_icon_right.texture_size[1]) - dp(8), \
                self.center[1] - self._lbl_icon_right.texture_size[1] / 2 + (dp(8) if root.mode != "fill" else 0) \
                if root.mode != "rectangle" else \
                self.center[1] - self._lbl_icon_right.texture_size[1] / 2 - dp(4)

        Color:
            rgba: root.background_color
        RoundedRectangle:
            pos: self.x, self.y
            size: self.width, self.height + dp(8)
            radius: root.radius

        Color:
            rgba:
                (self._current_line_color if self.focus and not \
                self._cursor_blink else (0, 0, 0, 0))
        Rectangle:
            pos: (int(x) for x in self.cursor_pos)
            size: 1, -self.line_height

        # Hint text.
        Color:
            rgba: 0.2,0.5,1,1
        Rectangle:
            texture: self._hint_lbl.texture
            size: self._hint_lbl.texture_size
            pos: self.x + (dp(8) if root.mode == "fill" else 0), self.y + self.height - self._hint_y

        Color:
            rgba:
                self.disabled_foreground_color if self.disabled else\
                (self.hint_text_color if not self.text and not\
                self.focus else self.foreground_color)

        # "rectangle" mode
        Color:
            rgba:
                self.text_color

        Line:
            width: dp(1) if root.mode == "rectangle" else dp(0.00001)
            points:
                (
                self.x + root._line_blank_space_right_point, self.top - self._hint_lbl.texture_size[1] // 2,
                self.right + dp(12), self.top - self._hint_lbl.texture_size[1] // 2,
                self.right + dp(12), self.y,
                self.x - dp(12), self.y,
                self.x - dp(12), self.top - self._hint_lbl.texture_size[1] // 2,
                self.x + root._line_blank_space_left_point, self.top - self._hint_lbl.texture_size[1] // 2
                )

    # "fill" mode.
    canvas.after:       
        Color:
            rgba: root._fill_color if root.mode == "fill" else (0, 0, 0, 0)
        RoundedRectangle:
            pos: self.x, self.y
            size: self.width, self.height + dp(8)
            radius: root.radius

    font_name: "Roboto" if not root.font_name else root.font_name
    foreground_color: self.theme_cls.text_color
    bold: False
    padding:
        0 if root.mode != "fill" else "8dp", \
        "16dp" if root.mode != "fill" else "24dp", \
        0 if root.mode != "fill" and not root.icon_right else ("14dp" if not root.icon_right else self._lbl_icon_right.texture_size[1] + dp(20)), \
        "16dp" if root.mode == "fill" else "10dp"
    multiline: False
    size_hint_y: None
    height: self.minimum_height + (dp(8) if root.mode != "fill" else 0)

"""
)
from kivy.animation import Animation
from kivy.metrics import dp, sp


class MDTextFieldInput(MDTextField):
    background_color = ColorProperty()
    text_color = (0, 0, 0, 1)

    def on_focus(self, *args):

        disabled_hint_text_color = self.theme_cls.disabled_hint_text_color
        Animation.cancel_all(
            self, "_line_width", "_hint_y", "_hint_lbl_font_size"
        )
        self._set_text_len_error()

        if self.focus:
            self.background_color = (0, 0, 0.2, 0.05)
            if not self._get_has_error():
                def on_progress(*args):
                    self._line_blank_space_right_point = (
                            self._hint_lbl.width + dp(5)
                    )

                animation = Animation(
                    _line_blank_space_left_point=self._hint_lbl.x - dp(5),
                    _current_hint_text_color=self.line_color_focus,
                    _fill_color=self.fill_color[:-1]
                                + [self.fill_color[-1] - 0.1],
                    duration=0.2,
                    t="out_quad",
                )
                animation.bind(on_progress=on_progress)
                animation.start(self)
            self.has_had_text = True
            Animation.cancel_all(
                self, "_line_width", "_hint_y", "_hint_lbl_font_size"
            )
            if not self.text:
                self._anim_lbl_font_size(dp(14), sp(12))
            Animation(
                _line_width=self.width,
                duration=(0.2 if self.line_anim else 0),
                t="out_quad",
            ).start(self)
            if self._get_has_error():
                self._anim_current_error_color(self.error_color)
                if self.helper_text_mode == "on_error" and (
                        self.error or self._text_len_error
                ):
                    self._anim_current_error_color(self.error_color)
                elif (
                        self.helper_text_mode == "on_error"
                        and not self.error
                        and not self._text_len_error
                ):
                    self._anim_current_error_color((0, 0, 0, 0))
                elif self.helper_text_mode in ("persistent", "on_focus"):
                    self._anim_current_error_color(disabled_hint_text_color)
            else:
                self._anim_current_right_lbl_color(disabled_hint_text_color)
                Animation(
                    duration=0.2, _current_hint_text_color=self.line_color_focus
                ).start(self)
                if self.helper_text_mode == "on_error":
                    self._anim_current_error_color((0, 0, 0, 0))
                if self.helper_text_mode in ("persistent", "on_focus"):
                    self._anim_current_error_color(disabled_hint_text_color)
        else:
            self.background_color = (1, 1, 1, 0)
            Animation(
                _fill_color=self.fill_color[:-1] + [self.fill_color[-1] + 0.1],
                duration=0.2,
                t="out_quad",
            ).start(self)
            if not self.text:
                self._anim_lbl_font_size(dp(38), sp(16))
                Animation(
                    _line_blank_space_right_point=0,
                    _line_blank_space_left_point=0,
                    duration=0.2,
                    t="out_quad",
                ).start(self)
            if self._get_has_error():
                self._anim_get_has_error_color(self.error_color)
                if self.helper_text_mode == "on_error" and (
                        self.error or self._text_len_error
                ):
                    self._anim_current_error_color(self.error_color)
                elif (
                        self.helper_text_mode == "on_error"
                        and not self.error
                        and not self._text_len_error
                ):
                    self._anim_current_error_color((0, 0, 0, 0))
                elif self.helper_text_mode == "persistent":
                    self._anim_current_error_color(disabled_hint_text_color)
                elif self.helper_text_mode == "on_focus":
                    self._anim_current_error_color((0, 0, 0, 0))
            else:
                Animation(duration=0.2, color=(1, 1, 1, 1)).start(
                    self._hint_lbl
                )
                self._anim_get_has_error_color()
                if self.helper_text_mode == "on_error":
                    self._anim_current_error_color((0, 0, 0, 0))
                elif self.helper_text_mode == "persistent":
                    self._anim_current_error_color(disabled_hint_text_color)
                elif self.helper_text_mode == "on_focus":
                    self._anim_current_error_color((0, 0, 0, 0))
                Animation(
                    _line_width=0,
                    duration=(0.2 if self.line_anim else 0),
                    t="out_quad",
                ).start(self)

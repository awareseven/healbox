import random
import string

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GObject


class PageContainer(Gtk.VBox):
    title: str = ""
    page_type: Gtk.AssistantPageType = Gtk.AssistantPageType.CONTENT
    completed: bool = True
    username: str = ""
    hostname: str = ""

    def __init__(self):
        super().__init__()

        # Initialize Colors (Gdk.Color)
        self._color_error = Gdk.RGBA()
        self._color_error.parse("#ff0000")
        self._color_error = self._color_error.to_color()

        self._color_warning = Gdk.RGBA()
        self._color_warning.parse("#ffcc00")
        self._color_warning = self._color_warning.to_color()

        self._color_success = Gdk.RGBA()
        self._color_success.parse("#00cc00")
        self._color_success = self._color_success.to_color()

        self.set_valign(Gtk.Align.CENTER)

        GObject.signal_new("page_completed", self,
                           GObject.SignalFlags.RUN_LAST, None, (bool,))

        GObject.signal_new("page_exception", self,
                           GObject.SignalFlags.RUN_LAST, None, (object,))

    def _emit_page_completed(self, sufficient: bool):
        self.emit("page_completed", sufficient)

    def _emit_exception(self, exception: Exception):
        self.emit("page_exception", exception)

    @staticmethod
    def __rand_string(string_length: int) -> str:
        return ''.join(random.choice(
            string.ascii_letters + string.digits
        ) for _ in range(string_length))

    @classmethod
    def set_random_username(cls, rand_char_len):
        cls.username = "hb-" + cls.__rand_string(rand_char_len)

    @classmethod
    def set_random_hostname(cls, rand_char_len):
        cls.hostname = "healbox-" + cls.__rand_string(rand_char_len)


PageContainer.set_random_username(3)
PageContainer.set_random_hostname(6)

from gi.repository import Gdk, GObject, Gtk

from .. import ApplicationState


class PageContainer(Gtk.VBox):
    title: str = ""
    page_type: Gtk.AssistantPageType = Gtk.AssistantPageType.CONTENT
    completed: bool = True
    _application_state = None

    # Custom Signals
    __gsignals__ = {
        "page_completed": (GObject.SIGNAL_RUN_LAST, None, (bool,)),
        "page_exception": (GObject.SIGNAL_RUN_LAST, None, (object,)),
    }

    def _emit_page_completed(self, sufficient: bool):
        self.emit("page_completed", sufficient)

    def _emit_exception(self, exception: Exception):
        self.emit("page_exception", exception)

    def __init__(self):
        super().__init__()

        self._application_state = ApplicationState.get_instance()

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

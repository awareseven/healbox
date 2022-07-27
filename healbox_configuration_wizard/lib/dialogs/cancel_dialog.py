from gi.repository import Gtk


class CancelDialog(Gtk.MessageDialog):
    def __init__(self, parent):
        super().__init__(
            title="Schließen?",
            transient_for=parent,
            flags=0,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.OK_CANCEL,
            text="Das Fenster wird nun geschlossen."
        )

        self.format_secondary_text("Möchten Sie fortfahren?")
        self.show_all()
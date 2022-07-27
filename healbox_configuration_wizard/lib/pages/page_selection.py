from gi.repository import Gtk

from . import PageContainer


class PageSelection(PageContainer):
    title = "Programme auswählen"

    def __init__(self):
        super().__init__()
        self.__content()

    def __content(self):
        # Create Label
        lbl = Gtk.Label()
        lbl.set_justify(Gtk.Justification.LEFT)
        lbl.set_halign(Gtk.Align.START)
        lbl.set_margin_bottom(10)
        lbl.set_label(
            "Bitte wählen Sie die Programme aus, die installiert werden sollen:")

        self.add(lbl)

        # Create Check Boxes
        cb1 = Gtk.CheckButton.new_with_label(
            "Thunderbird (E-Mail Client)")
        cb1.connect("toggled", self._application_state.set_user_selection,
                    "cb1", "thunderbird thunderbird-l10n-de")
        cb1.set_active(True)

        cb2 = Gtk.CheckButton.new_with_label(
            "LibreOffice (Office Anwendung)")
        cb2.connect("toggled", self._application_state.set_user_selection,
                    "cb2", "libreoffice-writer")
        cb2.set_active(True)

        cb3 = Gtk.CheckButton.new_with_label(
            "ScreenShooter (Bildschirmfotos)")
        cb3.connect("toggled", self._application_state.set_user_selection,
                    "cb3", "xfce4-screenshooter")
        cb3.set_active(True)

        container = Gtk.VBox()
        container.add(cb1)
        container.add(cb2)
        container.add(cb3)

        self.add(container)

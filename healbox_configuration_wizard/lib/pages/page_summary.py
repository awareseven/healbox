import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from . import PageContainer


class PageSummary(PageContainer):
    title = "Zusammenfassung"
    page_type = Gtk.AssistantPageType.CONFIRM

    def __init__(self):
        super().__init__()
        self.__content()

    def __content(self):
        lbl = Gtk.Label()
        lbl.set_justify(Gtk.Justification.LEFT)
        lbl.set_label("""
Folgende Änderungen werden am System vorgenommen:

Unnötige Dienste werden deaktiviert
Nicht notwendige Anwendungen entfernt
E-Mail & Office Anwendungen Installiert
Sicherheitseinstellungen angewendet
Berechtigungen angepasst
""")

        # TODO: Display system changes

        self.add(lbl)

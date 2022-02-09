import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from . import PageContainer


class PageResult(PageContainer):
    title = "Ergebnis"
    page_type = Gtk.AssistantPageType.SUMMARY

    def __init__(self):
        super().__init__()
        self.__content()

    def __content(self):
        lbl = Gtk.Label()
        lbl.set_justify(Gtk.Justification.LEFT)
        lbl.set_label(f"""
Das System ({self.hostname}) wurde angepasst.
Ein neuer Benutzer {self.username} wurde angelegt.
Starten Sie das System neu und melden Sie sich als neuer
Nutzer {self.username} an.
""")
        self.add(lbl)

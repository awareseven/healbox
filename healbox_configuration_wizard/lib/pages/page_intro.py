import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from . import PageContainer


class PageIntro(PageContainer):
    title = "Einführung"
    page_type = Gtk.AssistantPageType.INTRO

    def __init__(self):
        super().__init__()
        self.__content()

    def __content(self):
        lbl = Gtk.Label()
        lbl.set_justify(Gtk.Justification.LEFT)
        lbl.set_label("""
Fast geschafft!
Es müssen nur noch ein paar Dinge angepasst werden bevor es richtig losgehen kann!

Wenn Sie bereit sind, drücken Sie auf "Weiter".
""")
        self.add(lbl)

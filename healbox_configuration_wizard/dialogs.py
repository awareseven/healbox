import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf


class CancelDialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Schließen?", transient_for=parent, flags=0)

        self.add_button("Abbrechen", Gtk.ResponseType.CANCEL)
        self.add_button("OK", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.CANCEL)

        lbl1 = Gtk.Label()
        lbl1.set_label("Das Fenster wird nun geschlossen.")
        lbl1.set_justify(Gtk.Justification.CENTER)
        lbl1.set_margin_start(10)
        lbl1.set_margin_end(10)
        lbl1.set_margin_top(10)
        lbl1.set_margin_bottom(10)

        lbl2 = Gtk.Label()
        lbl2.set_label("Möchten Sie Fortfahren?")
        lbl2.set_margin_bottom(10)

        container = Gtk.VBox()
        container.add(lbl1)
        container.add(lbl2)

        self.get_content_area().add(container)
        # self.get_action_area().set_halign(Gtk.Align.CENTER)
        self.show_all()


class RebootDialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Bitte Neustarten", transient_for=parent, flags=0)
        self.set_default_size(100, 100)

        self.add_button("Später Neustarten", Gtk.ResponseType.CANCEL)
        self.add_button("Jetzt Neustarten", Gtk.ResponseType.OK)
        self.set_default_response(Gtk.ResponseType.OK)

        logo_pixbuf = GdkPixbuf.Pixbuf.new_from_file('healbox.svg')
        logo_pixbuf = logo_pixbuf.scale_simple(
            80, 80, GdkPixbuf.InterpType.BILINEAR)

        hb_icon = Gtk.Image.new_from_pixbuf(logo_pixbuf)
        hb_icon.set_margin_top(10)
        hb_icon.set_margin_bottom(20)
        hb_icon.set_margin_start(10)
        hb_icon.set_margin_end(10)

        lbl1 = Gtk.Label()
        lbl1.set_label(
            "Um die Installation vollständig abzuschließen muss das System neugestartet werden.")
        lbl1.set_line_wrap(True)
        lbl1.set_size_request(80, -1)
        lbl1.set_justify(Gtk.Justification.CENTER)
        lbl1.set_margin_bottom(30)

        lbl2 = Gtk.Label()
        lbl2.set_label("Jetzt neustarten?")
        lbl2.set_margin_bottom(10)

        container = Gtk.VBox()
        container.add(hb_icon)
        container.add(lbl1)
        container.add(lbl2)

        self.get_content_area().add(container)
        self.show_all()

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, GdkPixbuf

from pages import *

import subprocess

class AppWindow(Gtk.Assistant):
    def __init__(self):
        # Initialize Object properties
        ## Colors (Gdk.Color)
        self.clr_error = Gdk.RGBA()
        self.clr_error.parse("#ff0000")
        self.clr_error = self.clr_error.to_color()

        self.clr_warning = Gdk.RGBA()
        self.clr_warning.parse("#ffcc00")
        self.clr_warning = self.clr_warning.to_color()

        self.clr_success = Gdk.RGBA()
        self.clr_success.parse("#00cc00")
        self.clr_success = self.clr_success.to_color()

        self.pw_sufficient = False

        # Initialize Gtk.Assistant
        super().__init__()

        # Initialize Main Window
        self.InitWindow()

        # Initialize Header
        self.InitHeader()

        # Initialize Pages
        self.InitPage(PageIntro())

        ## Deployment options
        self.pd = PageDeployment()
        self.InitPage(self.pd)

        ## Password page
        self.pwp = PagePassword()
        self.InitPage(self.pwp)
        self.pwp.pw1.connect("changed", self.do_handle_pw1_changed)
        self.pwp.pw2.connect("changed", self.do_handle_pw2_changed)

        ## Page selection
        self.ps = PageSelection()
        self.InitPage(self.ps)
        
        self.InitPage(PageSummary())

        ## Progress page
        self.pp = PageProgress()
        self.InitPage(self.pp)

        ## Summary page
        self.InitPage(PageResult())

    def InitWindow(self):
        self.set_icon_from_file("healbox.svg")
        self.set_default_size(600, 350)
        self.set_resizable(False)
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)

        self.connect("cancel", self.do_handle_cancel)
        self.connect("close", self.do_handle_close)
        self.connect("prepare", self.do_handle_prepare)

    def InitHeader(self):
        hb = Gtk.HeaderBar()
        hb.set_has_subtitle(True)
        hb.set_show_close_button(True)
        hb.set_subtitle("Healbox Configuration Wizard")

        logo_pixbuf = GdkPixbuf.Pixbuf.new_from_file('healbox.svg')
        logo_pixbuf = logo_pixbuf.scale_simple(
            40, 40, GdkPixbuf.InterpType.BILINEAR)

        hb_icon = Gtk.Image.new_from_pixbuf(logo_pixbuf)
        hb_icon.set_margin_top(5)
        hb_icon.set_margin_bottom(5)
        hb_icon.set_margin_start(5)
        hb_icon.set_margin_end(5)

        hb.add(hb_icon)
        self.set_titlebar(hb)

    def InitPage(self, page: PageContainer):
        self.append_page(page)
        self.set_page_title(page, page.title)
        self.set_page_type(page, page.page_type)
        self.set_page_complete(page, page.completed)

    def do_handle_cancel(self, _widget):
        dialog = CancelDialog(self)

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            dialog.destroy()
            self.destroy()
            Gtk.main_quit
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()

    def do_handle_close(self, _widget):
        self.destroy()

        dialog = RebootDialog(self)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            print("Reboot")
        elif response == Gtk.ResponseType.CANCEL:
            print("Do not reboot")

        dialog.destroy()

    def do_handle_pw1_changed(self, _widget):
        new_pw1 = self.pwp.pw1.get_text()
        self.pwp.pw1.set_progress_fraction(0)

        if not new_pw1.strip():
            self.pwp.pw_result.modify_fg(Gtk.StateType.NORMAL, self.clr_error)
            self.pwp.pw_result.set_label("Das Passwort darf nicht leer sein!")
        else:
            pw_shell = subprocess.run("/usr/bin/pwscore", input=new_pw1, capture_output=True, text=True)
            self.pw_sufficient = False

            if (pw_shell.returncode != 0):
                self.pwp.pw_result.modify_fg(Gtk.StateType.NORMAL, self.clr_error)
                self.pwp.pw_result.set_label(pw_shell.stderr.splitlines()[-1])
            else:
                pw_score = int(pw_shell.stdout)
                
                self.pwp.pw_result.modify_fg(Gtk.StateType.NORMAL, self.clr_warning)
                self.pwp.pw_result.set_label(f"Aktuelle Passwort-Stärke: {pw_score}")
                self.pwp.pw1.set_progress_fraction(pw_score/100)
                
                if (pw_score > 90):
                    self.pwp.pw_result.modify_fg(Gtk.StateType.NORMAL, self.clr_success)
                    self.pw_sufficient = True
        

    def do_handle_pw2_changed(self, _widget):
        if self.pw_sufficient:
            if (self.pwp.pw1.get_text() == self.pwp.pw2.get_text()):
                self.pwp.pw_result.modify_fg(Gtk.StateType.NORMAL, self.clr_success)
                self.pwp.pw_result.set_label("Die Passwörter stimmen überein!")
                self.set_page_complete(self.pwp, True)
            else:
                self.pwp.pw_result.modify_fg(Gtk.StateType.NORMAL, self.clr_error)
                self.pwp.pw_result.set_label("Die Passwörter stimmen nicht überein!")
                self.set_page_complete(self.pwp, False)

    def do_handle_prepare(self, assistant, page):
        if (page.page_type == Gtk.AssistantPageType.PROGRESS):
            # Remove Back-Button and clear History
            assistant.commit()
            # TODO: Process User Input
            assistant.set_page_complete(page, True)

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


win = AppWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

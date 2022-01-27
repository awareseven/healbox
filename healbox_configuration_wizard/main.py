import subprocess
# from time import sleep
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf
# TODO Import atomically
from pages import *
from dialogs import *


class AppWindow(Gtk.Assistant):
    def __init__(self):
        # Initialize Object properties
        # Colors (Gdk.Color)
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

        # Deployment options
        self.pd = PageDeployment()
        self.InitPage(self.pd)

        # Password page
        self.pwp = PagePassword()
        self.InitPage(self.pwp)
        self.pwp.pw1.connect("changed", self.do_handle_pw1_changed)
        self.pwp.pw2.connect("changed", self.do_handle_pw2_changed)

        # Page selection
        self.ps = PageSelection()
        self.InitPage(self.ps)

        self.InitPage(PageSummary())

        # Progress page
        self.pp = PageProgress()
        self.InitPage(self.pp)

        # Summary page
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
        self.pwp.pw2.set_sensitive(False)

        if not new_pw1.strip():
            self.pwp.pw_result.modify_fg(Gtk.StateType.NORMAL, self.clr_error)
            self.pwp.pw_result.set_label("Das Passwort darf nicht leer sein!")
        else:
            pw_shell = subprocess.run(
                "/usr/bin/pwscore", input=new_pw1, capture_output=True, text=True)

            if (pw_shell.returncode != 0):
                self.pwp.pw_result.modify_fg(
                    Gtk.StateType.NORMAL, self.clr_error)
                self.pwp.pw_result.set_label(
                    pw_shell.stderr.splitlines()[-1].strip())
            else:
                pw_score = int(pw_shell.stdout)

                self.pwp.pw_result.modify_fg(
                    Gtk.StateType.NORMAL, self.clr_warning)
                self.pwp.pw_result.set_label(
                    f"Aktuelle Passwort-Stärke: {pw_score}")
                self.pwp.pw1.set_progress_fraction(pw_score / 100)

                # TODO Display minimum password score
                if (pw_score > 90):
                    self.pwp.pw_result.modify_fg(
                        Gtk.StateType.NORMAL, self.clr_success)
                    self.pwp.pw2.set_sensitive(True)

    def do_handle_pw2_changed(self, _widget):
        if (self.pwp.pw1.get_text() == self.pwp.pw2.get_text()):
            self.pwp.pw_result.modify_fg(
                Gtk.StateType.NORMAL, self.clr_success)
            self.pwp.pw_result.set_label("Die Passwörter stimmen überein!")
            self.set_page_complete(self.pwp, True)
        else:
            self.pwp.pw_result.modify_fg(
                Gtk.StateType.NORMAL, self.clr_error)
            self.pwp.pw_result.set_label(
                "Die Passwörter stimmen nicht überein!")
            self.set_page_complete(self.pwp, False)

    def do_handle_prepare(self, assistant, page):
        if (page.page_type == Gtk.AssistantPageType.PROGRESS):
            # Remove Back-Button and clear History
            assistant.commit()

            # TODO: Process User Input
            # + Set up firewall (SMTP)
            # + New generated user
            # + Set and validate password (requires libpwquality-tools)
            # + Change hostname
            # + Install selected packages
            # + Remove user 'pi'
            # + Remove script + dependencies
            # + Deactivate autologin
            # + Restore sudo configuration (revert exception to start wizard as root)
            # + System restore on error

            cmd_list = [
                ["apt", "list", "--installed"]
            ]

            for cmd in cmd_list:
                p = subprocess.Popen(
                    cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
                while p.poll() is None:
                    std_out = p.stdout.readline()
                    # sleep(0.05)
                    self.pp.pb.pulse()
                    self.pp.txtbuf.insert_at_cursor(
                        std_out, len(std_out.encode('utf-8')))

            assistant.set_page_complete(page, True)


win = AppWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

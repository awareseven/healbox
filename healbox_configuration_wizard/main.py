import shlex
import subprocess
from threading import Thread
from time import sleep

# Import GTK
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf, GLib

from dialogs import CancelDialog, RebootDialog
from pages import PageContainer, PageDeployment, PageIntro, PagePassword, PageProgress, PageResult, PageSelection, PageSummary


class AppWindow(Gtk.Assistant):
    def __init__(self):
        # Initialize Gtk.Assistant
        super().__init__()

        # Initialize Main Window
        self.__init_window()

        # Initialize Header
        self.__init_header()

        # Initialize Pages
        self.__init_page(PageIntro())

        # Deployment options
        self.page_deployment = PageDeployment()
        self.__init_page(self.page_deployment)

        # Password page
        self.page_password = PagePassword()
        self.page_password.connect(
            "pw_sufficient", self.__do_handle_pw_sufficient)
        self.__init_page(self.page_password)

        # Page selection
        self.page_selection = PageSelection()
        self.__init_page(self.page_selection)

        self.__init_page(PageSummary())

        # Progress page
        self.page_progress = PageProgress()
        self.__init_page(self.page_progress)

        # Summary page
        self.__init_page(PageResult())

    def __init_window(self):
        self.set_icon_from_file("healbox.svg")
        self.set_default_size(600, 350)
        self.set_resizable(False)
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)

        self.connect("cancel", self.__do_handle_cancel)
        self.connect("close", self.__do_handle_close)
        self.connect("prepare", self.__do_handle_prepare)

    def __init_header(self):
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

    def __init_page(self, page: PageContainer):
        self.append_page(page)
        self.set_page_title(page, page.title)
        self.set_page_type(page, page.page_type)
        self.set_page_complete(page, page.completed)

    def __do_handle_cancel(self, _):
        dialog = CancelDialog(self)

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            dialog.destroy()
            self.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()

    def __do_handle_close(self, _):
        self.destroy()

        dialog = RebootDialog(self)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            print("Reboot")
        elif response == Gtk.ResponseType.CANCEL:
            print("Do not reboot")

        dialog.destroy()

    def __do_handle_prepare(self, _, page: PageContainer):
        if (page.page_type == Gtk.AssistantPageType.PROGRESS):
            # Remove Back-Button and clear History
            self.commit()

            # TODO: create appropriate command list
            print(self.page_deployment.deployment_mode)
            print(self.page_selection.get_package_list())
            print(self.page_password.password)

            # Initialize command list to be executed by subprocess.Popen()
            cmd_list = [
                "apt list --installed",
                "cat /etc/ssh/ssh_config",
            ]

            # Process system changes
            # Docs: https://pygobject.readthedocs.io/en/latest/guide/threading.html
            Thread(target=self.__process_input,
                   daemon=True, args=(cmd_list,)).start()

    def __do_handle_pw_sufficient(self, page: PageContainer, pw_sufficient: bool):
        self.set_page_complete(page, pw_sufficient)

    def __process_input(self, cmd_list):
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

        def show_pulse() -> bool:
            self.page_progress.pb.pulse()
            return True

        def init_progress(cmd_index: int, cmd_list: list):
            cmd_string = f"Command output [{cmd_list[cmd_index]}]:\n"
            self.page_progress.pb.set_fraction(0)
            self.page_progress.pb.set_text(
                f"Es werden Änderungen an Ihrem System vorgenommen. Bitte warten. {cmd_index + 1}/{len(cmd_list)}")
            self.page_progress.txtbuf.insert(
                self.page_progress.end_iter,
                cmd_string,
                len(cmd_string.encode("utf-8"))
            )

        def write_progress_log(log_output: str):
            self.page_progress.txtbuf.insert(
                self.page_progress.end_iter,
                log_output,
                len(log_output.encode("utf-8"))
            )

            self.page_progress.txtview.scroll_to_mark(
                self.page_progress.txtmark, 0, False, 0, 0)

        pulse_id = GLib.timeout_add(100, show_pulse)

        for i in range(len(cmd_list)):
            GLib.idle_add(init_progress, i, cmd_list)
            p = subprocess.Popen(
                shlex.split(cmd_list[i]),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                encoding="utf-8"
            )

            while True:
                std_out = p.stdout.readline()
                if std_out == "" and p.poll() is not None:
                    GLib.idle_add(write_progress_log, "\n")
                    break

                GLib.idle_add(write_progress_log, std_out)
                sleep(0.02)

        GLib.source_remove(pulse_id)
        self.page_progress.pb.set_fraction(1)
        self.page_progress.pb.set_text(
            "Alle Änderungen sind erfolgreich durchgeführt worden!")
        self.set_page_complete(self.page_progress, True)


def main():
    win = AppWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()


if __name__ == '__main__':
    main()

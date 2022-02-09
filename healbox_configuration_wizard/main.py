from threading import Thread

# Import GTK
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf

from lib.dialogs import CancelDialog
from lib.dialogs import RebootDialog
from lib.pages import PageContainer
from lib.pages import PageDeployment
from lib.pages import PageIntro
from lib.pages import PagePassword
from lib.pages import PageProgress
from lib.pages import PageResult
from lib.pages import PageSelection
from lib.pages import PageSummary

HEALBOX_LOGO = "assets/healbox.svg"


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
            "page_completed", self.__do_handle_page_completed)
        self.__init_page(self.page_password)

        # Page selection
        self.page_selection = PageSelection()
        self.__init_page(self.page_selection)

        self.__init_page(PageSummary())

        # Progress page
        self.page_progress = PageProgress()
        self.page_progress.connect(
            "page_completed", self.__do_handle_page_completed)
        self.__init_page(self.page_progress)

        # Summary page
        self.__init_page(PageResult())

    def __init_window(self):
        self.set_icon_from_file(HEALBOX_LOGO)
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

        logo_pixbuf = GdkPixbuf.Pixbuf.new_from_file(HEALBOX_LOGO)
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
        page.connect("page_exception", self.__do_handle_page_exception)

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

        dialog = RebootDialog(self, HEALBOX_LOGO)
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
            print(PageContainer.username)
            print(PageContainer.hostname)

            # Initialize command list to be executed by subprocess.Popen()
            cmd_list = [
                "apt list --installed",
                "cat /etc/ssh/ssh_config",
            ]

            # Process system changes
            # Docs: https://pygobject.readthedocs.io/en/latest/guide/threading.html
            Thread(target=self.page_progress.process_input,
                   daemon=True, args=(cmd_list,)).start()

    def __do_handle_page_completed(self, page: PageContainer, completed: bool):
        self.set_page_complete(page, completed)

    def __do_handle_page_exception(self, widget, exception: Exception):
        # TODO: Error dialog
        print(widget, exception)


def main():
    win = AppWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()


if __name__ == '__main__':
    main()

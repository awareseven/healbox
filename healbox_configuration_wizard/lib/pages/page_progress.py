import shlex
import subprocess
from time import sleep

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

from . import PageContainer


class PageProgress(PageContainer):
    title = "Verlauf"
    page_type = Gtk.AssistantPageType.PROGRESS
    completed = False

    def __init__(self):
        super().__init__()
        self.__pb = ""
        self.__txtview = ""
        self.__txtbuf = ""
        self.__txtmark = ""
        self.__end_iter = ""
        self.__content()

    def __content(self):
        # Fill entire page
        self.set_valign(Gtk.Align.FILL)

        # Add Progress Bar
        self.__pb = Gtk.ProgressBar()
        self.__pb.set_show_text(True)
        self.__pb.set_valign(Gtk.Align.END)

        self.add(self.__pb)

        # Add Expander
        exp = Gtk.Expander()
        exp.set_label("Mehr Informationen")
        exp.set_margin_top(10)

        # Add scroll window
        sw = Gtk.ScrolledWindow()
        # Allow terminal output to grow vertically
        sw.set_vexpand(True)

        # Add text box
        self.__txtview = Gtk.TextView()
        self.__txtview.set_editable(False)
        self.__txtview.set_input_purpose(Gtk.InputPurpose.FREE_FORM)
        self.__txtview.set_monospace(True)

        # Create text buffer
        self.__txtbuf = Gtk.TextBuffer()

        # Create text mark
        self.__txtmark = Gtk.TextMark.new(None, False)

        # Get text iterator at the end of the buffer
        self.__end_iter = self.__txtbuf.get_end_iter()

        # Add text mark at the end of the buffer
        self.__txtbuf.add_mark(self.__txtmark, self.__end_iter)

        self.__txtview.set_buffer(self.__txtbuf)
        sw.add(self.__txtview)
        exp.add(sw)
        self.add(exp)

    def process_input(self, cmd_list):
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
            self.__pb.pulse()
            return True

        def init_progress(cmd_index: int, cmd_list: list):
            cmd_string = f"Command output [{cmd_list[cmd_index]}]:\n"
            self.__pb.set_fraction(0)
            self.__pb.set_text(
                f"Es werden Änderungen an Ihrem System vorgenommen. Bitte warten. {cmd_index + 1}/{len(cmd_list)}")
            self.__txtbuf.insert(
                self.__end_iter,
                cmd_string,
                len(cmd_string.encode("utf-8"))
            )

        def write_progress_log(log_output: str):
            self.__txtbuf.insert(
                self.__end_iter,
                log_output,
                len(log_output.encode("utf-8"))
            )

            self.__txtview.scroll_to_mark(
                self.__txtmark, 0, False, 0, 0)

        pulse_id = GLib.timeout_add(100, show_pulse)

        try:
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
            self.__pb.set_fraction(1)
            self.__pb.set_text(
                "Alle Änderungen sind erfolgreich durchgeführt worden!")

            self._emit_page_completed(True)
        except Exception as e:
            self._emit_exception(e)

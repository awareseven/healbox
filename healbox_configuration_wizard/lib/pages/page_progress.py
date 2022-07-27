import subprocess

from gi.repository import GLib, Gtk

from .. import ProcessExecutor
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

        self.cmd_max = 0
        self.cmd_step = 0

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

    def __show_pulse(self) -> bool:
        self.__pb.pulse()
        return True

    def __init_progress(self):
        self.__pb.set_fraction(0)
        self.__pb.set_text(
            f"Es werden Änderungen an Ihrem System vorgenommen. Bitte warten. {self.cmd_step}/{self.cmd_max}")

    def __write_progress(self, cmd_out):
        self.__txtbuf.insert(
            self.__end_iter,
            cmd_out,
            len(cmd_out.encode("utf-8"))
        )
        self.__txtview.scroll_to_mark(
            self.__txtmark, 0, False, 0, 0)

    def __on_cmd_max(self, _, cmd_max: int):
        self.cmd_max = cmd_max

    def __on_cmd_step(self, _, cmd_step: int):
        self.cmd_step = cmd_step
        GLib.idle_add(self.__init_progress)

    def __on_cmd_out(self, _, cmd_out: str):
        GLib.idle_add(self.__write_progress, cmd_out)

    def process_input(self):
        try:
            system_changes = self._application_state.get_application_state()

            process_executor = ProcessExecutor()
            process_executor.connect("cmd_max", self.__on_cmd_max)
            process_executor.connect("cmd_step", self.__on_cmd_step)
            process_executor.connect("cmd_out", self.__on_cmd_out)

            pulse_id = GLib.timeout_add(100, self.__show_pulse)
            process_executor.process_input(system_changes)
            GLib.source_remove(pulse_id)
            self.__pb.set_fraction(1)
            self.__pb.set_text(
                "Alle Änderungen sind erfolgreich durchgeführt worden!")

            self._emit_page_completed(True)
        except Exception as e:
            self._emit_exception(e)

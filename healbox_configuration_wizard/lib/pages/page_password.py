import subprocess

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from . import PageContainer


class PagePassword(PageContainer):
    title = "Passwort für neuen Benutzer"
    completed = False

    def __init__(self):
        super().__init__()
        self.__pw1: str = ""
        self.__pw2: str = ""
        self.__pw_result: str = ""
        self.password: str = ""
        self.__content()

    def __content(self):
        # password message
        lbl = Gtk.Label()
        lbl.set_label(
            f"Bitte setzen Sie ein sicheres Passwort für Ihren Healbox-Benutzer \"{self.username}\".")
        lbl.set_margin_bottom(20)
        lbl.set_halign(Gtk.Align.START)

        self.add(lbl)

        # password prompt
        self.__pw1 = self.__create_password_entry("Passwort")
        self.__pw1.connect("changed", self.__do_handle_pw1_changed)
        self.__pw2 = self.__create_password_entry("Passwort wiederholen")
        self.__pw2.connect("changed", self.__do_handle_pw2_changed)

        self.__pw2.set_sensitive(False)

        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_row_spacing(5)

        pw_prompt = Gtk.Label()
        pw_prompt.set_label("Neues Passwort")
        pw_prompt.set_margin_top(5)
        pw_prompt.set_margin_bottom(5)
        pw_prompt.set_margin_start(5)
        pw_prompt.set_margin_end(5)
        pw_prompt.set_halign(Gtk.Align.END)

        grid.attach(pw_prompt, 0, 0, 1, 1)
        grid.attach(self.__pw1, 1, 0, 1, 1)
        grid.attach(self.__pw2, 1, 1, 1, 1)

        # password check result
        self.__pw_result = Gtk.Label()
        self.__pw_result.set_margin_top(5)
        self.__pw_result.set_line_wrap(True)

        self.__pw_result.modify_fg(Gtk.StateType.NORMAL, self._color_warning)
        self.__pw_result.set_label("Bitte wählen Sie ein Passwort")

        grid.attach(self.__pw_result, 1, 2, 1, 1)

        self.add(grid)

    def __create_password_entry(self, placeholder: str) -> Gtk.Entry:
        txt = Gtk.Entry()
        txt.set_placeholder_text(placeholder)
        txt.set_visibility(False)
        txt.set_input_purpose(Gtk.InputPurpose.PASSWORD)
        txt.set_halign(Gtk.Align.FILL)
        txt.set_hexpand(True)
        # TODO: Select appropriate icon for the current icon theme
        txt.set_icon_from_icon_name(
            Gtk.EntryIconPosition.SECONDARY, "image-red-eye-symbolic")
        txt.connect("icon-press", self.__do_handle_press)
        txt.connect("icon-release", self.__do_handle_release)
        return txt

    def __do_handle_press(self, widget, *_):
        widget.set_visibility(True)

    def __do_handle_release(self, widget, *_):
        widget.set_visibility(False)

    def __do_handle_pw1_changed(self, _):
        self.password = self.__pw1.get_text()
        self.__pw1.set_progress_fraction(0)
        self.__pw2.set_sensitive(False)

        if not self.password.strip():
            self.__pw_result.modify_fg(Gtk.StateType.NORMAL, self._color_error)
            self.__pw_result.set_label("Das Passwort darf nicht leer sein!")
        else:
            pw_shell = subprocess.run(
                "/usr/bin/pwscore",
                input=self.password,
                capture_output=True,
                text=True
            )

            if (pw_shell.returncode != 0):
                self.__pw_result.modify_fg(
                    Gtk.StateType.NORMAL, self._color_error)
                self.__pw_result.set_label(
                    pw_shell.stderr.splitlines()[-1].strip())
            else:
                pw_score = int(pw_shell.stdout)

                self.__pw_result.modify_fg(
                    Gtk.StateType.NORMAL, self._color_warning)
                self.__pw_result.set_label(
                    f"Aktuelle Passwort-Stärke: {pw_score}")
                self.__pw1.set_progress_fraction(pw_score / 100)

                # TODO Display minimum password score
                if (pw_score > 90):
                    self.__pw_result.modify_fg(
                        Gtk.StateType.NORMAL, self._color_success)
                    self.__pw2.set_sensitive(True)

    def __do_handle_pw2_changed(self, _):
        if (self.__pw1.get_text() == self.__pw2.get_text()):
            self.__pw_result.modify_fg(
                Gtk.StateType.NORMAL, self._color_success)
            self.__pw_result.set_label("Die Passwörter stimmen überein!")
            self._emit_page_completed(True)
        else:
            self.__pw_result.modify_fg(
                Gtk.StateType.NORMAL, self._color_error)
            self.__pw_result.set_label(
                "Die Passwörter stimmen nicht überein!")
            self._emit_page_completed(False)

from enum import Enum
import random
import string
import subprocess

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GObject


class PageContainer(Gtk.VBox):
    title: str = "Page Title"
    page_type: Gtk.AssistantPageType = Gtk.AssistantPageType.CONTENT
    completed: bool = True

    def __init__(self):
        super().__init__()
        self.set_valign(Gtk.Align.CENTER)

    @staticmethod
    def __rand_string(strlen: int) -> str:
        return ''.join(random.choice(
            string.ascii_letters + string.digits
        ) for _ in range(strlen))

    username: str = "hb-" + __rand_string(3)
    hostname: str = "healbox-" + __rand_string(6)


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


class PageDeployment(PageContainer):
    title = "Einsatzzweck"

    class DeploymentMode(Enum):
        READ_ONLY = 1
        READ_SEND = 2
        PROXY = 3

    def __init__(self):
        super().__init__()
        self.deployment_mode = self.DeploymentMode.READ_ONLY
        self.__content()

    def __content(self):
        # Create Label
        lbl = Gtk.Label()
        lbl.set_justify(Gtk.Justification.LEFT)
        lbl.set_halign(Gtk.Align.START)
        lbl.set_margin_bottom(10)
        lbl.set_label("Wählen Sie aus, wie Sie die Healbox einsetzen möchten:")

        self.add(lbl)

        # Create Radio Buttons
        rb1 = Gtk.RadioButton.new_with_label(
            None, "Ich möchte E-Mails lesen (standard)")
        rb1.connect("toggled", self.__set_deployment_mode,
                    self.DeploymentMode.READ_ONLY)
        rb2 = Gtk.RadioButton.new_with_label_from_widget(
            rb1, "Ich möchte E-Mails lesen und versenden")
        rb2.connect("toggled", self.__set_deployment_mode,
                    self.DeploymentMode.READ_SEND)
        rb3 = Gtk.RadioButton.new_with_label_from_widget(
            rb1, "Ich möchte die Healbox als E-Mail-Proxy verwenden (experimentell)")
        rb3.set_sensitive(False)
        rb3.connect("toggled", self.__set_deployment_mode,
                    self.DeploymentMode.PROXY)

        container = Gtk.VBox()
        container.add(rb1)
        container.add(rb2)
        container.add(rb3)

        self.add(container)

    def __set_deployment_mode(self, _, deployment_mode: DeploymentMode):
        self.deployment_mode = deployment_mode


class PagePassword(PageContainer):
    title = "Passwort für neuen Benutzer"
    completed = False

    def __init__(self):
        super().__init__()
        # Initialize Colors (Gdk.Color)
        self.clr_error = Gdk.RGBA()
        self.clr_error.parse("#ff0000")
        self.clr_error = self.clr_error.to_color()

        self.clr_warning = Gdk.RGBA()
        self.clr_warning.parse("#ffcc00")
        self.clr_warning = self.clr_warning.to_color()

        self.clr_success = Gdk.RGBA()
        self.clr_success.parse("#00cc00")
        self.clr_success = self.clr_success.to_color()

        GObject.signal_new("pw_sufficient", self,
                           GObject.SignalFlags.RUN_LAST, None, (bool,))

        self.pw1 = ""
        self.pw2 = ""
        self.pw_result = ""

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
        self.pw1 = self.__create_password_entry("Passwort")
        self.pw1.connect("changed", self.__do_handle_pw1_changed)
        self.pw2 = self.__create_password_entry("Passwort wiederholen")
        self.pw2.connect("changed", self.__do_handle_pw2_changed)

        self.pw2.set_sensitive(False)

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
        grid.attach(self.pw1, 1, 0, 1, 1)
        grid.attach(self.pw2, 1, 1, 1, 1)

        # password check result
        self.pw_result = Gtk.Label()
        self.pw_result.set_margin_top(5)

        pw_clr = Gdk.RGBA()
        pw_clr.parse("#ffcc00")

        self.pw_result.modify_fg(Gtk.StateType.NORMAL, pw_clr.to_color())
        self.pw_result.set_label("Bitte wählen Sie ein Passwort")

        grid.attach(self.pw_result, 1, 2, 1, 1)

        self.add(grid)

    @staticmethod
    def __create_password_entry(placeholder: str) -> Gtk.Entry:
        txt = Gtk.Entry()
        txt.set_placeholder_text(placeholder)
        txt.set_visibility(False)
        txt.set_input_purpose(Gtk.InputPurpose.PASSWORD)
        txt.set_halign(Gtk.Align.FILL)
        txt.set_hexpand(True)
        return txt

    def __do_handle_pw1_changed(self, _):
        self.password = self.pw1.get_text()
        self.pw1.set_progress_fraction(0)
        self.pw2.set_sensitive(False)

        if not self.password.strip():
            self.pw_result.modify_fg(Gtk.StateType.NORMAL, self.clr_error)
            self.pw_result.set_label("Das Passwort darf nicht leer sein!")
        else:
            pw_shell = subprocess.run(
                "/usr/bin/pwscore", input=self.password, capture_output=True, text=True)

            if (pw_shell.returncode != 0):
                self.pw_result.modify_fg(
                    Gtk.StateType.NORMAL, self.clr_error)
                self.pw_result.set_label(
                    pw_shell.stderr.splitlines()[-1].strip())
            else:
                pw_score = int(pw_shell.stdout)

                self.pw_result.modify_fg(
                    Gtk.StateType.NORMAL, self.clr_warning)
                self.pw_result.set_label(
                    f"Aktuelle Passwort-Stärke: {pw_score}")
                self.pw1.set_progress_fraction(pw_score / 100)

                # TODO Display minimum password score
                if (pw_score > 90):
                    self.pw_result.modify_fg(
                        Gtk.StateType.NORMAL, self.clr_success)
                    self.pw2.set_sensitive(True)

    def __do_handle_pw2_changed(self, _):
        if (self.pw1.get_text() == self.pw2.get_text()):
            self.pw_result.modify_fg(
                Gtk.StateType.NORMAL, self.clr_success)
            self.pw_result.set_label("Die Passwörter stimmen überein!")
            self.__emit_pw_sufficient(True)
        else:
            self.pw_result.modify_fg(
                Gtk.StateType.NORMAL, self.clr_error)
            self.pw_result.set_label(
                "Die Passwörter stimmen nicht überein!")
            self.__emit_pw_sufficient(False)

    def __emit_pw_sufficient(self, sufficient: bool):
        self.emit("pw_sufficient", sufficient)


class PageSelection(PageContainer):
    title = "Programme auswählen"

    def __init__(self):
        super().__init__()
        self.user_selection = {}
        self.__content()

    def __content(self):
        # Create Label
        lbl = Gtk.Label()
        lbl.set_justify(Gtk.Justification.LEFT)
        lbl.set_halign(Gtk.Align.START)
        lbl.set_margin_bottom(10)
        lbl.set_label(
            "Bitte wählen Sie die Programme aus, die installiert werden sollen:")

        self.add(lbl)

        # Create Check Boxes
        cb1 = Gtk.CheckButton.new_with_label(
            "Thunderbird (E-Mail Client)")
        cb1.connect("toggled", self.__set_user_selection, "cb1", "thunderbird")
        cb1.set_active(True)

        cb2 = Gtk.CheckButton.new_with_label(
            "LibreOffice (Office Anwendung)")
        cb2.connect("toggled", self.__set_user_selection,
                    "cb2", "libreoffice-writer")
        cb2.set_active(True)

        cb3 = Gtk.CheckButton.new_with_label(
            "ScreenShooter (Bildschirmfotos)")
        cb3.connect("toggled", self.__set_user_selection,
                    "cb3", "screenshooter")
        cb3.set_active(True)

        container = Gtk.VBox()
        container.add(cb1)
        container.add(cb2)
        container.add(cb3)

        self.add(container)

    def __set_user_selection(self, widget, key: str, value: str):
        if widget.get_active():
            self.user_selection[key] = value
        elif key in self.user_selection.keys():
            self.user_selection.pop(key)

    def get_package_list(self) -> str:
        return " ".join(self.user_selection.values())


class PageSummary(PageContainer):
    title = "Zusammenfassung"
    page_type = Gtk.AssistantPageType.CONFIRM

    def __init__(self):
        super().__init__()
        self.__content()

    def __content(self):
        lbl = Gtk.Label()
        lbl.set_justify(Gtk.Justification.LEFT)
        lbl.set_label("""
Folgende Änderungen werden am System vorgenommen:

Unnötige Dienste werden deaktiviert
Nicht notwendige Anwendungen entfernt
E-Mail & Office Anwendungen Installiert
Sicherheitseinstellungen angewendet
Berechtigungen angepasst
""")

        # TODO: Display system changes

        self.add(lbl)


class PageProgress(PageContainer):
    title = "Verlauf"
    page_type = Gtk.AssistantPageType.PROGRESS
    completed = False

    def __init__(self):
        super().__init__()
        self.pb = ""
        self.txtview = ""
        self.txtbuf = ""
        self.__content()

    def __content(self):
        # Fill entire page
        self.set_valign(Gtk.Align.FILL)

        # Add Progress Bar
        self.pb = Gtk.ProgressBar()
        self.pb.set_show_text(True)
        self.pb.set_valign(Gtk.Align.END)

        self.add(self.pb)

        # Add Expander
        exp = Gtk.Expander()
        exp.set_label("Mehr Informationen")
        exp.set_margin_top(10)

        # Add scroll window
        sw = Gtk.ScrolledWindow()
        # Allow terminal output to grow vertically
        sw.set_vexpand(True)

        # Add text box
        self.txtview = Gtk.TextView()
        self.txtview.set_editable(False)
        self.txtview.set_input_purpose(Gtk.InputPurpose.FREE_FORM)
        self.txtview.set_monospace(True)

        # Create text buffer
        self.txtbuf = Gtk.TextBuffer()

        # Create text mark
        self.txtmark = Gtk.TextMark.new(None, False)

        # Get text iterator at the end of the buffer
        self.end_iter = self.txtbuf.get_end_iter()

        # Add text mark at the end of the buffer
        self.txtbuf.add_mark(self.txtmark, self.end_iter)

        self.txtview.set_buffer(self.txtbuf)
        sw.add(self.txtview)
        exp.add(sw)
        self.add(exp)


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

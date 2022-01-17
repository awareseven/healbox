import string
import random
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk


class PageContainer(Gtk.VBox):
    title: str = "Page Title"
    page_type: int = Gtk.AssistantPageType.CONTENT
    completed: bool = True

    def __init__(self):
        super().__init__()
        self.set_valign(Gtk.Align.CENTER)

    def rand_string(strlen: int):
        return ''.join(random.choice(
            string.ascii_letters + string.digits
        ) for _ in range(strlen))

    username: str = "hb-" + rand_string(3)
    hostname: str = "healbox-" + rand_string(6)


class PageIntro(PageContainer):
    title = "Einführung"
    page_type = Gtk.AssistantPageType.INTRO

    def __init__(self):
        super().__init__()
        self.PageContent()

    def PageContent(self):
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

    def __init__(self):
        super().__init__()
        self.PageContent()

    def PageContent(self):
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
        rb2 = Gtk.RadioButton.new_with_label_from_widget(
            rb1, "Ich möchte E-Mails lesen und versenden")
        rb3 = Gtk.RadioButton.new_with_label_from_widget(
            rb1, "Ich möchte die Healbox als E-Mail-Proxy verwenden (experimentell)")
        rb3.set_sensitive(False)

        container = Gtk.VBox()
        container.add(rb1)
        container.add(rb2)
        container.add(rb3)

        self.add(container)


class PagePassword(PageContainer):
    title = "Passwort für neuen Benutzer"
    completed = False

    def __init__(self):
        super().__init__()
        self.PageContent()

    def PageContent(self):
        # password message
        lbl = Gtk.Label()
        lbl.set_label(
            f"Bitte setzen Sie ein sicheres Passwort für Ihren Healbox-Benutzer \"{self.username}\".")
        lbl.set_margin_bottom(20)
        lbl.set_halign(Gtk.Align.START)

        self.add(lbl)

        # password prompt
        self.pw1 = self.CreatePasswordEntry("Passwort")
        self.pw2 = self.CreatePasswordEntry("Passwort wiederholen")

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

    def CreatePasswordEntry(self, placeholder: str):
        txt = Gtk.Entry()
        txt.set_placeholder_text(placeholder)
        txt.set_visibility(False)
        txt.set_input_purpose(Gtk.InputPurpose.PASSWORD)
        txt.set_halign(Gtk.Align.FILL)
        txt.set_hexpand(True)
        return txt


class PageSelection(PageContainer):
    title = "Programme auswählen"

    def __init__(self):
        super().__init__()
        self.PageContent()

    def PageContent(self):
        # Create Label
        lbl = Gtk.Label()
        lbl.set_justify(Gtk.Justification.LEFT)
        lbl.set_halign(Gtk.Align.START)
        lbl.set_margin_bottom(10)
        lbl.set_label(
            "Bitte wählen Sie die Programme aus, die installiert werden sollen:")

        self.add(lbl)

        # Create Check Boxes
        self.cb1 = Gtk.CheckButton.new_with_label(
            "Thunderbird (E-Mail Client)")
        self.cb1.set_active(True)

        self.cb2 = Gtk.CheckButton.new_with_label(
            "LibreOffice (Office Anwendung)")
        self.cb2.set_active(True)

        self.cb3 = Gtk.CheckButton.new_with_label(
            "ScreenShooter (Bildschirmfotos)")
        self.cb3.set_active(True)

        container = Gtk.VBox()
        container.add(self.cb1)
        container.add(self.cb2)
        container.add(self.cb3)

        self.add(container)


class PageSummary(PageContainer):
    title = "Zusammenfassung"
    page_type = Gtk.AssistantPageType.CONFIRM

    def __init__(self):
        super().__init__()
        self.PageContent()

    def PageContent(self):
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
        self.PageContent()

    def PageContent(self):
        # Add Progress Bar
        self.pb = Gtk.ProgressBar()
        self.pb.set_text(
            "Es werden Änderungen an Ihrem System vorgenommen. Bitte warten.")
        self.pb.set_show_text(True)

        self.add(self.pb)

        # Add Expander
        expander = Gtk.Expander()
        expander.set_label("Mehr Informationen")
        expander.set_margin_top(10)

        tv = Gtk.TextView()
        tv.set_editable(False)
        tv.set_input_purpose(Gtk.InputPurpose.FREE_FORM)
        tv.set_monospace(True)

        txtbuf = Gtk.TextBuffer()
        txtbuf.set_text("Test-Ausgabe")

        tv.set_buffer(txtbuf)

        expander.add(tv)
        self.add(expander)


class PageResult(PageContainer):
    title = "Ergebnis"
    page_type = Gtk.AssistantPageType.SUMMARY

    def __init__(self):
        super().__init__()
        self.PageContent()

    def PageContent(self):
        lbl = Gtk.Label()
        lbl.set_justify(Gtk.Justification.LEFT)
        lbl.set_label(f"""
Das System ({self.hostname}) wurde angepasst.
Ein neuer Benutzer {self.username} wurde angelegt.
Starten Sie das System neu und melden Sie sich als neuer
Nutzer {self.username} an.
""")
        self.add(lbl)

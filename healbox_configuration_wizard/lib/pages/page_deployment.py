from enum import Enum

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from . import PageContainer


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

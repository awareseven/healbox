import os
import subprocess
from socket import gethostname

from gi.repository import GObject

from . import DeploymentMode


class ProcessExecutor(GObject.Object):
    __gsignals__ = {
        "cmd_max": (GObject.SIGNAL_RUN_LAST, None, (int,)),
        "cmd_step": (GObject.SIGNAL_RUN_LAST, None, (int,)),
        "cmd_out": (GObject.SIGNAL_RUN_LAST, None, (str,)),
    }

    def __emit_cmd_max(self, cmd_max: int):
        self.emit("cmd_max", cmd_max)

    def __emit_cmd_step(self, cmd_step: int):
        self.emit("cmd_step", cmd_step)

    def __emit_cmd_out(self, cmd_out: str):
        self.emit("cmd_out", cmd_out)

    def __init__(self):
        super().__init__()
        # Initialize command list to be executed by subprocess.Popen()
        self.cmd_list = []

    def __update_firewall(self):
        pass

    def __add_user(self, username: str):
        self.cmd_list.append(
            f"useradd -m -s /bin/bash -G sudo,netdev,users {username}")

    def __set_password(self, username: str, password: str):
        # self.cmd_list.append("echo '{0}:{1}' | chpasswd".format(
        #     system_changes["username"],
        #     system_changes["password"]
        # ))

        subprocess.run(
            ["/usr/sbin/chpasswd"],
            input="{0}:{1}".format(
                username,
                password
            ),
            text=True
        )

    def __update_hostname(self, new_hostname: str):
        self.cmd_list.append(
            "sed -i 's/\(127\.[0-9]\.[0-9]\.[0-9].*\){0}/\\1{1}/g' /etc/hosts".format(
                gethostname(),
                new_hostname
            ))
        self.cmd_list.append(f"hostnamectl set-hostname {new_hostname}")

    def __install_packages(self, package_list: str):
        self.cmd_list.append(f"apt-get update")
        self.cmd_list.append(
            f"apt-get install -y {package_list}")

    def __disable_autologin(self):
        self.cmd_list.append(
            "sed /etc/lightdm/lightdm.conf -i -e 's/^autologin-user=\w*/#autologin-user=/'")

    def __cleanup(self):
        HEALBOX_PATH = "/opt/healbox"
        SCRIPT_PATH = f"{HEALBOX_PATH}/healbox_cleanup.sh"
        CRON_PATH = "/etc/cron.d/healbox"

        self.cmd_list.append(f"""cat <<EOF >> {SCRIPT_PATH}
#!/usr/bin/env sh
PATH={os.getenv("PATH")}

userdel -fr {os.getenv("SUDO_USER")}
rm /etc/sudoers.d/healbox
rm -r {HEALBOX_PATH}
rm {CRON_PATH}
EOF
""")
        self.cmd_list.append(f"chmod u+x {SCRIPT_PATH}")
        self.cmd_list.append(
            f"echo '@reboot\troot\t{SCRIPT_PATH}' > {CRON_PATH}")

    def __init_step(self, cmd_step, cmd_out):
        self.__emit_cmd_step(cmd_step)
        self.__emit_cmd_out(cmd_out)

    @staticmethod
    def reboot():
        subprocess.run(["/usr/sbin/reboot"])

    def process_input(self, system_changes: dict):
        # TODO: Process User Input
        # [ ] Set up firewall (SMTP)
        # [x] New generated user
        # [x] Set password (requires libpwquality-tools)
        # [x] Change hostname
        # [x] Install selected packages
        # [x] Remove current user
        # [x] Remove script + dependencies
        # [x] Deactivate autologin
        # [x] Restore sudo configuration (revert exception to start wizard as root)
        # [ ] System restore on error

        # TODO Set up firewall
        if system_changes["deployment_mode"] == DeploymentMode.READ_SEND:
            self.__update_firewall()

        # Add new user
        self.__add_user(system_changes['username'])
        # self.__set_password(
        #     system_changes["username"],
        #     system_changes["password"]
        # )

        # Change hostname
        self.__update_hostname(system_changes["hostname"])

        # Install selected packages
        self.__install_packages(system_changes['package_list'])

        # Disable autologin
        self.__disable_autologin

        # Cleanup operations
        self.__cleanup()

        cmd_len = len(self.cmd_list)
        # Add password changing step
        cmd_max = cmd_len + 1

        self.__emit_cmd_max(cmd_max)

        for i in range(cmd_len):
            self.__init_step(i + 1, f"Command output [{self.cmd_list[i]}]:\n")

            p = subprocess.Popen(
                self.cmd_list[i],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                encoding="utf-8",
                shell=True
            )

            while True:
                std_out = p.stdout.readline()
                if std_out == "" and p.poll() is not None:
                    self.__emit_cmd_out("\n")
                    break

                self.__emit_cmd_out(std_out)

        # Set password
        self.__init_step(cmd_max, "Set password [/usr/sbin/chpasswd]")
        self.__set_password(
            system_changes["username"],
            system_changes["password"]
        )

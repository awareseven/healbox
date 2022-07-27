from enum import Enum
import random
import string


class DeploymentMode(Enum):
    READ_ONLY = 1
    READ_SEND = 2
    PROXY = 3


class ApplicationState:
    __instance = None

    def __init__(self):
        if ApplicationState.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            ApplicationState.__instance = self

            self.password: str = ""
            self.__user_selection: dict = {}
            self.__deployment_mode: DeploymentMode = DeploymentMode.READ_ONLY

            self.username: str = self.__get_random_username(3)
            self.hostname: str = self.__get_random_hostname(6)

    @staticmethod
    def get_instance():
        if ApplicationState.__instance == None:
            ApplicationState()
        return ApplicationState.__instance

    @staticmethod
    def __get_rand_string(string_length: int) -> str:
        return ''.join(random.choice(
            string.ascii_letters + string.digits
        ) for _ in range(string_length))

    def __get_random_username(self, rand_char_len: int) -> str:
        return "hb-" + self.__get_rand_string(rand_char_len)

    def __get_random_hostname(self, rand_char_len: int) -> str:
        return "healbox-" + self.__get_rand_string(rand_char_len)

    def __get_package_list(self) -> str:
        return " ".join(self.__user_selection.values())

    def set_deployment_mode(self, _, deployment_mode: DeploymentMode):
        self.__deployment_mode = deployment_mode

    def set_user_selection(self, widget, widget_id: str, packages: str):
        if widget.get_active():
            self.__user_selection[widget_id] = packages
        elif widget_id in self.__user_selection.keys():
            self.__user_selection.pop(widget_id)

    def get_application_state(self) -> dict:
        return {
            "deployment_mode": self.__deployment_mode,
            "package_list": self.__get_package_list(),
            "password": self.password,
            "username": self.username,
            "hostname": self.hostname,
        }

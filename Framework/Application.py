from abc import abstractmethod
from Framework.ParentComp import ParentComp


class Application(ParentComp):
    def __init__(self, parent=None, controller_name="", name=""):
        ParentComp.__init__(self, parent)
        self.controller_name = controller_name
        self.controllers = {}
        self.name = name

    @abstractmethod
    def execute(self):
        pass


    @abstractmethod
    def _get_controller(self, controller_name):
        pass

    @abstractmethod
    def _add_controller(self, controller_name, controller):
        pass
from Framework.ParentComp import ParentComp
from abc import abstractmethod


class Controller(ParentComp):
    def __init__(self, parent):
        ParentComp.__init__(self, parent)

    @abstractmethod
    def execute(self):
        pass

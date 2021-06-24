from abc import abstractmethod
from Framework.ParentComp import ParentComp
from Framework.Parser import Parser


class FrameModel(ParentComp):
    def __init__(self, parent):
        ParentComp.__init__(self, parent)
        self.parser = Parser()

    @abstractmethod
    def get_widgets_dict(self, files_api):
        pass

    @abstractmethod
    def _get_documents(self, files):
        pass

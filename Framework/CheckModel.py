from abc import abstractmethod
from ParentComp import ParentComp


class CheckModel(ParentComp):
    def __init__(self, parent):
        ParentComp.__init__(self, parent)

    @abstractmethod
    def report(self, dictionary):
        pass

    @abstractmethod
    def _check_item_presence(self, item_value):
        pass

    @abstractmethod
    def _check_string_expression(self, item_value):
        pass

    @abstractmethod
    def _get_item_checking_result(self, dictionary, item_value):
        pass
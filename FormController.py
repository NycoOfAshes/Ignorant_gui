from FormView import GuiView
from IgnorantModel import IgnorantModel
from FormModel import GuiModel


class FormController:
    def __init__(self, parent):
        self.parent = parent
        self.gui_model = GuiModel(self)
        self.ignorant_model = IgnorantModel(self)
        self.gui_view = GuiView(self)

    def execute(self, **kwargs):
        """
        Gets Gui parameters from the gui model, then transfers to the Gui view for displaying
        :param kwargs:
        :return: None
        """
        dictionaries = self.gui_model.get_objects_models(**kwargs)
        self.gui_view.display(dictionaries["doc"], dictionaries["dic"])

    def get_phone_infos(self, form_values):
        """
        Returns positive results from phone numbers searches from the ignorant model
        :param form_values:
        :return: positive results from phone numbers searches
        """
        return self.ignorant_model.report(form_values)

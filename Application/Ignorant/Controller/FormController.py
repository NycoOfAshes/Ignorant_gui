from Application.Ignorant.Model.FormModel import GuiModel
from Application.Ignorant.View.FormView import GuiView
from Application.Ignorant.Model.IgnorantModel import IgnorantModel
from Framework.Controller import Controller
import os


class FormController(Controller):
    def __init__(self, parent):
        Controller.__init__(self, parent)
        self.gui_model = GuiModel(self)
        self.gui_view = GuiView(self)
        self.ignorant_model = IgnorantModel(self)

    def execute(self):
        """
        Gets Gui parameters from the gui model, then transfers to the Gui view for displaying
        :return: None
        """
        app_name = self.get_parent().name
        path_name_1 = os.path.join("Application", app_name, "DB", "languages.json")
        path_name_2 = os.path.join("Application", app_name, "DB", "widgets.xml")
        dictionaries = self.gui_model.get_widgets_dict([(path_name_1, "JsonObjectSerializer"),
                                                        (path_name_2, "XmlTreeSerializer")])
        self.gui_view.display(dictionaries)

    def get_phone_infos(self, form_values):
        """
        Returns positive results from phone numbers searches from the ignorant model
        :param form_values:
        :return: positive results from phone numbers searches
        """
        return self.ignorant_model.report(form_values)

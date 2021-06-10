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
        dictionaries = self.gui_model.get_objects_models(**kwargs)
        self.gui_view.display(dictionaries["doc"], dictionaries["dic"])

    def get_phone_infos(self, form_values):
        return self.ignorant_model.report(form_values)
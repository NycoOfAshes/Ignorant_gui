from Framework.Application import Application
from Application.Ignorant.Controller.FormController import FormController


class IgnorantApplication(Application):

    def __init__(self, parent=None, controller_name="", name=""):
        Application.__init__(self, parent=parent, controller_name=controller_name, name=name)

    def execute(self):

        controller = self._get_controller(self.controller_name)
        controller.execute()

    def _get_controller(self, controller_name):

        if controller_name == "Form":
            controller = FormController(self)
        try:
            self._add_controller(controller_name, controller)
            return controller
        except:
            print("controller doesn't exists")

    def _add_controller(self, controller_name, controller):

        if controller_name not in self.controllers.keys():
            self.controllers[controller_name] = controller

from FormController import FormController

class Application:
    def __init__(self, parent=None):
        self.parent = parent
        self.controller = FormController(self)

    def execute(self, **kwargs):
        self.controller.execute(**kwargs)
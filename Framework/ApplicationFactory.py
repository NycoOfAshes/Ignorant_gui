from Application.Ignorant.IgnorantApp import IgnorantApplication


class ApplicationFactory:

    def get_app(self, app_name, controller):
        if app_name == "Ignorant":
            app = IgnorantApplication(controller_name=controller, name =app_name)
            return app


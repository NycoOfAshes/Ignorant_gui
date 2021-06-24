from Framework.ApplicationFactory import ApplicationFactory
"""
The bootstrap
"""

if __name__ == "__main__":
    app_fact = ApplicationFactory()
    app = app_fact.get_app(app_name="Ignorant", controller="Form")
    app.execute()

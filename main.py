from Application import Application
"""
The bootstrap
"""


if __name__ == "__main__":
    app = Application()
    app.execute(doc="widgets.xml", dic="languages.json")

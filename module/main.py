from m_gui import CalendrumApp

class Main:
    def __init__(self):
        self.__app:CalendrumApp = CalendrumApp()
    @property
    def app(self)->CalendrumApp:
        return self.__app

if __name__ == "__main__":
    Main().app.run()
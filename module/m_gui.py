import kivy
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen

kivy.require("2.3.1")

class CalendrumApp(MDApp):
    """App zur .kv.
    Ruft beim Aufruf dieses Objekts die eigene "build"-Methode auf,
    die das Layout der App erstellt.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        """Wird automatisch aufgerufen, wenn die App gestartet wird.
        Hier wird das Layout der App erstellt und danach der ScreenManager aufgerufen.
        Schriftarten und andere Einstellungen können hier vorgenommen werden.
        """
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Gray"

        return Manager()

"""Folgende Klassen müssen in der py definiert werden, 
damit sie in der .kv-Datei verwendet werden können.
Funktioniert auch ohne super()-Konstruktor, vielleicht aber nicht in allen Fällen."""

class Manager(MDScreenManager):
    """ScreenManager der App."""
    pass

class HomeScreen(MDScreen):
    """Startbildschirm der App."""
    pass






class Main:
    """Startet die App.
    Test-Code kann hier eingefügt werden."""
    CalendrumApp().run()

if __name__ == "__main__":
    Main()
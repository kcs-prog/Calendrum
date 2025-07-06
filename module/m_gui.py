import kivy
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from m_datumzeit import Datumzeit

kivy.require("2.3.1")

class CalendrumApp(MDApp):
    """App zur calendrum.kv.
    Ruft beim Aufruf dieses Objekts die eigene "build"-Methode auf,
    die das Layout der App erstellt.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__zeit = Datumzeit()# Initialisiert die Zeit- und Datumsobjekte.
        self.zeit.jetzt()# Aktuelles Datum und Uhrzeit werden gesetzt

    @property
    def zeit(self) -> Datumzeit:
        """Gibt das Datumzeit-Objekt zurück."""
        return self.__zeit

    def build(self) -> MDScreenManager:
        """Wird automatisch aufgerufen, wenn die App gestartet wird.
        Hier wird das Layout der App erstellt und danach der ScreenManager aufgerufen.
        Schriftarten und andere Einstellungen können hier vorgenommen werden.
        """
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Gray"

        return Manager()

    def update_jahr(self) -> None:
        """Methode zum Updaten des Jahres im HomeScreen beim Klicken des Buttons."""
        home_screen = self.root.get_screen("home")
        home_screen.ids.jahr_auswahl.text = str(self.zeit.jahr)

    def update_monat(self) -> None:
        """Methode zum Updaten des Monats im HomeScreen beim Klicken des Buttons."""
        home_screen = self.root.get_screen("home")
        home_screen.ids.monat_auswahl.text = str(self.zeit.monat)


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
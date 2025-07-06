"""
Hauptmodul des GUIs. Hier wird die App gestartet und das Layout des Home-Bildschirms definiert.
"""

import kivy
from kivy.clock import Clock
from kivy.properties import StringProperty
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
    uhrzeit = StringProperty()  # Uhrzeit wird als StringProperty definiert, um sie im KV-Layout zu verwenden.
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.zeit = Datumzeit()# Initialisiert die Zeit- und Datumsobjekte.
        self.zeit.jetzt()
        self.uhrzeit = f"{self.zeit.stunde:02d}:{self.zeit.minute:02d}:{self.zeit.sekunde:02d} Uhr"
        self.monate_deutsch = ["Januar", "Februar", "März", "April", "Mai", "Juni","Juli", "August", "September", "Oktober", "November", "Dezember"]

    @property
    def home_screen(self) -> MDScreen:
        """Gibt den HomeScreen zurück."""
        return self.root.get_screen("home")

    def update_monat(self) -> None:
        """Methode zum Updaten des Monats im HomeScreen beim Klicken des Buttons."""
        try:
            self.home_screen.ids.monat_anzeige.text = self.monate_deutsch[self.zeit.get_monat() - 1]
        except Exception as e:
            print(f"Error updating month: {e}")

    def update_jahr(self) -> None:
        """Methode zum Updaten des Jahres im HomeScreen beim Klicken des Buttons."""
        try:
            current_year = self.zeit.get_jahr()
            if current_year is not None:
                self.home_screen.ids.jahr_anzeige.text = str(current_year)
        except Exception as e:
            print(f"Error updating year: {e}")

    def update_uhrzeit(self, *args) -> None:
        """Aktualisiert die Uhrzeit im HomeScreen jede Sekunde."""
        self.zeit.jetzt()
        self.uhrzeit = f"{self.zeit.stunde:02d}:{self.zeit.minute:02d}:{self.zeit.sekunde:02d} Uhr"

    def build(self) -> MDScreenManager:
        """Wird automatisch aufgerufen, wenn die App gestartet wird.
        Hier wird das Layout der App erstellt und danach der ScreenManager aufgerufen.
        Schriftarten und andere Einstellungen können hier vorgenommen werden.
        """
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Gray"

        Clock.schedule_interval(self.update_uhrzeit, 1) # Aktualisiert die Zeit jede Sekunde

        return Manager()


"""Folgende Klassen müssen in der .py definiert werden, 
damit sie in der .kv-Datei verwendet werden können.
Funktioniert auch ohne super()-Konstruktor, vielleicht aber nicht in allen Fällen."""

class Manager(MDScreenManager):
    """ScreenManager der App."""
    pass

class HomeScreen(MDScreen):
    """Startbildschirm der App."""
    pass

"""Main Klasse OOP"""

class Main:
    """Startet die App.
    Test-Code kann hier eingefügt werden."""
    CalendrumApp().run()

if __name__ == "__main__":
    Main()
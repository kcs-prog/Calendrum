"""
Hauptmodul des GUIs. Hier wird die App gestartet und das Layout des Home-Bildschirms definiert.
"""

import kivy
from kivy.core.text import LabelBase
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from m_eventman import Eventman
from m_datumzeit import Datumzeit

kivy.require("2.3.1")


class CalendrumApp(MDApp):
    """App zur calendrum.kv.
    Ruft beim Aufruf dieses Objekts die eigene "build"-Methode auf,
    die das Layout der App erstellt.
    """

    uhrzeit: str = StringProperty()  # Uhrzeit wird als StringProperty definiert, um sie im KV-Layout zu verwenden.
    zeit: Datumzeit = Datumzeit()
    try: zeit.jetzt()  # Setzt die aktuelle Zeit, wenn die App gestartet wird
    except Exception as e: print(f"Error initializing time: {e}")
    monat: int = zeit.monat  # Kopie des Monats zum schutz gegen das Update für die Uhrzeit
    jahr: int = zeit.jahr  # Kopie des Jahres zum schutz gegen das Update für die Uhrzeit

    eventman: Eventman = Eventman()  # Instanz der Eventman-Klasse, um Ereignisse zu verwalten
    dialog:MDDialog = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.uhrzeit = f"{self.zeit.stunde:02d}:{self.zeit.minute:02d}:{self.zeit.sekunde:02d} Uhr"
        self.monate_deutsch = ["Jan.", "Feb.", "März", "April", "Mai", "Juni",
                               "Juli", "Aug.", "Sep.", "Okt.", "Nov.", "Dez."]

    @property
    def home_screen(self) -> MDScreen:
        """Gibt den HomeScreen zurück."""
        return self.root.get_screen("home")

    def monat_plus(self) -> None:
        """Methode zum Erhöhen des Monats im HomeScreen beim Klicken des Buttons."""
        try:
            if self.monat < 12:
                self.monat += 1
            else:
                self.monat = 1
                self.jahr += 1
            self.__update_monat()
            self.__update_jahr()
        except Exception as e:
            print(f"Error updating month: {e}")

    def monat_minus(self) -> None:
        """Methode zum Verringern des Monats im HomeScreen beim Klicken des Buttons."""
        try:
            if self.monat > 1:
                self.monat -= 1
            else:
                self.monat = 12
                self.jahr -= 1
            self.__update_monat()
            self.__update_jahr()
        except Exception as e:
            print(f"Error updating month: {e}")

    def __update_monat(self) -> None:
        """Methode zum Updaten des Monats im HomeScreen beim Klicken des Buttons."""
        try:
            self.home_screen.ids.monat_anzeige.text = self.monate_deutsch[self.monat - 1]
        except Exception as e:
            print(f"Error updating month: {e}")

    def jahr_plus(self) -> None:
        """Methode zum Erhöhen des Jahres im HomeScreen beim Klicken des Buttons."""
        try:
            self.jahr += 1
            self.__update_jahr()
        except Exception as e:
            print(f"Error updating year: {e}")

    def jahr_minus(self) -> None:
        """Methode zum Verringern des Jahres im HomeScreen beim Klicken des Buttons."""
        try:
            self.jahr -= 1
            self.__update_jahr()
        except Exception as e:
            print(f"Error updating year: {e}")

    def __update_jahr(self) -> None:
        """Methode zum Updaten des Jahres im HomeScreen beim Klicken des Buttons."""
        try:
            current_year = self.jahr
            if current_year is not None:
                self.home_screen.ids.jahr_anzeige.text = str(current_year)
        except Exception as e:
            print(f"Error updating year: {e}")

    def _update_uhrzeit(self, *args) -> None:  # *args ist notwendig, für Clock.schedule_interval
        """Aktualisiert die Uhrzeit im HomeScreen jede Sekunde."""
        self.zeit.jetzt()
        self.uhrzeit = f"{self.zeit.stunde:02d}:{self.zeit.minute:02d}:{self.zeit.sekunde:02d} Uhr"

    def open_wecker_dialog(self) -> None:
        """Öffnet den Dialog zum Einstellen des Weckers."""
        if not self.dialog:
            self.dialog = MDDialog(
                text="Wecker einstellen",
                pos_hint={"center_x": 0.5},
                buttons=[
                    MDIconButton(
                        icon="close-circle",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        pos_hint ={"center_x": 0.5},
                        on_release=lambda x: self.dialog.dismiss()
                    ),

                ],
            )
        self.dialog.open()

    def build(self) -> MDScreenManager:
        """Wird automatisch aufgerufen, wenn die App gestartet wird.
        Hier wird das Layout der App erstellt und danach der ScreenManager aufgerufen.
        Schriftarten und andere Einstellungen können hier vorgenommen werden.
        """
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Gray"
        self.theme_cls.primary_hue = "500"
        # Hier werden die Schriftarten für die App definiert.
        LabelBase.register(
            name="jetbrains",
            fn_regular="assets/fonts/JetBrainsMono-Regular.ttf",
        )
        self.theme_cls.font_styles.update({
            "H1": ["jetbrains", 90, True, 0.15],
            "H2": ["jetbrains", 60, False, -0.05],
            "H3": ["jetbrains", 48, False, 0],
            "H4": ["jetbrains", 34, False, 0.25],
            "H5": ["jetbrains", 24, False, 0],
            "H6": ["jetbrains", 20, False, 0.15],
            "Subtitle1": ["jetbrains", 16, False, 0.15],
            "Subtitle2": ["jetbrains", 14, False, 0.1],
            "Body1": ["jetbrains", 16, False, 0.5],
            "Body2": ["jetbrains", 14, False, 0.25],
            "Button": ["jetbrains", 14, True, 1.25],
            "Caption": ["jetbrains", 12, False, 0.4],
            "Overline": ["jetbrains", 10, True, 1.5],
        })

        Clock.schedule_interval(self._update_uhrzeit, 1)  # Aktualisiert die Zeit jede Sekunde
        Clock.schedule_interval(self.eventman.event_trigger, 1) # Triggert abgelaufene Events jede Sekunde

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

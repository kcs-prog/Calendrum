"""
Hauptmodul des GUIs. Hier wird die App gestartet und das Layout des Home-Bildschirms definiert.
"""

import kivy
from kivy.core.text import LabelBase
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from scripts.m_eventman import Eventman
from scripts.m_datumzeit import Datumzeit
from scripts.m_gui_TagFeld import TagFeld

kivy.require("2.3.1")


class CalendrumApp(MDApp):
    """App zur calendrum.kv.
    Ruft beim Aufruf dieses Objekts die eigene "build"-Methode auf,
    die das Layout der App erstellt.
    """

    _uhrzeit: str = StringProperty() # Uhrzeit wird als StringProperty definiert, um sie im KV-Layout zu verwenden.
    _zeit: Datumzeit = Datumzeit()
    try: _zeit.jetzt()  # Setzt die aktuelle Zeit, wenn die App gestartet wird
    except Exception as e: print(f"Error initializing time: {e}")
    _monat: int = _zeit.monat  # Kopie des Monats zum schutz gegen das Update für die Uhrzeit
    _jahr: int = _zeit.jahr  # Kopie des Jahres zum schutz gegen das Update für die Uhrzeit
    eventman: Eventman = Eventman()  # Instanz der Eventman-Klasse, um Ereignisse zu verwalten
    dialog:MDDialog = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._uhrzeit:str = f"{self._zeit.stunde:02d}:{self._zeit.minute:02d}:{self._zeit.sekunde:02d} Uhr"
        self.__button_namen:list[str] = ["jahr_plus", "jahr_minus", "monat_plus", "monat_minus"] # für _handle_button_input()
        self._monate_deutsch:list[str] = ["Jan.", "Feb.", "März", "Apr.", "Mai", "Juni",
                                        "Juli", "Aug.", "Sep.", "Okt.", "Nov.", "Dez."]

    @property
    def home_screen(self) -> MDScreen:
        """Gibt den HomeScreen zurück."""
        return self.root.get_screen("home")

    @property
    def wecker_screen(self) -> MDScreen:
        return self.root.get_screen("wecker")

    def _handle_button_input(self, button_name:str) -> None:
        """ Verarbeitet die Eingaben der Buttons im HomeScreen.
        :param button_name: Name des Buttons, der gedrückt wurde.
        """
        if not isinstance(button_name, str):
            raise ValueError("button_name must be a string")
        if button_name not in self.__button_namen:
            raise ValueError(f"Invalid button_name: {button_name}")
        match button_name:
            case "monat_plus":
                if self._monat < 12:
                    self._monat += 1
                else:
                    self._monat = 1
                    self._jahr += 1
            case "monat_minus":
                if self._monat > 1:
                    self._monat -= 1
                else:
                    self._monat = 12
                    self._jahr -= 1
            case "jahr_plus":
                self._jahr += 1
            case "jahr_minus":
                self._jahr -= 1
        self.__update_anzeige()
        return None

    def __update_anzeige(self) -> None:
        """Aktualisiert die Anzeige des Monats und des Jahres im HomeScreen."""
        self.home_screen.ids.monat_anzeige.text = self._monate_deutsch[self._monat - 1]
        self.home_screen.ids.jahr_anzeige.text = str(self._jahr)

        self.gen_tagegrid()

    def _update_uhrzeit(self, *args) -> None:  # *args ist notwendig, für Clock.schedule_interval
        """Aktualisiert die Uhrzeit im HomeScreen jede Sekunde."""
        self._zeit.jetzt()
        self._uhrzeit = f"{self._zeit.stunde:02d}:{self._zeit.minute:02d}:{self._zeit.sekunde:02d} Uhr"

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
            fn_regular="./assets/fonts/JetBrainsMono-Regular.ttf", # ist open-source free to use
        )
        self.theme_cls.font_styles.update({
        #   Name: [Familie, Größe, fett, Abstand zwischen Buchstaben]
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

        manager:Manager = Manager()
        return manager

    def on_start(self):
        """Wird automatisch nach build() aufgerufen.
        Alle Prozesse und Parameter, die davon abhängen, dass build() fertig ist, können hier gestartet werden.
        """
        self.gen_tagegrid()

    def gen_tagegrid(self):
        container = self.home_screen.ids.kalender_grid
        container.clear_widgets()

        # Headerzeile
        for wd in ["Mo","Di","Mi","Do","Fr","Sa","So"]:
            tag = TagFeld(wd)
            container.add_widget(tag)
        # Leertage setzen um den 1ten am richtigen Platz starten zu lassen
        # nach Zeller-Formel
        y,m = self._jahr, self._monat
        # Monat anpassen: Januar und Februar als Monate 13 und 14 des Vorjahres
        if m < 3:
            m += 12
            y -= 1
        h = (-1 + ((13 * (m + 1)) // 5) + y + (y // 4) - (y // 100) + (y // 400)) % 7
        # h: 0:Mo ... 6:So
        for _ in range(h):
            tag = TagFeld("")
            container.add_widget(tag)

        # Eigentliche Kalendertage auffüllen
        tage = self._zeit.max_tage(self._monat, self._jahr)
        for i in range(tage):
            tag = TagFeld(str(i+1),[])
            container.add_widget(tag)

        # rest auffüllen mit Leertagen
        for _ in range(42-h-tage):
            tag = TagFeld("")
            container.add_widget(tag)



"""Folgende Klassen müssen in der .py definiert werden, 
damit sie in der .kv-Datei verwendet werden können.
Funktioniert auch ohne super()-Konstruktor, vielleicht aber nicht in allen Fällen."""


class Manager(MDScreenManager):
    """ScreenManager der App."""
    pass


class HomeScreen(MDScreen):
    """Startbildschirm der App."""
    pass


class WeckerScreen(MDScreen):
    """Screen für das Einstellen des Weckers."""
    pass


if __name__ == "__main__":
    #App: CalendrumApp = CalendrumApp()
    #App.run()
    """run() startet die App und ruft automatisch build() auf.
    Nach build() wird on_start() automatisch aufgerufen."""

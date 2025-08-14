"""
Modul: m_kalender

Zentrale Verwaltung von Terminen, Weckern und Feiertagen.
Bietet Methoden zum Anlegen, Entfernen, Anzeigen und Sortieren,
sowie zur Erzeugung eines Monatsrasters.

"""

from scripts.m_datumzeit import Datumzeit
from scripts.m_eventman import Eventman
from scripts.m_wecker_termine import Wecker

from typing import List, Tuple, Union
import calendar


class Kalender:
    """
    Die Klasse Kalender verwaltet:
      - Termine: Datumzeit + Beschreibung
      - Wecker: Datumzeit + Event-Anbindung
      - Feiertage: Datumzeit (optional mit Name) oder String

    Sie bietet Methoden zum Hinzufügen, Entfernen, Anzeigen,
    Sortieren und zur Monatsberechnung.
    """

    def __init__(self, termin_liste:list):
        """
        Initialisiert einen Kalender mit leeren Listen für Termine, Wecker und Feiertage.
        """
        self.termine = termin_liste         # Liste von (Datumzeit, Name)-Tupeln
        self.wecker_list = []     # Liste von Wecker-Objekten
        self.feiertage = []       # Liste von Feiertagen (Datumzeit-Objekte oder Strings)
        self.kalender_array = []  # Monatsdarstellung (z.B. 2D-Array für Tage)

    def create_termin(self, datumzeit: Datumzeit, name: str) -> None:
        """
        Legt einen neuen Termin an.
        Duplikate werden bei identischem Datum+Name nicht erneut hinzugefügt.

        :param datumzeit: Datum und Uhrzeit des Termins
        :param name: Bezeichnung des Termins
        """
        eintrag = (datumzeit, name)
        if eintrag not in self.termine:
            self.termine.append(eintrag)

    def remove_termin(self, index: int) -> bool:
        """
        Entfernt einen Termin nach Listenindex.

        :param index: Position in der Termine-Liste
        :return: True wenn entfernt, False bei fehlerhaftem Index
        """
        if 0 <= index < len(self.termine):
            del self.termine[index]
            return True
        return False

    def create_wecker(self, datumzeit: Datumzeit, eventman: Eventman) -> None:
        """
        Erstellt einen neuen Wecker mit Eventbindung.

        :param datumzeit: Zeitpunkt des Alarms
        :param eventman: Eventmanager zur Auslösung
        """
        wecker = Wecker(datumzeit, eventman)
        if all(w.get_datumzeit() != datumzeit for w in self.wecker_list):
            self.wecker_list.append(wecker)

    def remove_wecker(self, index: int) -> bool:
        """
        Entfernt einen Wecker nach Listenindex.

        :param index: Position in der Wecker-Liste
        :return: True bei Erfolg, False sonst
        """
        if 0 <= index < len(self.wecker_list):
            del self.wecker_list[index]
            return True
        return False

    def add_feiertag(self, feiertag: Union[Datumzeit, Tuple[Datumzeit, str], str]) -> None:
        """
        Fügt einen Feiertag hinzu. 
        Akzeptiert Datumzeit, Tupel(Datumzeit, Name) oder String.
        Doppelte Einträge werden ignoriert.

        :param feiertag: Datumzeit oder (Datumzeit, Name) oder Name
        """
        if feiertag not in self.feiertage:
            self.feiertage.append(feiertag)

    def remove_feiertag(self, index: int) -> bool:
        """
        Entfernt einen Feiertag nach Index.

        :param index: Position in der Feiertags-Liste
        :return: True wenn entfernt, False bei ungültigem Index
        """
        if 0 <= index < len(self.feiertage):
            del self.feiertage[index]
            return True
        return False

    def ist_feiertag(self, datum: Datumzeit) -> bool:
        """
        Prüft, ob ein Datum als Feiertag gespeichert ist.

        :param datum: zu prüfendes Datum
        :return: True wenn ein passender Eintrag existiert
        """
        for ft in self.feiertage:
            if isinstance(ft, Datumzeit) and ft == datum:
                return True
            if isinstance(ft, tuple) and ft[0] == datum:
                return True
        return False

    def termine_anzeigen(self) -> List[str]:
        """
        Gibt alle Termine sortiert (nach Datumzeit) aus.

        :return: Formatierte Termin-Strings
        """
        self.termine.sort(key=lambda x: (
            x[0].jahr, x[0].monat, x[0].tag, x[0].stunde, x[0].minute
        ))
        ausgabe = [f"{str(dz)} – {name}" for dz, name in self.termine]
        for zeile in ausgabe:
            print(zeile)
        return ausgabe

    def wecker_anzeigen(self) -> List[str]:
        """
        Gibt alle Wecker sortiert (nach Datumzeit) aus.

        :return: Formatierte Wecker-Strings
        """
        self.wecker_list.sort(key=lambda w: (
            w.get_datumzeit().jahr,
            w.get_datumzeit().monat,
            w.get_datumzeit().tag,
            w.get_datumzeit().stunde,
            w.get_datumzeit().minute
        ))
        ausgabe = [f"Wecker: {str(w.get_datumzeit())}" for w in self.wecker_list]
        for zeile in ausgabe:
            print(zeile)
        return ausgabe

    def feiertage_anzeigen(self) -> List[str]:
        """
        Gibt alle Feiertage aus (Datum + optional Name).

        :return: Formatierte Feiertags-Strings
        """
        ausgabe = []
        for ft in self.feiertage:
            if isinstance(ft, tuple):
                dz, name = ft
                ausgabe.append(f"{str(dz)} – {name}")
            else:
                ausgabe.append(str(ft))
        for zeile in ausgabe:
            print(zeile)
        return ausgabe

    def wechsle_zu(self, monat: int, jahr: int) -> None:
        """
        Erzeugt ein Monatsraster für den angegebenen Monat und speichert es.

        :param monat: 1–12
        :param jahr: z. B. 2025
        """
        self.kalender_array = self._berechne_kalender(monat, jahr)

    def _berechne_kalender(self, monat: int, jahr: int) -> List[int]:
        """
        Berechnet alle Tageszahlen eines Monats.

        :param monat: 1–12
        :param jahr: ganzzahliges Jahr
        :return: Liste der Tageszahlen (1…letzter Tag)
        """
        tage = calendar.monthrange(jahr, monat)[1]
        return list(range(1, tage + 1))

    def clear_all(self) -> None:
        """
        Entfernt alle Termine, Wecker und Feiertage.
        """
        for event in self.termine:
            print(f"{event.zeit[0]}-{event.zeit[1]}-{event.zeit[2]} {event.zeit[3]}:{event.zeit[4]} - {event.name}")

    def wecker_anzeigen(self):
        """
        Gibt alle Wecker im Kalender aus.
        """
        for wecker in self.wecker_list:
            dz = wecker.get_datumzeit()
            print(f"Wecker: {dz.jahr}-{dz.monat:02}-{dz.tag:02} {dz.stunde:02}:{dz.minute:02}")

if __name__ == "__main__":
    # Kleiner Funktionstest
    dz = Datumzeit()
    dz.jetzt()
    em = Eventman()
    kalender = Kalender([])
    kalender.create_termin(dz, "Automatisch erzeugter Termin")
    kalender.create_wecker(dz, em)
    kalender.termine_anzeigen()
    kalender.wecker_anzeigen()
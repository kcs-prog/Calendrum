from m_datumzeit import Datumzeit
from m_eventman import Eventman
from m_wecker_termine import Wecker

class Kalender:
    """
    Die Klasse Kalender verwaltet Termine, Wecker und Feiertage.
    Sie bietet Methoden zum Hinzufügen von Terminen und Weckern sowie zum Wechseln des Monats/Jahres.
    """

    def __init__(self):
        """
        Initialisiert einen Kalender mit leeren Listen für Termine, Wecker und Feiertage.
        """
        self.termine = []         # Liste von (Datumzeit, Name)-Tupeln
        self.wecker_list = []     # Liste von Wecker-Objekten
        self.feiertage = []       # Liste von Feiertagen (Datumzeit-Objekte oder Strings)
        self.kalender_array = []  # Monatsdarstellung (z.B. 2D-Array für Tage)

    def create_termin(self, datumzeit: Datumzeit, name: str):
        """
        Fügt einen neuen Termin zum Kalender hinzu.

        :param datumzeit: Datumzeit-Objekt für den Termin
        :param name: Name oder Beschreibung des Termins
        """
        self.termine.append((datumzeit, name))

    def create_wecker(self, datumzeit: Datumzeit, eventman: Eventman):
        """
        Erstellt einen neuen Wecker und fügt ihn der Weckerliste hinzu.

        :param datumzeit: Datumzeit-Objekt für den Weckzeitpunkt
        :param eventman: Eventman-Objekt zur Verwaltung von Events
        """
        wecker = Wecker(datumzeit, eventman)
        self.wecker_list.append(wecker)

    def wechsle_zu(self, monat: int, jahr: int):
        """
        Aktualisiert die Kalenderdarstellung für einen neuen Monat und ein neues Jahr.

        :param monat: Monat (1-12)
        :param jahr: Jahr (z.B. 2025)
        """
        self.kalender_array = self._berechne_kalender(monat, jahr)

    def _berechne_kalender(self, monat: int, jahr: int):
        """
        Erstellt eine einfache Liste aller Tage des angegebenen Monats.

        :param monat: Monat (1-12)
        :param jahr: Jahr (z.B. 2025)
        :return: Liste der Tageszahlen im Monat
        """
        import calendar
        tage = calendar.monthrange(jahr, monat)[1]
        return list(range(1, tage + 1))

    def termine_anzeigen(self):
        """
        Gibt alle Termine im Kalender aus.
        """
        for dz, name in self.termine:
            print(f"{dz.jahr}-{dz.monat:02}-{dz.tag:02} {dz.stunde:02}:{dz.minute:02} - {name}")

    def wecker_anzeigen(self):
        """
        Gibt alle Wecker im Kalender aus.
        """
        for wecker in self.wecker_list:
            dz = wecker.get_datumzeit()
            print(f"Wecker: {dz.jahr}-{dz.monat:02}-{dz.tag:02} {dz.stunde:02}:{dz.minute:02}")

if __name__ == "__main__":
    # Beispielhafter Test
    dz = Datumzeit(2025, 6, 23, 8, 0, 0)
    em = Eventman()
    kalender = Kalender()
    kalender.create_termin(dz, "Arzttermin")
    kalender.create_wecker(dz, em)
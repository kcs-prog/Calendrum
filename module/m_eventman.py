"""
Eventman
————————————
-Event-Liste:dict{EventID:Event} #Event-Liste im Format {EventID:int: list[list[int], Event-Aktion: str, Event-Name: str]}.
-System-Zeit:list[int] #Aktuelle Systemzeit.
-Event-Aktionen:list[str] #Liste der verfügbaren Event-Aktionen.
————————————
-init() → None
-events_laden() → None
-events_speichern() → None
-event_abgelaufen(event_zeit: list[int]) → bool
+trigger_event() → list[str]
+event_erstellen(event_zeit: list[int], event_akt: str, event_name: str = "") → None
+event_aufrufen(event_id: int) → list[list[int], str, str] | None
+event_entfernen(event_id: int) → None

"""
from m_datumzeit import Datumzeit
from csv import writer, reader
import ast


class Eventman:
    """Eventman-Klasse zur Verwaltung von Events.
    Diese Klasse ermöglicht das Erstellen, Aufrufen und Entfernen von Events.
    Die Events werden in einer CSV-Datei gespeichert und können über eine Event-ID verwaltet werden.
    Löst automatisch abgelaufene Events aus, wenn die Klasse instanziiert wird.
    _____________Attribute:_____________________
        __zeit (Datumzeit): Datumzeit-Objekt.
        __system_zeit (list[int]): Aktuelle Systemzeit.
        __event_liste (dict[int: list]): Event-Liste im Format {Event-ID:int: list[list[int], Event-Aktion: str, Event-Name: str]}.
        __event_aktionen (list[str]): Liste der verfügbaren Event-Aktionen.
    _____________Methoden:______________________
        event_erstellen(event_zeit: list[int], event_akt: str, event_name: str) → None: Fügt ein Event der Liste hinzu und speichert es in der CSV-Datei.
        event_aufrufen(event_id: int) → list[list[int], str, str]: Ruft ein Event anhand der Event-ID auf und gibt es zurück.
        event_entfernen(event_id: int) → None: Entfernt ein Event anhand der Event-ID aus der Event-Liste und CSV-Datei.
        trigger_event() → list[str] | None: Überprüft, ob Events abgelaufen sind und löst sie aus.
    """
    EVENTS_CSV = 'events.csv'  # CSV-Datei, in der die Events gespeichert werden

    def __init__(self) -> None:
        """Initialisiert die Eventman-Klasse und lädt die Events aus der CSV-Datei.\
        Setzt die aktuelle Systemzeit und initialisiert die Event-Liste und verfügbaren Event-Aktionen.\
        """
        self.__zeit:Datumzeit = Datumzeit()  # Aktuelle Systemzeit
        self.__zeit.jetzt()
        self.__system_zeit:list[int] = [self.__zeit.jahr,
                                        self.__zeit.monat,
                                        self.__zeit.tag,
                                        self.__zeit.stunde,
                                        self.__zeit.minute,
                                        self.__zeit.sekunde] # Zeitstempel der aktuellen Systemzeit
        # Event-Liste im Format {EventID:int:list[list[int], Event-Aktion:str, Event-Name:str]}
        self.__event_liste: dict[int: list] = {}
        # Liste der verfügbaren Event-Aktionen
        self.__event_aktionen: list[str] = ["klingeln", "email", "sms", "anruf", "alarm", "test"]
        self.__events_laden()  # Lädt die Events aus der CSV-Datei
        self.event_trigger() # Überprüft, ob die Events bereits ausgelöst werden sollten

    @property
    def system_zeit(self) -> list[int]:
        """Gibt die aktuelle Systemzeit zurück.\
        :return:list[int] # Aktuelle Systemzeit als list[int]-Objekt.\
        """
        return self.__system_zeit

    @property
    def event_liste(self) -> dict[int:list]:
        """Gibt die Event-Liste zurück.\
        :return:dict[int: list[list[int], str, str]]
        #Event-Liste im Format {EventID:int: list[list[int], Event-Aktion: str, Event-Name: str]}\
        """
        return self.__event_liste

    @event_liste.setter
    def event_liste(self, new__event_liste: dict[int:list,str,str]) -> None:
        """Setzt eine neue Event-Liste und speichert sie in CSV.\
        :param new__event_liste:dict[int: list[list[int], str, str]]
        #Neue Event-Liste im Format {EventID:int: list[list[int], Event-Aktion: str, Event-Name: str]}\
        :raises exception: Bei falschem Typ der neuen Event-Liste.\
        """
        if not isinstance(new__event_liste, dict):
            raise Exception("Neue Event-Liste muss vom Typ 'dict' sein.\n")
        self.__event_liste = new__event_liste
        self.__events_speichern()

    @property
    def event_aktionen(self) -> list[str]:
        """Gibt die Liste der verfügbaren Event-Aktionen zurück.\
        :return:list[str] #Liste der verfügbaren Event-Aktionen.\
        :raises exception: Bei leerer Event-Aktionsliste.\
        """
        if not self.__event_aktionen:
            raise Exception("Aktions-Liste ist leer.\n")
        return self.__event_aktionen

    @event_aktionen.setter
    def event_aktionen(self, _new_event_aktionen: list[str]) -> None:
        """Setzt eine neue Liste von Event-Aktionen.\
        :param _new_event_aktionen:list[str] #Neue Liste der verfügbaren Event-Aktionen.\
        :raises exception: Bei falschem Typ der neuen Event-Aktionsliste.\
        """
        if not isinstance(_new_event_aktionen, list) or not all(isinstance(a, str) for a in _new_event_aktionen):
            raise Exception("Aktions-Liste muss eine Liste von Strings sein.\n")
        self.__event_aktionen = _new_event_aktionen

    def __events_laden(self) -> None:
        """Lädt die Events aus der CSV-Datei in die Event-Liste.\
        Erstellt die Datei, falls sie nicht existiert.\
        :raises exception: Bei Fehlern beim Laden der Events aus der CSV-Datei.\
        """
        try:
            with open(self.EVENTS_CSV, 'r', encoding='utf-8') as f:
                csv_reader = reader(f)
                next(csv_reader)
                self.__event_liste = {
                    int(row[0]): [ast.literal_eval(row[1]), row[2], row[3].strip()]
                    for row in csv_reader if row
                }
        except FileNotFoundError:
            with open(self.EVENTS_CSV, 'w', newline='', encoding='utf-8') as f:
                csv_writer = writer(f)
                csv_writer.writerow(['EventID', 'Zeitstempel', 'Aktion', 'Name'])

    def __events_speichern(self) -> None:
        """Speichert die aktuelle Event-Liste in der CSV-Datei.\
        """
        with open(self.EVENTS_CSV, 'w', newline='', encoding='utf-8') as f:
            csv_writer = writer(f)
            csv_writer.writerow(['EventID', 'Zeitstempel', 'Aktion', 'Name'])
            for event_id, event_data in self.__event_liste.items():
                csv_writer.writerow([event_id, [self.system_zeit[0],
                                            self.system_zeit[1],
                                            self.system_zeit[2],
                                            self.system_zeit[3],
                                            self.system_zeit[4],
                                            self.system_zeit[5]], event_data[1], event_data[2]])

    def __event_abgelaufen(self, event_zeit:list[int]) -> bool:
        """Prüft, ob ein Event-Zeitstempel abgelaufen ist.\
        :param event_zeit:list[int] #Zeitstempel des Events.\
        :return:bool # Gibt True zurück, wenn der Event-Zeitstempel abgelaufen ist, sonst False.\
        """
        if event_zeit[0] <= self.system_zeit[0]: # Jahr
            if event_zeit[1] <= self.system_zeit[1]: # Monat
                if event_zeit[2] <= self.system_zeit[2]: # Tag
                    if event_zeit[3] <= self.system_zeit[3]: # Stunde
                        if event_zeit[4] <= self.system_zeit[4]: # Minute
                            if event_zeit[5] <= self.system_zeit[5]: # Sekunde
                                return True
        return False

    def event_trigger(self) -> list[list[str]] | None:
        """Geht durch die Event-Liste, prüft, ob Events abgelaufen sind und löst sie aus.\
        :return:str | None # Gibt die Aktion des ausgelösten Events zurück, wenn eines gefunden wurde, sonst None.\
        """
        aktionen_temp:list[str] = []
        for event in self.__event_liste:
            event_zeit:list[int] = self.__event_liste[event][0]
            event_akt:str = self.__event_liste[event][1]
            event_id = event
            if self.__event_abgelaufen(event_zeit):
                try:
                    print(f"Event-Backlog - Abgelaufene Events:\nID: '{event_id}'\nName: {event_akt}\nZeit: {event_zeit}.")
                    print("#Event wird später gelöscht, wenn es ausgelöst wurde.\n")
                    aktionen_temp.append(event_akt)
                except Exception as e:
                    print(f"Fehler beim Auslösen des Events: {str(e)}\n")
                    return None
        return set(aktionen_temp) if aktionen_temp else None

    def event_erstellen(self, event_zeit:list[int], event_akt: str, event_name: str) -> None:
        """Fügt ein Event der Liste hinzu und speichert es in der CSV-Datei.\
        :param event_zeit:list[int] #Zeitstempel des Events.\
        :param event_akt:str #Aktion, die mit dem Event verknüpft werden soll, aus vordefinierter Liste.\
        :param event_name:str #Name des Events zur Darstellung im UI.\
        :raises exception: Bei ungültiger Event-Zeit, Aktion oder Name.\
        """
        if not isinstance(event_zeit, list) or not all(isinstance(x, int) for x in event_zeit):
            raise Exception("Event-Zeit muss eine Liste von int sein.\n")
        if not isinstance(event_akt, str) or event_akt not in self.__event_aktionen:
            raise Exception("Ungültige Event-Aktion.\n")
        if not isinstance(event_name, str):
            raise Exception("Event-Name muss aus String bestehen.\n")
        if self.__event_liste:
            new_event_id = max(self.__event_liste.keys()) + 1  # Neue Event-ID basierend auf der höchsten vorhandenen ID
        else:
            new_event_id = 1  # Startet bei 1, wenn keine Events vorhanden sind
        self.__event_liste[new_event_id] = [event_zeit, event_akt, event_name]  # Fügt das neue Event der Liste hinzu
        print(f"Event '{event_name}' wurde erstellt mit ID '{new_event_id}'.\n")
        try:  # Speichert das neue Event in der CSV-Datei
            self.__events_speichern()
        except Exception as e:
            del self.__event_liste[new_event_id]
            raise Exception(f"Fehler beim Speichern des Events: {str(e)}\n")

    def event_aufrufen(self, event_id:int) -> list:
        """Methode zum Aufrufen eines Events anhand der Event-ID.\
        :param event_id:int # ID-Nummer des Events\
        :return:list[list[int], str, str] # Gibt das Event-Objekt zurück, wenn es existiert, sonst None.\
        :raises exception: Bei ungültiger Event-ID oder wenn das Event nicht gefunden wird.\
        """
        try:
            if event_id in self.__event_liste:
                return self.__event_liste[event_id]
            with open(self.EVENTS_CSV, 'r', encoding='utf-8') as f:
                csv_reader = reader(f)
                next(csv_reader)  # Überspringt die Header-Zeile
                for row in csv_reader:  # Durchsucht die CSV-Datei nach der Event-ID
                    if int(row[0]) == event_id:
                        return [row[1], row[2], row[3].strip()]  # Gibt das Event-Objekt zurück
            raise Exception(f"Es existiert kein Event mit der ID '{event_id}'.\n")
        except Exception as e:
            raise Exception(f"Event konnte nicht aufgerufen werden: {str(e)}\n")

    def event_entfernen(self, event_id: int) -> None:
        """Entfernt ein Event anhand der Event-ID aus der Event-Liste und CSV-Datei.\
        :param event_id:int # ID-Nummer des Events\
        :raises exception: bei ungültiger Event-ID oder wenn das Event nicht gefunden wird.\
        """
        if event_id not in self.__event_liste:
            raise Exception(f"Es existiert kein Event mit der ID '{event_id}'.\n")
        del self.__event_liste[event_id]
        print(f"Event mit ID {event_id} wurde entfernt.\n")
        try:
            self.__events_speichern()
        except Exception as e:
            raise Exception(f"Fehler beim speichern der Event-Liste: {str(e)}\n")


if __name__ == "__main__":
    """Testcode für die Eventman-Klasse."""
    EM: Eventman = Eventman()  # Beispiel-Event-Liste
    EM.event_erstellen(EM.system_zeit, "test", "Test-Event - Event erstellen")
    letztes_event_id = max(EM.event_liste.keys())
    letztes_event = EM.event_aufrufen(letztes_event_id)
    print(f"Event-Objekt aufgerufen mit Event-ID '{letztes_event_id}' :\n{letztes_event}\n")
    print(f"Eventzeit des Events:\n{letztes_event[0]}\n")
    print(f"Eventaktion des Events:\n{letztes_event[1]}\n")
    print(f"Eventname des Events:\n{letztes_event[2]}\n")
    print(f"Eventliste vor dem Entfernen eines Events:\n{EM.event_liste}\n")
    EM.event_entfernen(letztes_event_id)
    print(f"Eventliste nach dem Entfernen eines Events:\n{EM.event_liste}\n")

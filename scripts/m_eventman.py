"""
Eventman
————————————
-Event-Liste:list[Event] #Events im Format [int, Datumzeit, str, str, bool, bool, bool] gespeichert.
-Zeit:list[int] #Aktuelle Systemzeit.
-Event-Aktionen:list[str] #Liste der verfügbaren Event-Aktionen.
————————————
-init() → None
-events_laden() → None
-events_speichern() → None
-event_abgelaufen(event_zeit:list[int]) → bool
+trigger_event(entfernen:bool=True) → list[str]
+event_erstellen(event_zeit: Datumzeit, event_akt: str, event_name: str = "", taeglich: bool = False, monatlich: bool = False, jaehrlich: bool = False) → None
+event_aufrufen(event_id:int) → list[list[int], str, str, bool] | None
+event_entfernen(event_id:int) → None

"""
from scripts.m_datumzeit import Datumzeit
from scripts.m_event import Event
from csv import writer, reader
import ast


class Eventman:
    """Eventman-Klasse zur Verwaltung von Events.
    Diese Klasse ermöglicht das Erstellen, Aufrufen und Entfernen von Events.
    Die Events werden in einer CSV-Datei gespeichert und können über eine Event-ID verwaltet werden.
    Löst automatisch abgelaufene Events aus, wenn die Klasse instanziiert wird.
    ————————————Attribute: ————————————
        __zeit (Datumzeit): Aktuelle Systemzeit.
        __event_liste (list[Event]): Format von Event-Objekten kann in der Event-Klasse nachgelesen werden.
        __event_aktionen (list[str]): Liste der verfügbaren Event-Aktionen.
    ————————————Methoden: ————————————
        event_erstellen(event_zeit: Datumzeit, event_liste: list[Event], event_akt: str, event_name: str) → None: Fügt ein Event der Liste hinzu und speichert es in der CSV-Datei.
        event_aufrufen(event_id: int) → Event: Ruft ein Event anhand der Event-ID auf und gibt es zurück.
        event_entfernen(event_id: int) → None: Entfernt ein Event anhand der Event-ID aus der Event-Liste und CSV-Datei.
        trigger_event(entfernen=True) → list[str] | None: Überprüft, ob Events abgelaufen sind und löst sie aus. Gibt die Aktionen der ausgelösten Events zurück.
    """
    EVENTS_CSV = '../events.csv'  #Pfad zur CSV-Datei, in der die Events gespeichert werden

    def __init__(self) -> None:
        """Initialisiert die Eventman-Klasse und lädt die Events aus der CSV-Datei.
        Setzt die aktuelle Systemzeit und initialisiert die Event-Liste und verfügbaren Event-Aktionen.
        """
        self.__zeit:Datumzeit = Datumzeit()  # Aktuelle Systemzeit
        self.__zeit.jetzt()
        self.__event_liste: list[Event] = []
        self.__event_aktionen: list[str] = ["klingeln", "email", "sms", "anruf", "alarm", "test"]
        self.__events_laden()  # Lädt die Events aus der CSV-Datei
        self.event_trigger() # Überprüft, ob die Events bereits ausgelöst werden sollten

    @property
    def zeit(self) -> Datumzeit:
        """Gibt die aktuelle Systemzeit zurück.
        :return: # Aktuelle Systemzeit als Datumzeit-Objekt.
        """
        return self.__zeit

    @property
    def event_liste(self) -> list[Event]:
        """Gibt die Event-Liste zurück.
        :return: # Liste der Events als Event-Objekte.
        """
        return self.__event_liste

    @property
    def event_aktionen(self) -> list[str]:
        """Gibt die Liste der verfügbaren Event-Aktionen zurück.
        :return: #Liste der verfügbaren Event-Aktionen falls vorhanden, sonst eine leere Liste.
        """
        return self.__event_aktionen if self.__event_aktionen else []

    def __iter__(self) -> iter:
        """Ermöglicht die Iteration über die Event-Liste."""
        yield from self.__event_liste

    def __len__(self) -> int:
        """Gibt die Anzahl der Events in der Event-Liste zurück.
        :return: #Anzahl der Events als int.
        """
        return len(self.__event_liste)

    def __events_laden(self) -> None:
        """Lädt die Events aus der CSV-Datei in die Event-Liste.
        Erstellt die Datei, falls sie nicht existiert.
        :raises exception: Bei Fehlern beim Laden der Events aus der CSV-Datei.
        """
        try:
            with open(self.EVENTS_CSV, 'r', encoding='utf-8') as f:
                csv_reader = reader(f)
                next(csv_reader)
                for row in csv_reader:
                    if row:
                        try:
                            event_id = int(row[0])
                            zeitstempel = ast.literal_eval(row[1])  # Konvertiert den Zeitstempel in eine Liste
                            zeit_objekt = Datumzeit(zeitstempel[0], zeitstempel[1], zeitstempel[2], zeitstempel[3], zeitstempel[4], zeitstempel[5])
                            aktion = row[2]
                            name = row[3]
                            taeglich = ast.literal_eval(row[4])
                            monatlich = ast.literal_eval(row[5])
                            jaehrlich = ast.literal_eval(row[6])
                            self.event_erstellen(
                                event_zeit=zeit_objekt,
                                event_akt=aktion,
                                event_name=name,
                                taeglich=taeglich,
                                monatlich=monatlich,
                                jaehrlich=jaehrlich)
                        except Exception as e:
                            self.event_entfernen(event_id) #Fehlerhafte Events werden gelöscht
                            print(f"Fehler beim Laden des Events: {str(e)}\n")
        except FileNotFoundError:
            with open(self.EVENTS_CSV, 'w', newline='', encoding='utf-8') as f:
                csv_writer = writer(f)
                csv_writer.writerow(['EventID', 'Zeitstempel', 'Aktion', 'Name', 'Täglich ?', 'Monatlich ?', 'Jährlich ?'])

    def __events_speichern(self) -> None:
        """Speichert die aktuelle Event-Liste in der CSV-Datei.\
        """
        with open(self.EVENTS_CSV, 'w', newline='', encoding='utf-8') as f:
            csv_writer = writer(f)
            csv_writer.writerow(['EventID', 'Zeitstempel', 'Aktion', 'Name', 'Täglich ?', 'Monatlich ?', 'Jährlich ?'])
            for ev in self.__event_liste:
                csv_writer.writerow([ev.id, str(ev.zeit), ev.akt, ev.name, str(ev.taeglich), str(ev.monatlich), str(ev.jaehrlich)])

    def event_trigger(self, *args) -> list[str]:
        """Geht durch die Event-Liste, prüft, ob Events abgelaufen sind und löst sie aus.
        Entfernt das Event aus der Liste, wenn es nicht täglich, monatlich oder jährlich ist.
        Verschiebt das Event auf den nächsten Tag, Monat oder Jahr, wenn es täglich, monatlich oder jährlich ist.
        :param args: Wird hier gebraucht für die Timeout-Zeit von schedule_interval() in der App.
        :return: | None # Gibt die Aktion des ausgelösten Events als String zurück, wenn eines gefunden wurde, sonst None.
        """
        aktionen_temp:list[str] = []
        for ev in self.__event_liste:
            if ev.abgelaufen(self.__zeit):
                try:
                    print(f"Event-Backlog - Abgelaufene Events:\nID: '{ev.id}'\nName: {ev.akt}\nZeit: {ev.zeit}\n")
                    aktionen_temp.append(ev.akt)
                    # Verschiebt das Event auf den nächsten Tag, Monat oder Jahr, wenn es täglich, monatlich oder jährlich ist.
                    if ev.taeglich or ev.monatlich or ev.jaehrlich:
                        neue_zeit = Datumzeit()
                        neue_zeit.jahr = ev.zeit[0]
                        neue_zeit.monat = ev.zeit[1]
                        neue_zeit.tag = ev.zeit[2]
                        neue_zeit.stunde = ev.zeit[3]
                        neue_zeit.minute = ev.zeit[4]
                        neue_zeit.sekunde = ev.zeit[5]
                        if ev.jaehrlich:
                            neue_zeit.jahr += 1
                        elif ev.monatlich:
                            neue_zeit.monat += 1
                            if neue_zeit.monat > 12:
                                neue_zeit.monat = 1
                                neue_zeit.jahr += 1
                        elif ev.taeglich:
                            neue_zeit.tag += 1
                        ev.zeit = neue_zeit
                    self.event_entfernen(ev.id) if not ev.taeglich and not ev.monatlich and not ev.jaehrlich else None
                    self.__events_speichern()
                except Exception as e:
                    raise Exception(f"Fehler beim Triggern des Events: {str(e)}\n")
        return set(aktionen_temp) if aktionen_temp else []

    def event_erstellen(
            self,
            event_zeit:Datumzeit,
            event_akt: str,
            event_name: str,
            taeglich:bool = False,
            monatlich:bool = False,
            jaehrlich:bool = False,) -> None:
        """Fügt ein Event der Liste hinzu und speichert es in der CSV-Datei.
        :param event_zeit:list[int] #Zeitstempel des Events.
        :param event_akt:str #Aktion, die mit dem Event verknüpft werden soll, aus vordefinierter Liste.
        :param event_name:str #Name des Events zur Darstellung im UI.
        :param taeglich:bool #bei True wird das Event auf den Nächsten Tag verschoben, wenn es getriggert wird. Default False.
        :param monatlich:bool #bei True wird das Event auf den Nächsten Monat verschoben, wenn es getriggert wird. Default False.
        :param jaehrlich:bool #bei True wird das Event auf das Nächste Jahr verschoben, wenn es getriggert wird. Default False.
        :raises exception: Bei ungültiger Event-Zeit, Aktion oder Name.
        """
        if not isinstance(event_zeit, Datumzeit):
            raise TypeError("Event-Zeit muss ein Datumzeit-Objekt sein.\n")
        if not isinstance(event_akt, str) or event_akt not in self.__event_aktionen:
            raise TypeError(f"Ungültige Event-Aktion.\nGültige Aktionen: {self.__event_aktionen}\n")
        if not isinstance(event_name, str):
            raise TypeError("Event-Name muss ein String sein.\n")
        neues_event:Event = Event(
                event_zeit=event_zeit,
                event_liste=self.__event_liste,
                event_akt=event_akt,
                event_name=event_name,
                taeglich=taeglich,
                monatlich=monatlich,
                jaehrlich=jaehrlich)
        self.__event_liste.append(neues_event)
        print(f"Event '{neues_event.name}' wurde erstellt mit ID '{neues_event.id}'.\n")
        try:  # Speichert das neue Event in der CSV-Datei
            self.__events_speichern()
        except Exception as e:
            for ev in self.__event_liste:
                if ev.id == neues_event.id:
                    self.__event_liste.remove(ev)
            raise Exception(f"Fehler beim Speichern des Events: {str(e)}\n")

    def event_aufrufen(self, event_id:int) -> Event:
        """Methode zum Aufrufen eines Events anhand der Event-ID.
        :param event_id:int # ID-Nummer des Events
        :return: Gibt das Event-Objekt zurück, wenn es existiert, sonst None.
        :raises exception: Bei ungültiger Event-ID oder wenn das Event nicht gefunden wird.
        """
        try:
            for ev in self.__event_liste:
                if ev.id == event_id:
                    return ev
            raise ValueError(f"Es existiert kein Event mit der ID '{event_id}'.\n")
        except Exception as e:
            raise Exception(f"Event konnte nicht aufgerufen werden: {str(e)}\n")

    def event_entfernen(self, event_id: int) -> None:
        """Entfernt ein Event anhand der Event-ID aus der Event-Liste und CSV-Datei.
        :param event_id:int # ID-Nummer des Events
        :raises exception: bei ungültiger Event-ID oder wenn das Event nicht gefunden wird.
        """
        for ev in self.__event_liste:
            if ev.id == event_id:
                self.__event_liste.remove(ev)
                print(f"Event mit ID {ev.id} wurde entfernt.\n")
        try:
            self.__events_speichern()
        except Exception as e:
            raise Exception(f"Fehler beim speichern der Event-Liste: {str(e)}\n")



if __name__ == "__main__":
    """Testcode für die Eventman-Klasse."""
    EM: Eventman = Eventman()
    EM.event_erstellen(EM.zeit, "test", "Test-Event")
    letztes_event_id = EM.event_liste[-1].id
    letztes_event = EM.event_aufrufen(letztes_event_id)
    print(f"Event-Objekt aufgerufen mit Event-ID '{letztes_event_id}' :\n{letztes_event}\n")
    print(f"Eventliste vor dem Entfernen eines Events:\n")
    for event in EM:
        print(f"{event}\n")
    print("Events werden getriggert.\n");EM.event_trigger()
    print(f"Eventliste nach dem Entfernen eines Events:\n")
    for event in EM:
        print(f"{event}\n")

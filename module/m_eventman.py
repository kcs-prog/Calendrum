"""
Eventman
————————————
#Event-Liste:dict{EventID:Event} #noch im code integriert, wird später lokal von einer Datei geholt wenn vorhanden.
#System-Zeit:dict{str:int}
#Event-Aktionen:list[str] #Liste der verfügbaren Event-Aktionen.
————————————
-init() -> None
#load_events() -> None
#save_events() -> None
+event_erstellen(event_zeit: dict[str:int], event_akt: str, event_name: str = "") -> None
+event_aufrufen(event_id: int) -> Any | None
+event_entfernen(event_id: int) -> None
+()

"""
import ast
from time import localtime
from typing import Any
from csv import writer, reader

class Eventman:
    """Eventman-Klasse zur Verwaltung von Events.
    Diese Klasse ermöglicht das Erstellen, Aufrufen und Entfernen von Events.
    Die Events werden in einer CSV-Datei gespeichert und können über eine Event-ID verwaltet werden.
    """
    def __init__(self) -> None:
        """Initialisiert die Eventman-Klasse und lädt die Events aus der CSV-Datei."""
        self._system_zeit = localtime() # Aktuelle Systemzeit
        self._event_liste: dict[int: list[dict[str, int]], str, str] = {} # Event-Liste im Format {EventID:int: list[dict{Zeitstempel:str:int}, Event-Aktion: str, Event-Name: str]}
        self._event_aktionen: list[str] = ["klingeln", "erinnern", "email", "sms", "anruf", "alarm", "benachrichtigen","test"] # Liste der verfügbaren Event-Aktionen
        self._load_events() # Lädt die Events aus der CSV-Datei

    def _load_events(self) -> None:
        """Lädt die Events aus der CSV-Datei in die Event-Liste.
        :raises exception: Bei Fehlern beim Lesen der CSV-Datei oder wenn die Datei nicht gefunden wird."""
        try:# Versucht, die Events aus der CSV-Datei zu laden
            with open('events.csv', 'r', encoding='utf-8') as f:
                csv_reader = reader(f)
                next(csv_reader)
                self._event_liste = {# Erstellt ein Dictionary aus der CSV-Datei
                    int(row[0]): [ast.literal_eval(row[1]), row[2], row[3].strip()]
                    for row in csv_reader if row
                }
        except FileNotFoundError:# Wenn die Datei nicht existiert, wird eine leere Event-Liste erstellt
            with open('events.csv', 'w', newline='', encoding='utf-8') as f:
                csv_writer = writer(f)
                csv_writer.writerow(['EventID', 'Zeitstempel', 'Aktion', 'Name'])

    def _events_speichern(self) -> None:
        """Speichert die aktuelle Event-Liste in der CSV-Datei.
        :raises exception: Bei Fehlern beim Schreiben der CSV-Datei."""
        with open('events.csv', 'w', newline='', encoding='utf-8') as f:
            csv_writer = writer(f)
            csv_writer.writerow(['EventID', 'Zeitstempel', 'Aktion', 'Name'])
            for event_id, event_data in self._event_liste.items():
                csv_writer.writerow([event_id, event_data[0], event_data[1], event_data[2]])

    @property
    def system_zeit(self) -> dict[str:int]:
        """Gibt die aktuelle Systemzeit zurück.
        :return:dict[str: int] #Aktuelle Systemzeit im Format {Jahr, Monat, Tag, Stunde, Minute, Sekunde}
        """
        return {
            "J":self._system_zeit.tm_year,
            "M":self._system_zeit.tm_mon,
            "T":self._system_zeit.tm_mday,
            "h":self._system_zeit.tm_hour,
            "m":self._system_zeit.tm_min,
            "s":self._system_zeit.tm_sec
        }

    @property
    def event_liste(self) -> dict[int:list[dict[str,int]],str,str]:
        """Gibt die Event-Liste zurück.
        :return:dict[int: list[dict[str: int]], str, str] #Event-Liste aus CSV im Format {EventID:int: list[dict{Zeitstempel:str:int}, Event-Aktion: str, Event-Name: str]}
        :raises exception: Bei leerer Event-Liste oder Fehler beim Lesen der CSV-Datei.
        """
        try:
            if not self._event_liste:
                with open('events.csv', 'r', encoding='utf-8') as f:
                    import ast
                    lines = f.readlines()
                    self._event_liste = {int(line.split(',')[0]):
                        [ast.literal_eval(line.split(',')[1]),
                         line.split(',')[2],
                         line.split(',')[3].strip()]
                        for line in lines[1:]}  # Skip header
            return self._event_liste
        except FileNotFoundError:
            return {}
        except Exception as e:
            raise Exception(f"Fehler beim Lesen der Event-Liste: {str(e)}\n")

    @event_liste.setter
    def event_liste(self, new_event_liste:dict[int:list[dict[str,int]],str,str]) -> None:
        """Setzt eine neue Event-Liste und speichert sie in CSV.
        :param new_event_liste:dict[int:list[dict[str:int]],str,str] #Neue Event-Liste im Format {EventID:int: list[dict{Zeitstempel:str:int}, Event-Aktion: str , Event-Name: str]}
        :raises exception: Bei falschem Typ der neuen Event-Liste oder Fehler beim Schreiben der CSV-Datei.
        """
        if type(new_event_liste) != dict:
            raise Exception("Neue Event-Liste muss vom Typ 'dict' sein.\n")
        self._event_liste = new_event_liste
        try:
            with open('events.csv', 'r', encoding='utf-8') as f:
                csv_reader = reader(f)
                next(csv_reader)  # Skip header
                self._event_liste = {
                    int(row[0]): [ast.literal_eval(row[1]), row[2], row[3].strip()]
                    for row in csv_reader if row
                }
        except Exception as e:
            raise Exception(f"Fehler beim Speichern der Event-Liste: {str(e)}\n")

    @property
    def event_aktionen(self) -> list[str]:
        """Gibt die Liste der verfügbaren Event-Aktionen zurück.
        :return:list[str] #Liste der verfügbaren Event-Aktionen.
        :raises exception: Bei leerer Event-Aktionsliste.
        """
        if not self._event_aktionen:
            raise Exception("Event-Aktionsliste ist leer.\n")
        return self._event_aktionen

    @event_aktionen.setter
    def event_aktionen(self, new_event_aktionen:list[str]) -> None:
        """Setzt eine neue Liste von Event-Aktionen.
        :param new_event_aktionen:list[str] #Neue Liste der verfügbaren Event-Aktionen.
        :raises exception: Bei falschem Typ der neuen Event-Aktionsliste.
        """
        if type(new_event_aktionen) != list:
            raise Exception("Neue Event-Aktionsliste muss vom Typ 'list' sein.\nElemente der Liste müssen vom Typ 'str' sein.\n")
        self._event_aktionen = new_event_aktionen

    @staticmethod
    def __chk_event_zeit(event_zeit: dict[str:int]) -> bool:
        """Überprüft die angegebene Event-Zeit auf das richtige Format für die Event-Manager-Methoden.
        :param event_zeit:dict[str: int] #Datumzeit-Format.
        :return:bool #True, wenn das Format korrekt ist, sonst False.
        :raises exception: Bei unvollständigem oder falschem Format der Event-Zeit.
        """
        for k in event_zeit.keys():
            if k not in ["J","M","T","h","m","s"]:
                raise Exception("Datum und Uhrzeit des Events unvollständig.\n")
        for v in event_zeit.values():
            if type(v) != int:
                raise Exception("Falsches Zeichen für Zeit-Format.\nNur ganze Nummern.\n")
        return True

    def event_erstellen(self, event_zeit: dict[str:int], event_akt: str, event_name: str = "") -> None:
        """Fügt ein Event der Liste hinzu und speichert es in der CSV-Datei.
        :param event_zeit:dict[str: int] #Datumzeit-Format.
        :param event_akt:str #Aktion, die mit dem Event verknüpft werden soll, aus vordefinierter Liste.
        :param event_name:str #Name des Events zur Darstellung im UI.
        :raises exception: Wenn die Event-Zeit im falschen Format ist, die Event-Aktion ungültig ist oder der Event-Name ungültige Zeichen enthält.
        """
        if not self.__chk_event_zeit(event_zeit):
            raise Exception("Zeiten für das Event sind im falschen Format.\n")
        if type(event_akt) != str or event_akt not in self._event_aktionen:
            raise Exception("Ungültige Event-Aktion.\n")
        if type(event_name) != str:
            raise Exception("Ungültige Zeichen für Event-Namen\n")
        if self._event_liste:
            new_event_id = max(self._event_liste.keys()) + 1
        else:
            new_event_id = 1
        self._event_liste[new_event_id] = [event_zeit, event_akt, event_name]
        try:
            with open('events.csv', 'a', newline='', encoding='utf-8') as f:
                csv_writer = writer(f)
                csv_writer.writerow([new_event_id, event_zeit, event_akt, event_name])
        except Exception as e:
            del self._event_liste[new_event_id]
            raise Exception(f"Fehler beim Speichern des Events: {str(e)}\n")

    def event_aufrufen(self, event_id: int) -> Any | None:
        """Methode zum Aufrufen eines Events anhand der Event-ID.
        :param event_id:int # ID-Nummer des Events
        :return:Any | None # Gibt das Event-Objekt zurück, wenn es existiert, sonst None.
        :raises exception: Bei ungültiger Event-ID oder wenn das Event nicht gefunden wird.
        """
        try:
            if event_id in self._event_liste:
                return self._event_liste[event_id]
            # Wenn nicht im Cache, dann aus CSV laden
            with open('events.csv', 'r', encoding='utf-8') as f:
                import ast
                lines = f.readlines()[1:]  # Skip header
                for line in lines:
                    current_id = int(line.split(',')[0])
                    if current_id == event_id:
                        return [ast.literal_eval(line.split(',')[1]),
                                line.split(',')[2],
                                line.split(',')[3].strip()]
            raise Exception("Es existiert kein Event mit dieser ID.\n")
        except Exception as e:
            raise Exception(f"Event konnte nicht aufgerufen werden: {str(e)}\n")

    def event_entfernen(self, event_id: int) -> None:
        """Entfernt ein Event anhand der Event-ID aus der Event-Liste und CSV-Datei.
        :param event_id:int # ID-Nummer des Events
        :raises exception: bei ungültiger Event-ID oder wenn das Event nicht gefunden wird.
        """
        if event_id not in self._event_liste:
            raise Exception("Es existiert kein Event mit dieser ID.\n")
        # Event aus dem Cache entfernen
        del self._event_liste[event_id]
        try:
            # CSV neu schreiben ohne das gelöschte Event
            with open('events.csv', 'w', newline='', encoding='utf-8') as f:
                csv_writer = writer(f)
                csv_writer.writerow(['EventID', 'Zeitstempel', 'Aktion', 'Name'])
                for event_id, event_data in self._event_liste.items():
                    csv_writer.writerow([event_id, event_data[0], event_data[1], event_data[2]])
        except Exception as e:
            raise Exception(f"Fehler beim Entfernen des Events aus der CSV: {str(e)}\n")

if __name__ == "__main__":
    """Testcode für die Eventman-Klasse"""
    EM:Eventman = Eventman() # Beispiel-Event-Liste
    EM.event_erstellen(EM.system_zeit,"klingeln","Test-Event Event erstellen") # debug
    for key in EM.event_liste.keys():
        print(f"EventID:{key}\n") # ID des beispielevents
    for value in EM.event_liste.values(): #values sind die events
        print(f"Eventzeit:{value[0]}\n") #zeitstempel des beispielevents
        print(f"Aktion:{value[1]}\n") #aktion des beispielevents
        print(f"Name:{value[2]}\n") #name des beispielevents
    print(f"Event-Objekt aufgerufen mit Event-ID '0':\n{EM.event_aufrufen(3),f"\n"}\n") # event anhand einer ID aufrufen
    print(f"Eventliste vor dem Entfernen eines Events:\n{EM.event_liste}")
    EM.event_entfernen(3) # event anhand einer ID entfernen
    print(f"Eventliste nach dem Entfernen eines Events:\n{EM.event_liste}")
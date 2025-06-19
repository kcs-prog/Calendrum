"""
Eventman
————————————
#Event-Liste:dict{EventID:Event} #noch im code integriert, wird später lokal von einer Datei geholt wenn vorhanden.
#System-Zeit:dict{str:int}
#Event-Aktionen:list[str] #Liste der verfügbaren Event-Aktionen.
————————————
-init() -> None
+event_erstellen(event_zeit:dict{str:int}, event_aktion:str, event_name:str) -> None
+event_aufrufen(event_id:int) -> list[dict[str:int],str,str] -> ('Any' laut IDE) | None
+event_entfernen(event_id:int) -> None
+()

"""
from typing import Any
from time import localtime
from logging import exception

class Eventman:
    """Event-Manager-Klasse der Calendrum-App.
    Verwaltet Events (erstellen, löschen, bearbeiten, anzeigen).
    Events sind dict-type-Objekte im Format:\n
    {EventID:int: list[dict{Zeitstempel:str:int}, Event-Aktion: str , Event-Name: str]} \n
    """
    def __init__(self) -> None:
        self._system_zeit = localtime() # Echtzeit zum Abgleich mit Event-Zeiten
        #print(self._system_zeit) # debug
        self._event_liste:dict[int:list[dict[str,int]],str,str] = {} # platzhalter, event-liste muss ausgelagert werden.
        self._event_aktionen:list[str] = ["klingeln","erinnern","email","sms"] # für die Prüfung und ausführung von Klassenspezifischen Methoden
        #print(len(self.event_liste)) # debug

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
        :return:dict[int:list[dict[str:int]],str,str] #Event-Liste im Format {EventID:int: list[dict{Zeitstempel:str:int}, Event-Aktion: str , Event-Name: str]}
        """
        return self._event_liste

    @event_liste.setter
    def event_liste(self, new_event_liste:dict[int:list[dict[str,int]],str,str]) -> None:
        """Setzt eine neue Event-Liste.
        :param new_event_liste:dict[int:list[dict[str:int]],str,str] #Neue Event-Liste im Format {EventID:int: list[dict{Zeitstempel:str:int}, Event-Aktion: str , Event-Name: str]}
        """
        if type(new_event_liste) != dict:
            raise exception("Neue Event-Liste muss vom Typ 'dict' sein.\n")
        self._event_liste = new_event_liste

    @property
    def event_aktionen(self) -> list[str]:
        """Gibt die Liste der verfügbaren Event-Aktionen zurück.
        :return:list[str] #Liste der verfügbaren Event-Aktionen.
        """
        return self._event_aktionen

    @event_aktionen.setter
    def event_aktionen(self, new_event_aktionen:list[str]) -> None:
        """Setzt eine neue Liste von Event-Aktionen.
        :param new_event_aktionen:list[str] #Neue Liste der verfügbaren Event-Aktionen.
        """
        if type(new_event_aktionen) != list:
            raise exception("Neue Event-Aktionsliste muss vom Typ 'list' sein.\nElemente der Liste müssen vom Typ 'str' sein.\n")
        self._event_aktionen = new_event_aktionen

    @staticmethod
    def __chk_event_zeit(event_zeit: dict[str:int]) -> bool:
        """Überprüft die angegebene Event-Zeit auf das richtige Format für die Event-Manager-Methoden.
        :param event_zeit:dict[str: int] #Datumzeit-Format.
        """
        for k in event_zeit.keys():
            if k not in ["J","M","T","h","m","s"]:
                raise exception("Datum und Uhrzeit des Events unvollständig.\n")
        for v in event_zeit.values():
            if type(v) != int:
                raise exception("Falsches Zeichen für Zeit-Format.\nNur ganze Nummern.\n")
        return True

    def event_erstellen(self,event_zeit:dict[str:int],event_akt:str,event_name:str="") -> None:
        """Fügt ein Event der Liste hinzu. benötigt eine event-zeit (vorher festgelegt),
        eine event-aktion (aus einer vorgegebenen Liste), und einen event-namen.
        Dem Event wird eine ID zugeteilt und es wird in der 'Eventman.event_liste' gespeichert.
        Event-Liste ist zurzeit in der Klasse also gespeichert, muss später lokal in einer Datei gespeichert werden.
        :param event_zeit:dict[str: int] #Datumzeit-Format.
        :param event_akt:str #Aktion, die mit dem Event verknüpft werden soll, aus vordefinierter Liste.
        :param event_name:str #Name des Events zur Darstellung im UI.
        :raises exception: Wenn die Event-Zeit im falschen Format ist, die Event-Aktion ungültig ist oder der Event-Name ungültige Zeichen enthält.
        """
        if not self.__chk_event_zeit(event_zeit):
            raise exception("Zeiten für das Event sind im falschen Format.\n")
        if type(event_akt) != str or event_akt not in self._event_aktionen:
            raise exception("Ungültige Event-Aktion.\n")
        if type(event_name) != str:
            raise exception("Ungültige Zeichen für Event-Namen\n")
        self.event_liste.update({len(self.event_liste):[[event_zeit],event_akt,event_name]})
        #print(event_zeit) #debug

    def event_aufrufen(self, event_id:int) -> Any | None:
        """Methode zum Aufrufen eines Events anhand der Event-ID.
        :param event_id:int # ID-Nummer des Events
        :return:Any | None # Gibt das Event-Objekt zurück, wenn es existiert, sonst None.
        :raises exception: Wenn die Event-ID nicht existiert.
        """
        event_keys = self.event_liste.keys()
        #print(event_keys) #debug
        if event_id not in event_keys:
            raise exception("Es existiert kein Event mit dieser ID.\n")
        for k in event_keys:
            if k == event_id:
                return self.event_liste[k]
        raise exception("Event konnte nicht aufgerufen werden.\n")

    def event_entfernen(self, event_id:int) -> None:
        """Entfernt ein Event anhand der Event-ID aus der Event-Liste.
        :param event_id:int # ID-Nummer des Events
        """
        event_keys = self.event_liste.keys()
        if event_id not in event_keys:
            raise exception("Es existiert kein Event mit dieser ID.\n")
        for k in event_keys:
            if k == event_id:
                del self.event_liste[k]
                return None
        raise exception("Event konnte nicht entfernt werden.\n")

if __name__ == "__main__":
    """Testcode für die Eventman-Klasse"""
    EM:Eventman = Eventman()
    EM.event_erstellen(EM.system_zeit,"klingeln","test event erstellt") # debug
    for key in EM.event_liste.keys():
        print(f"EventID:{key}\n") # ID des beispielevents
    for value in EM.event_liste.values():
        print(f"Eventzeit:{value[0]}\n") #zeitstempel des beispielevents
        print(f"Aktion:{value[1]}\n") #aktion des beispielevents
        print(f"Name:{value[2]}\n") #name des beispielevents
    print(f"Event-Objekt aufgerufen mit Event-ID '0':\n{EM.event_aufrufen(0)}\n") # event anhand einer ID aufrufen
    print(f"Eventliste vor dem Entfernen eines Events:\n{EM.event_liste}")
    EM.event_entfernen(0) # event anhand einer ID entfernen
    print(f"Eventliste nach dem Entfernen eines Events:\n{EM.event_liste}")
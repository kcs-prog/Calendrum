"""
Eventman
————————————
+Event-Liste:dict{EventID:Event} #noch im code integriert, wird später lokal von einer Datei geholt wenn vorhanden.
#EventID:int
#Event:list[Zeitstempel,Event-Aktion,Event-Name]
#Zeitstempel:dict{str:int}
#Event-Aktion:str
#Event-Name:str
————————————
-init() -> None
+event_erstellen(event_zeit:dict{str:int}, event_aktion:str, event_name:str) -> None
+event_aufrufen(event_id:int) -> list[list[dict[str:int],str,str]] -> ('Any' laut IDE) | None
+()
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
        self.zeit_stempel:dict[str:int] = { # platzhalter dict für das Event-Zeit-Format
            "J":self._system_zeit.tm_year,
            "M":self._system_zeit.tm_mon,
            "T":self._system_zeit.tm_mday,
            "h":self._system_zeit.tm_hour,
            "m":self._system_zeit.tm_min,
            "s":self._system_zeit.tm_sec
        }
        self.event_liste:dict[int:list[dict[str,int]],str,str] = {} # platzhalter, event-liste muss ausgelagert werden.
        self._action_liste:list[str] = ["klingeln","erinnern","email","sms"] # für die Prüfung und ausführung von Klassenspezifischen Methoden
        #print(len(self.event_liste)) # debug

    def event_erstellen(self,event_zeit:dict[str:int],event_akt:str,event_name:str="") -> None:
        """Fügt ein Event der Liste hinzu. benötigt eine event-zeit (vorher festgelegt),
        eine event-aktion (aus einer vorgegebenen Liste), und einen event-namen.
        Dem Event wird eine ID zugeteilt und es wird in der 'Eventman.event_liste' gespeichert.
        Event-Liste ist zurzeit in der Klasse also gespeichert, muss später lokal in einer Datei gespeichert werden.
        :param event_zeit:dict[str:int] #Datumzeit-Format.
        :param event_akt:str #Aktion, die mit dem Event verknüpft werden soll, aus vordefinierter Liste.
        :param event_name:str #Name des Events zur Darstellung im UI.
        """
        if not self.__chk_event_zeit(event_zeit):
            raise exception("Zeiten für das Event sind im falschen Format.\n")
        if type(event_akt) != str or event_akt not in self._action_liste:
            raise exception("Ungültige Event-Aktion.\n")
        if type(event_name) != str:
            raise exception("Ungültige Zeichen für Event-Namen\n")
        self.event_liste.update({len(self.event_liste):[[event_zeit],event_akt,event_name]})
        #print(event_zeit) #debug

    def event_aufrufen(self, event_id:int) -> Any | None:
        """Methode zum Aufrufen eines Events anhand der Event-ID.
        Gibt Events im Format zurück:\n
        list[list[dict[str:int],str,str]] (IDE erkennt es als 'Any' an)\n
        return None, wenn keine Events in der Liste sind.
        :param event_id:int # ID-Nummer des Events
        """
        event_keys = self.event_liste.keys()
        #print(event_keys) #debug
        if event_id not in event_keys:
            raise exception("Es existiert kein Event mit dieser ID.\n")
        for k in event_keys:
            if k == event_id:
                return self.event_liste[k]
        return None

    def __chk_event_zeit(self,event_zeit:dict[str:int]) -> bool:
        """Überprüft die angegebene Event-Zeit auf das richtige Format für die Event-Manager-Methoden.
        :param event_zeit:dict[str:int] #Datumzeit-Format.
        """
        for k in event_zeit.keys():
            if k not in ["J","M","T","h","m","s"]:
                raise exception("Datum und Uhrzeit des Events unvollständig.\n")
        for v in event_zeit.values():
            if type(v) != int:
                raise exception("Falsches Zeichen für Zeit-Format.\nNur ganze Nummern.\n")
        return True


if __name__ == "__main__":
    EM:Eventman = Eventman()
    EM.event_erstellen(EM.zeit_stempel,"klingeln","test event erstellt") # debug
    for key in EM.event_liste.keys():
        print(f"EventID:{key}\n") # ID des beispielevents
    for value in EM.event_liste.values():
        print(f"Eventzeit:{value[0]}\n") #zeitstempel des beispielevents
        print(f"Aktion:{value[1]}\n") #aktion des beispielevents
        print(f"Name:{value[2]}\n") #name des beispielevents
    print(f"Event-Objekt aufgerufen mit Event-ID '0':\n{EM.event_aufrufen(0)}\n") # event anhand einer ID aufrufen
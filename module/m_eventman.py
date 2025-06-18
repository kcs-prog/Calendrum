"""
Event_Manager
————————————
+Event-Liste:dict{EventID:Event} #noch im code integriert, wird später lokal von einer Datei geholt wenn vorhanden.
-EventID:int
-Event:list[Zeitstempel,Event-Aktion,Event-Name]
-Zeitstempel:dict{str:int}
-Event-Aktion:str
-Event-Name:str
————————————
#init()
+event_erstellen(event_zeit:dict{str:int}, event_aktion:str, event_name:str)
+()
+()
+()

"""
from m_datumzeit import Datumzeit
from time import localtime
from logging import exception

class Event_Manager:
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
        Dem Event wird eine ID zugeteilt und es wird in der 'Event_Manager.event_liste' gespeichert.
        Event-Liste ist zurzeit in der Klasse also gespeichert, muss später lokal in einer Datei gespeichert werden."""
        if not self.__chk_event_zeit(event_zeit):
            raise exception("Zeiten für das Event sind im falschen Format.\n")
        if type(event_akt) != str or event_akt not in self._action_liste:
            raise exception("Ungültige Event-Aktion.\n")
        if type(event_name) != str:
            raise exception("Ungültige Zeichen für Event-Namen\n")
        self.event_liste.update({len(self.event_liste):[[event_zeit],event_akt,event_name]})
        #print(event_zeit) #debug

    def __chk_event_zeit(self,event_zeit:dict[str:int]) -> bool:
        """Überprüft die angegebene Event-Zeit auf das richtige Format für die Event-Manager-Methoden."""
        for key in event_zeit.keys():
            if key not in ["J","M","T","h","m","s"]:
                raise exception("Datum und Uhrzeit des Events unvollständig.\n")
        for value in event_zeit.values():
            if type(value) != int:
                raise exception("Falsches Zeichen für Zeit-Format.\nNur ganze Nummern.\n")
        return True


if __name__ == "__main__":
    EM:Event_Manager = Event_Manager()
    EM.event_erstellen(EM.zeit_stempel,"klingeln","test1") # debug
    for key in EM.event_liste.keys():
        print(f"EventID:{key}\n") # ID des beispielevents
    for value in EM.event_liste.values():
        print(f"Eventzeit:{value[0]}\n") #zeitstempel des beispielevents
        print(f"Aktion:{value[1]}\n") #aktion des beispielevents
        print(f"Name:{value[2]}\n") #name des beispielevents
from m_datumzeit import Datumzeit
from time import localtime
from logging import exception

class Event_Manager:
    """Event-Manager-Klasse der Calendrum-App"""
    def __init__(self) -> None:
        self._system_zeit = localtime() # Echtzeit zum Abgleich mit Event-Zeiten
        #print(self._system_zeit) # debug
        self.system_zeit:dict[str:int] = {
            "J":self._system_zeit.tm_year,
            "M":self._system_zeit.tm_mon,
            "T":self._system_zeit.tm_mday,
            "h":self._system_zeit.tm_hour,
            "m":self._system_zeit.tm_min,
            "s":self._system_zeit.tm_sec
        }
        self._event_liste:dict[int:list[list[int]],str,str] = {} # platzhalter, event-liste muss ausgelagert werden.
        #print(len(self._event_liste)) # debug

    def event_erstellen(self,event_zeit:dict[str:int],event_akt:str,event_name:str="") -> None:
        """Fügt ein Event der Liste hinzu. benötigt eine event-zeit (vorher festgelegt),
        eine event-aktion (aus einer vorgegebenen Liste), und einen event-namen.
        Dem Event wird eine ID zugeteilt und es wird in der 'Event_Manager._event_liste' gespeichert."""
        if not self.__chk_event_zeit(event_zeit):
            raise exception("Zeiten für das Event sind im falschen Format.\n")
        if type(event_akt) != str or event_akt not in ["klingeln","erinnern","email","sms"]:
            raise exception("Ungültige Event-Aktion.\n")
        if type(event_name) != str:
            raise exception("Ungültige Zeichen für Event-Namen\n")
        self._event_liste.update({len(self._event_liste):[[event_zeit],event_akt,event_name]})
        print(type(event_zeit), event_zeit)

    def event_erstellen(self,zeit:list[int],aktion:str) -> None:
        pass

    def __chk_event(self, event):
        if type(event) != list[list[int]]|str:
            raise exception("Format der Eventzeit ist falsch.\n Format: [[J,M,T,h,m,s],'aktion'")


if __name__ == "__main__":
    EM = Event_Manager()
    print(Event_Manager.get_event_liste(EM))
    print(len(EM.event_liste))
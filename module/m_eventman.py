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

    def get_event_liste(self) -> list[list[int]|str] or None:
        for event in self.event_liste:
            return self.event_liste[event] if self.__chk_event(event) else None
        return None

    def event_erstellen(self,zeit:list[int],aktion:str) -> None:
        pass

    def __chk_event(self, event):
        if type(event) != list[list[int]]|str:
            raise exception("Format der Eventzeit ist falsch.\n Format: [[J,M,T,h,m,s],'aktion'")


if __name__ == "__main__":
    EM = Event_Manager()
    print(Event_Manager.get_event_liste(EM))
    print(len(EM.event_liste))
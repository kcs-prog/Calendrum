from m_datumzeit import Datumzeit
from time import localtime
from logging import exception

class Event_Manager:
    """Event-Manager-Klasse der Calendrum-App"""
    def __init__(self) -> None:
        self.event_liste:dict[int : list[list[int]],str,str] = {
            #beispiel event der event_liste:
        # ID: [ [Datumzeit]  , event-Name, event-aktion]
            0:[[2025,6,18,13,20,30], "Alarm", "klingeln"]
        }

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
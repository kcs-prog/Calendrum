from itertools import count

from m_datumzeit import Datumzeit
from logging import exception

Datumzeit(2025,6,18,13,20,30)

class Event_Manager:
    def __init__(self) -> None:#id      dz   akt
        self.event_liste:dict[int:list[list],str] = {
            0:[[2025,6,18,13,20,30],"aktion"] # beispielevent in der event liste
        }

    def get_event_liste(self) -> list[list[int]|str] or None:
        for event in self.event_liste:
            return self.event_liste[event] if self.__chk_event(event) else None
        return None


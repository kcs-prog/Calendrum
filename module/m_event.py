from m_datumzeit import Datumzeit

class Event:
    def __init__(
            self,
            event_id :int,
            event_zeit :Datumzeit,
            event_akt :str = "",
            event_name :str = "",
            dauer_in_stunden :int = 0,
            taeglich :bool = False,
            monatlich :bool = False,
            jaehrlich :bool = False ,):
        self.__id = event_id
        self.__zeit = event_zeit
        self.__akt = event_akt
        self.__name = event_name
        self.__dauer = dauer_in_stunden
        self.__taeglich = taeglich
        self.__monatlich = monatlich
        self.__jaehrlich = jaehrlich

    @property
    def id(self) -> int:
        return self.__id
    @id.setter
    def id(self, neue_id:int):
        if not isinstance(neue_id, int):
            raise TypeError("neue_id must be an instance of integer")

    @property
    def zeit(self) -> list[int]:
        return [self.__zeit.jahr,
                self.__zeit.monat,
                self.__zeit.tag,
                self.__zeit.stunde,
                self.__zeit.minute,
                self.__zeit.sekunde]
    @zeit.setter
    def zeit(self, neue_event_zeit :Datumzeit):
        if not isinstance(neue_event_zeit, Datumzeit):
            raise TypeError("neue_event_zeit must be an instance of Datumzeit")
        else:
            self.__zeit = neue_event_zeit

    @property
    def akt(self) -> str:
        return self.__akt
    @akt.setter
    def akt(self, neue_event_aktion :str):
        if not isinstance(neue_event_aktion, str):
            raise TypeError("neue_event_aktion must be a string")
        else:
            self.__akt = neue_event_aktion

    @property
    def name(self) -> str:
        return self.__name
    @name.setter
    def name(self, neuer_name:str):
        if not isinstance(neuer_name, str):
            raise TypeError("neuer_name must be a string")
        else:
            self.__name = neuer_name

    @property
    def dauer(self) -> int:
        return self.__dauer
    @dauer.setter
    def dauer(self, neue_dauer_in_stunden:int):
        if not isinstance(neue_dauer_in_stunden, int):
            raise TypeError("neue_dauer_in_stunden must be an integer")
        else:
            self.__dauer = neue_dauer_in_stunden

    @property
    def taeglich(self) -> bool:
        return self.__taeglich
    @taeglich.setter
    def taeglich(self, ist_taeglich:bool):
        if not isinstance(ist_taeglich, bool):
            raise TypeError("ist_taeglich must be a boolean")
        else:
            self.__taeglich = ist_taeglich

    @property
    def monatlich(self) -> bool:
        return self.__monatlich
    @monatlich.setter
    def monatlich(self, ist_monatlich:bool):
        self.__monatlich = ist_monatlich

    @property
    def jaehrlich(self) -> bool:
        return self.__jaehrlich
    @jaehrlich.setter
    def jaehrlich(self, ist_jaehrlich:bool):
        if not isinstance(ist_jaehrlich, bool):
            raise TypeError("ist_jaehrlich must be a boolean")
        else:
            self.__jaehrlich = ist_jaehrlich

    def __str__(self) -> str:
        return (f"Event: {self.__name}\n"
                f"Zeit: {self.__zeit.jahr}-{self.__zeit.monat:02d}-{self.__zeit.tag:02d} "
                f"{self.__zeit.stunde:02d}:{self.__zeit.minute:02d}:{self.__zeit.sekunde:02d}\n"
                f"Dauer: {self.__dauer} Stunden\n"
                f"Täglich: {self.__taeglich}\n"
                f"Monatlich: {self.__monatlich}\n"
                f"Jährlich: {self.__jaehrlich}\n")



if __name__ == "__main__":
    dz = Datumzeit()
    dz.jetzt()
    print(Event(dz))

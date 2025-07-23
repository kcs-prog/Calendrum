from m_datumzeit import Datumzeit

class Event:
    """Repräsentiert ein Event mit Zeit, Aktion, Name und Dauer.
    ————————————Attribute: ————————————
        event_zeit (Datumzeit): Zeitstempel des Events
        event_liste (list[Event]): Liste, in der die Events zwischengespeichert werden, verwaltet durch den Eventmanager.
        event_akt (str): Aktion, die beim Triggern des Events ausgelöst werden soll.
        event_name (str): Name des Events zur darstellung in der UI. Soll vom User verändert werden können.
        taeglich (bool): Ob das Event bei Ablauf auf den nächsten Tag verschoben werden soll.
        monatlich (bool): Ob das Event bei Ablauf auf den nächsten Monat verschoben werden soll.
        jaehrlich (bool): Ob das Event bei Ablauf auf das nächste Jahr verschoben werden soll.
    ————————————Methoden: ————————————
        abgelaufen(zeitpunkt: Datumzeit) → bool: Prüft, ob das Event abgelaufen ist.
    """
    def __init__(
            self,
            event_zeit :Datumzeit,
            event_liste :list,
            event_akt :str = "",
            event_name :str = "",
            taeglich :bool = False,
            monatlich :bool = False,
            jaehrlich :bool = False,):
        self.__liste = event_liste
        self.__zeit = event_zeit
        self.__akt = event_akt
        self.__name = event_name
        self.__taeglich = taeglich
        self.__monatlich = monatlich
        self.__jaehrlich = jaehrlich
        if not self.__liste:self.__id = 1
        else:
            id_liste = []
            for event in self.__liste:id_liste.append(event.id)
            self.__id = max(id_liste) + 1

    @property
    def liste(self) -> list:
        """Gibt die Liste der Events zurück.
        :return: Liste der Events."""
        return self.__liste
    @liste.setter
    def liste(self, event_liste:list):
        if not isinstance(event_liste, list):
            raise TypeError("event_liste muss eine Liste sein.")
        else:
            self.__liste = event_liste

    @property
    def id(self) -> int: # für id kein setter, da id automatisch generiert wird
        """Gibt die ID des Events zurück.
        :return: ID des Events als int."""
        return self.__id

    @property
    def zeit(self) -> list[int]:
        """Gibt die Zeit des Events als Liste zum Vergleichen zurück.
        :return: Liste mit Jahr, Monat, Tag, Stunde, Minute und Sekunde des Events."""
        return [self.__zeit.jahr,
                self.__zeit.monat,
                self.__zeit.tag,
                self.__zeit.stunde,
                self.__zeit.minute,
                self.__zeit.sekunde]
    @zeit.setter
    def zeit(self, neue_event_zeit :Datumzeit):
        if not isinstance(neue_event_zeit, Datumzeit):
            raise TypeError("neue_event_zeit muss ein Datumzeit-Objekt sein.")
        else:
            self.__zeit = neue_event_zeit

    @property
    def akt(self) -> str:
        """Gibt die Aktion des Events zurück.
        :return: Aktion des Events als String."""
        return self.__akt
    @akt.setter
    def akt(self, neue_event_aktion :str):
        if not isinstance(neue_event_aktion, str):
            raise TypeError("neue_event_aktion muss ein String sein.")
        else:
            self.__akt = neue_event_aktion

    @property
    def name(self) -> str:
        """Gibt den Namen des Events zurück. Der Name kann vom User geändert werden.
        :return: Name des Events als String."""
        return self.__name
    @name.setter
    def name(self, neuer_name:str):
        if not isinstance(neuer_name, str):
            raise TypeError("neuer_name muss ein String sein.")
        else:
            self.__name = neuer_name

    @property
    def taeglich(self) -> bool:
        """Gibt zurück, ob das Event täglich wiederholt werden soll.
        :return: True, wenn das Event täglich wiederholt werden soll, sonst False."""
        return self.__taeglich
    @taeglich.setter
    def taeglich(self, ist_taeglich:bool):
        if not isinstance(ist_taeglich, bool):
            raise TypeError("ist_taeglich muss ein boolean sein.")
        else:
            self.__taeglich = ist_taeglich

    @property
    def monatlich(self) -> bool:
        """Gibt zurück, ob das Event monatlich wiederholt werden soll.
        :return: True, wenn das Event monatlich wiederholt werden soll, sonst False."""
        return self.__monatlich
    @monatlich.setter
    def monatlich(self, ist_monatlich:bool):
        self.__monatlich = ist_monatlich

    @property
    def jaehrlich(self) -> bool:
        """Gibt zurück, ob das Event jährlich wiederholt werden soll.
        :return: True, wenn das Event jährlich wiederholt werden soll, sonst False."""
        return self.__jaehrlich
    @jaehrlich.setter
    def jaehrlich(self, ist_jaehrlich:bool):
        if not isinstance(ist_jaehrlich, bool):
            raise TypeError("ist_jaehrlich muss ein boolean sein.")
        else:
            self.__jaehrlich = ist_jaehrlich

    def __str__(self) -> str:
        """Gibt eine lesbare Darstellung des Events zurück.
        :return: String mit den Details des Events."""
        return (f"EventNr: {self.id}\n"
                f"Name: {self.__name}\n"
                f"Zeit: {self.__zeit.jahr}-{self.__zeit.monat:02d}-{self.__zeit.tag:02d} "
                f"{self.__zeit.stunde:02d}:{self.__zeit.minute:02d}:{self.__zeit.sekunde:02d} Uhr\n"
                f"Täglich: {self.__taeglich}\n"
                f"Monatlich: {self.__monatlich}\n"
                f"Jährlich: {self.__jaehrlich}\n")

    def abgelaufen(self, zeitpunkt:Datumzeit) -> bool:
        """Prüft, ob das Event abgelaufen ist.
        :param zeitpunkt: Zeitpunkt, zu dem geprüft werden soll, ob das Event abgelaufen ist.
        :return: True, wenn das Event abgelaufen ist, sonst False."""
        if not isinstance(zeitpunkt, Datumzeit):
            raise TypeError("zeitpunkt muss ein Datumzeit-Objekt sein.")
        event_zeit = [
            self.__zeit.jahr,
            self.__zeit.monat,
            self.__zeit.tag,
            self.__zeit.stunde,
            self.__zeit.minute,
            self.__zeit.sekunde
        ]
        zeit_stempel = [
            zeitpunkt.jahr,
            zeitpunkt.monat,
            zeitpunkt.tag,
            zeitpunkt.stunde,
            zeitpunkt.minute,
            zeitpunkt.sekunde
        ]
        return event_zeit <= zeit_stempel



if __name__ == "__main__":
    dz = Datumzeit()
    dz.jetzt()
    event1 = Event(event_zeit=dz, event_name="test", event_liste=[])
    print(event1)

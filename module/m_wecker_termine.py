from m_datumzeit import Datumzeit
from m_eventman import Eventman

class Wecker:
    def __init__(self,dz:Datumzeit,em:Eventman):
        self._datumzeit = dz
        self._eventmanager = em
        pass

    def get_datumzeit(self) -> Datumzeit:
        """ Funktion, die das Datum und die Uhrzeit zurückgibt. """
        return self._datumzeit

    def set_datumzeit(self, jahr, monat, tag, minute, sekunde) -> None:
        """ Funktion, die das Datum und die Uhrzeit nach Eingabe und Überprüfung einbindet. """
        if not (1 <= jahr <= 2999):
            print("Ungültiges Jahr!")
            return
        if not (1 <= monat <= 12):
            print("Ungültiger Monat!")
            return
        if not (1 <= tag <= 31):
            print("Ungültiger Tag!")
            return
        if not (0 <= minute < 60):
            print("Ungültige Minute!")
            return
        if not (0 <= sekunde < 60):
            print("Ungültige Sekunde!")
            return

        self._datumzeit.jahr = jahr
        self._datumzeit.monat = monat
        self._datumzeit.tag = tag
        self._datumzeit.minute = minute
        self._datumzeit.sekunde = sekunde

    def aktivieren(self): 
        if self._datumzeit == em.triggerX
            print("Aktivierung wird ausgeführt!")


    def schlummermodus(self, minuten: int, stunden) -> None:
        """ Funktion, die es erlaubt, die Uhrzeit des Weckers neu einzustellen, so dass er später erneut aktiviert wird. """
        # Holt aktuelle Zeit
        aktuelle_zeit = Datumzeit()
        aktuelle_zeit.systemzeit()

        # Neue Zeit berechnen: Alles bleibt gleich, nur Minuten und Stunden werden erhöht
        neue_minute = self._datumzeit.minute + minuten
        neue_stunde = self._datumzeit.stunde + stunden
        neue_tag = self._datumzeit.tag
        neue_monat = self._datumzeit.monat
        neue_jahr = self._datumzeit.jahr

        # Minutenüberlauf berücksichtigen
        if neue_minute >= 60:
            neue_minute -= 60
            neue_stunde += 1

        # Stundenüberlauf berücksichtigen
        if neue_stunde >= 24:
            neue_stunde = 0
            neue_tag += 1

        self._datumzeit.set_datumzeit(
            jahr=neue_jahr,
            monat=neue_monat,
            tag=neue_tag,
            minute=neue_minute,
            sekunde=0  
        )

        print(f"Wecker in Schlummermodus neuer Alarm um {neue_stunde:02}:{neue_minute:02} Uhr.")
    
    def einstellen(self)-> None:
        pass
    
    def create_event(self)-> None:
        pass
    
    def del_me(self)-> None:
        self._datumzeit = 0



class Termine(Wecker):
    def __init__(self,dz:Datumzeit, em:Eventmanager):
        super.__init__(dz,em)


if __name__ == '__main__':
    EinWecker = Wecker()
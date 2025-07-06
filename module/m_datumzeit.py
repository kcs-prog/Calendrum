"""
Datumzeit
————————————
+jahr:int
+monat:int
+tag:int
+stunde:int
+minute:int
+sekunde:int
————————————
+inti(J, M, D, h, m, s)
+jump(dz:Datumzeit, [richtung:int=+1]):None
+maxTage(Monat:int):int
+istSchaltjahr(Jahr:int):bool
+ systemzeit(): None
+ wochentag(): str

"""
from logging import exception
from time import strftime

class Datumzeit:
    def __init__(self, J:int=0, M:int=0, T:int=0, h:int=0, m:int=0, s:int=0):
        if J: self.jahr = J
        else: self.__jahr = 0
        if M: self.monat = M
        else: self.__monat = 0
        if T: self.tag = T
        else: self.__tag = 0
        self.stunde = h
        self.minute = m
        self.sekunde = s
        self.__is_set = False if J + M + T + h + m + s == 0 else True
        self.wochentag = self.__gen_wochentag() if self.__is_set else "None"

    def get_jahr(self):
        return self.__jahr if self.__chk_jahr(self.__jahr) else None
    def set_jahr(self, J):
        if self.__chk_jahr(J): self.__jahr = J; self.__set_ein()
    def __chk_jahr(self,J)->bool:
        if type(J) != int:
            raise exception("Jahr muss int sein")
        elif not 0 < J < 3000:
            raise exception("Jahr außerhalb des Geltungsbereichs [1,3000[")
        else:
            return True
    jahr = property(get_jahr, set_jahr)

    def get_monat(self):
        return self.__monat if self.__chk_monat(self.__monat) else None
    def set_monat(self, M):
        if M < 1:
            M = 12
        elif M > 12:
            M = 1
        if not 1 <= M <= 12:
            raise exception("Monat außerhalb des Geltungsbereichs [1,12]")
        self.__monat = M
        self.__set_ein()
    def __chk_monat(self,M)->bool:
        if type(M) != int:
            raise exception("Monat muss int sein")
        if not 1 < M <= 12:
            raise Exception("Monat außerhalb des Geltungsbereichs [1,12]")
        else:
            return True
    monat = property(get_monat, set_monat)

    def get_tag(self):
        return self.__tag if self.__chk_tag(self.__tag) else None
    def set_tag(self, T):
        if self.__chk_tag(T): self.__tag = T; self.__set_ein()
    def __chk_tag(self,T)->bool:
        if type(T) != int:
            raise exception("Tag muss int sein")
        elif not 0 < T <= 32:
            raise exception("Tag außerhalb des Geltungsbereichs [1,12]")
        else:
            return True
    tag = property(get_tag, set_tag)

    def get_stunde(self):
        return self.__stunde if self.__chk_stunde(self.__stunde) else None
    def set_stunde(self, h):
        if self.__chk_stunde(h): self.__stunde = h; self.__set_ein()
    def __chk_stunde(self,h)->bool:
        if type(h) != int:
            raise exception("Stunde muss int sein")
        elif not 0 <= h <= 24:
            raise exception("Stunde außerhalb des Geltungsbereichs [0,24]")
        else:
            return True
    stunde = property(get_stunde, set_stunde)

    def get_minute(self):
        return self.__minute if self.__chk_minute(self.__minute) else None
    def set_minute(self, m):
        if self.__chk_minute(m): self.__minute = m; self.__set_ein()
    def __chk_minute(self,m)->bool:
        if type(m) != int:
            raise exception("Minute muss int sein")
        elif not 0 <= m <= 59:
            raise exception("Minute außerhalb des Geltungsbereichs [0,59]")
        else:
            return True
    minute = property(get_minute, set_minute)

    def get_sekunde(self):
        return self.__sekunde if self.__chk_sekunde(self.__sekunde) else None
    def set_sekunde(self, s):
        if self.__chk_sekunde(s): self.__sekunde = s; self.__set_ein()
    def __chk_sekunde(self,s)->bool:
        if type(s) != int:
            raise exception("Sekunde muss int sein")
        elif not 0 <= s <= 59:
            raise exception("Sekunde außerhalb des Geltungsbereichs [0,59]")
        else:
            return True
    sekunde = property(get_sekunde, set_sekunde)

    def __str__(self)->str:
        return f"{self.jahr:4d}.{self.monat:02d}.{self.tag:02d} {self.stunde:02d}:{self.minute:02d}:{self.sekunde:02d}" if self.__is_set else "nicht gesetzt"

    def __gen_wochentag(self)->str:
        y = self.jahr
        m = self.monat
        t = self.tag
        # Monat anpassen: Januar und Februar als Monate 13 und 14 des Vorjahres
        if m < 3:
            m += 12
            y -= 1
        # Zeller-Formel
        h = (t + ((13 * (m + 1)) // 5) + y + (y // 4) - (y // 100) + (y // 400)) % 7
        # Zuordnung des Wochentags
        return ["Samstag", "Sonntag", "Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"][h]

    def __set_ein(self)->None:
        self.__is_set = True

    def jetzt(self)->None:
        """setzt Datum und Zeit auf die jetzige Systemzeit"""
        dz_list = strftime("%Y,%m,%d,%H,%M,%S").split(sep=",")
        self.jahr = int(dz_list[0])
        self.monat = int(dz_list[1])
        self.tag = int(dz_list[2])
        self.stunde = int(dz_list[3])
        self.minute = int(dz_list[4])
        self.sekunde = int(dz_list[5])

if __name__ == '__main__':
    dz = Datumzeit(2025,2,17,6,35,00)
    print(dz.minute)
    dz.minute = 6
    dz2 = Datumzeit()
    print(dz2.wochentag)
    print(dz2)
    dz2.jetzt()
    print(dz2)
    list = dz2
    print(dz.minute)
    print(dz.wochentag)
    print(dz)
    dz.jetzt()
    print(dz)
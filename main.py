
#A program kezeli a foglalásokat, szobákat, csináltam egy gdepremium szobát is. :)
#Kezeli a lemondásokat is. Hibás dátumra, szobaszámra, létező foglalásra, stb. Csak jövőbeni foglalás lehetséges. Nem lehet szobát foglalni ha már valaki foglalt előzőleg.
# Gál Róbert - ZB2QIY
from abc import ABC, abstractmethod
import datetime

# Absztrakt Szoba osztály
class Szoba(ABC):
    def __init__(self, ar, szobaszam):
        self.ar = ar
        self.szobaszam = szobaszam

    @abstractmethod
    def leiras(self):
        pass

# EgyágyasSzoba osztály
class EgyagyasSzoba(Szoba):
    def __init__(self, ar, szobaszam):
        super().__init__(ar, szobaszam)

    def leiras(self):
        return f"Egyágyas szoba, Ár: {self.ar}, Szobaszám: {self.szobaszam}"

# KétágyasSzoba osztály
class KetagyasSzoba(Szoba):
    def __init__(self, ar, szobaszam):
        super().__init__(ar, szobaszam)

    def leiras(self):
        return f"Kétágyas szoba, Ár: {self.ar}, Szobaszám: {self.szobaszam}"

# Foglalás osztály
class Foglalas:
    def __init__(self, szoba, datum):
        self.szoba = szoba
        self.datum = datum

    def __str__(self):
        return f"Foglalás - Szoba: {self.szoba.szobaszam}, Dátum: {self.datum}"

# Szálloda osztály
class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []
        self.foglalasok = []

    def szoba_hozzaad(self, szoba):
        self.szobak.append(szoba)

    def foglalas(self, szobaszam, datum):
        if datum < datetime.date.today():
            raise ValueError("A dátumnak a jövőben kell lennie.")
        for foglalas in self.foglalasok:
            if foglalas.szoba.szobaszam == szobaszam and foglalas.datum == datum:
                raise ValueError("Ez a szoba már foglalt ezen a napon.")
        for szoba in self.szobak:
            if szoba.szobaszam == szobaszam:
                uj_foglalas = Foglalas(szoba, datum)
                self.foglalasok.append(uj_foglalas)
                return szoba.ar
        raise ValueError("Nincs ilyen szobaszám.")

    def foglalas_lemondas(self, szobaszam, datum):
        for foglalas in self.foglalasok:
            if foglalas.szoba.szobaszam == szobaszam and foglalas.datum == datum:
                self.foglalasok.remove(foglalas)
                return
        raise ValueError("Nincs ilyen foglalás.")

    def foglalasok_listazasa(self):
        if not self.foglalasok:
            print("Nincsenek foglalások.")
        for foglalas in self.foglalasok:
            print(foglalas)

# Felhasználói interfész
def main():
    szalloda = Szalloda("Példa Szálloda")
    # Példa szobák és foglalások hozzáadása
    egyagyas = EgyagyasSzoba(10000, 101)
    ketagyas = KetagyasSzoba(20000, 102)
    gdepremium = EgyagyasSzoba(ar=30000, szobaszam=103)
    szalloda.szoba_hozzaad(egyagyas)
    szalloda.szoba_hozzaad(ketagyas)
    szalloda.szoba_hozzaad(gdepremium)
    # További foglalások hozzáadása (opcionális)

    while True:
        print("\n1. Szoba foglalás")
        print("2. Foglalás lemondás")
        print("3. Foglalások listázása")
        print("4. Kilépés")
        valasztas = input("Válasszon egy opciót: ")

        if valasztas == '1':
            try:
                szobaszam = int(input("Adja meg a szobaszámot: "))
                ev, ho, nap = map(int, input("Adja meg a dátumot (év hó nap): ").split())
                datum = datetime.date(ev, ho, nap)
                ar = szalloda.foglalas(szobaszam, datum)
                print(f"Foglalás megtörtént, ár: {ar} Ft")
            except Exception as e:
                print(e)
        elif valasztas == '2':
            try:
                szobaszam = int(input("Adja meg a szobaszámot: "))
                ev, ho, nap = map(int, input("Adja meg a lemondás dátumát (év hó nap): ").split())
                datum = datetime.date(ev, ho, nap)
                szalloda.foglalas_lemondas(szobaszam, datum)
                print("Foglalás lemondva.")
            except Exception as e:
                print(e)
        elif valasztas == '3':
            szalloda.foglalasok_listazasa()
        elif valasztas == '4':
            break
        else:
            print("Érvénytelen választás.")

if __name__ == "__main__":
    main()

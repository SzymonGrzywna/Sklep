SCIEZKA_DANYCH = "dane"
PLIK_KONTO    = "dane/konto.txt"
PLIK_MAGAZYN  = "dane/magazyn.txt"
PLIK_HISTORIA = "dane/historia.txt"


def wczytaj_konto():
    try:
        with open(PLIK_KONTO, "r") as f:
            txt = f.read().strip()
            return float(txt) if txt else 0.0
    except FileNotFoundError:
        zapisz_konto(0.0)
        return 0.0
    except ValueError:
        return 0.0


def zapisz_konto(kwota: float):
    with open(PLIK_KONTO, "w") as f:
        f.write(f"{kwota}\n")


def wczytaj_magazyn():
    magazyn = []
    try:
        with open(PLIK_MAGAZYN, "r") as f:
            for linia in f:
                linia = linia.strip()
                if not linia:
                    continue
                pola = linia.split(";")  # NAZWA;CENA;ILOSC
                if len(pola) != 3:
                    continue
                nazwa = pola[0]
                try:
                    cena = float(pola[1])
                    ilosc = int(pola[2])
                except ValueError:
                    continue
                magazyn.append({
                    "nazwa_produktu": nazwa,
                    "cena_produktu": cena,
                    "ilosc_dostepna": ilosc
                })
        return magazyn
    except FileNotFoundError:
        # jeśli brak pliku – utwórz pusty i zwróć pusty magazyn
        zapisz_magazyn(magazyn)
        return magazyn


def zapisz_magazyn(magazyn_lista):
    with open(PLIK_MAGAZYN, "w") as f:
        for p in magazyn_lista:
            f.write(f"{p['nazwa_produktu']};{p['cena_produktu']};{p['ilosc_dostepna']}\n")


def wczytaj_historie():
    try:
        with open(PLIK_HISTORIA, "r") as f:
            return [linia.strip() for linia in f if linia.strip()]
    except FileNotFoundError:
        # brak pliku – utwórz pusty i zwróć pustą historię
        with open(PLIK_HISTORIA, "w") as _:
            pass
        return []


def dopisz_do_historii(linia: str):
    with open(PLIK_HISTORIA, "a") as f:
        f.write(linia.rstrip() + "\n")

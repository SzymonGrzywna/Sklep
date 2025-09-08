import os

SCIEZKA_DANYCH = os.path.join(os.path.dirname(__file__), "dane")
PLIK_KONTO = os.path.join(SCIEZKA_DANYCH, "konto.txt")
PLIK_MAGAZYN = os.path.join(SCIEZKA_DANYCH, "magazyn.txt")
PLIK_HISTORIA = os.path.join(SCIEZKA_DANYCH, "historia.txt")


def _upewnij_sie_ze_folder_istnieje():
    os.makedirs(SCIEZKA_DANYCH, exist_ok=True)


# ===== KONTO =====
def wczytaj_konto():
    _upewnij_sie_ze_folder_istnieje()
    if not os.path.exists(PLIK_KONTO):
        zapisz_konto(0.0)
        return 0.0
    with open(PLIK_KONTO, "r", encoding="utf-8") as f:
        tekst = f.read().strip()
        if tekst == "":
            return 0.0
        try:
            return float(tekst)
        except ValueError:
            return 0.0


def zapisz_konto(kwota: float):
    _upewnij_sie_ze_folder_istnieje()
    with open(PLIK_KONTO, "w", encoding="utf-8") as f:
        f.write(f"{kwota}\n")


# ===== MAGAZYN =====
def wczytaj_magazyn():
    _upewnij_sie_ze_folder_istnieje()
    magazyn = []
    if not os.path.exists(PLIK_MAGAZYN):
        zapisz_magazyn(magazyn)
        return magazyn
    with open(PLIK_MAGAZYN, "r", encoding="utf-8") as f:
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


def zapisz_magazyn(magazyn_lista):
    _upewnij_sie_ze_folder_istnieje()
    with open(PLIK_MAGAZYN, "w", encoding="utf-8") as f:
        for p in magazyn_lista:
            f.write(f"{p['nazwa_produktu']};{p['cena_produktu']};{p['ilosc_dostepna']}\n")


# ===== HISTORIA =====
def wczytaj_historie():
    _upewnij_sie_ze_folder_istnieje()
    historia = []
    if not os.path.exists(PLIK_HISTORIA):
        with open(PLIK_HISTORIA, "w", encoding="utf-8") as _:
            pass
        return historia
    with open(PLIK_HISTORIA, "r", encoding="utf-8") as f:
        for linia in f:
            linia = linia.strip()
            if not linia:
                continue
            historia.append(linia)
    return historia


def dopisz_do_historii(linia: str):
    _upewnij_sie_ze_folder_istnieje()
    with open(PLIK_HISTORIA, "a", encoding="utf-8") as f:
        f.write(linia.rstrip() + "\n")

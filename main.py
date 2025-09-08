from pliki import (
    wczytaj_konto, zapisz_konto,
    wczytaj_magazyn, zapisz_magazyn,
    wczytaj_historie, dopisz_do_historii
)

def wczytaj_float(tekst):
    try:
        return float(input(tekst).strip().replace(",", "."))
    except ValueError:
        print("Błąd: musisz podać liczbę (np. 3.49 albo 3,49).")
        return None



stan_konta = wczytaj_konto()
magazyn = wczytaj_magazyn()
historia = wczytaj_historie()

def pokaz_menu():
    print()
    print(30 * "V")
    print("Lista dostępnych komend: ")
    print(30 * "V")
    print("-= SALDO =-")
    print("-= SPRZEDAZ =-")
    print("-= ZAKUP =-")
    print("-= KONTO =-")
    print("-= LISTA =-")
    print("-= MAGAZYN =-")
    print("-= PRZEGLAD =-")
    print("-= KONIEC =-")
    print()


def znajdz_produkt(nazwa):
    for p in magazyn:
        if p["nazwa_produktu"] == nazwa:
            return p
    return None


while True:
    pokaz_menu()
    komenda = input("Wprowadź komendę: ").strip().upper()
    print(f"Wprowadziłeś komendę: {komenda}")

    # ------------------- KONIEC ----------------
    if komenda == "KONIEC":
        print("\n======== KOŃCZYMY DZIAŁANIE PROGRAMU =======")
        break

    # ---------------- SALDO ---------------------
    elif komenda == "SALDO":
        print("\nCo chcesz zrobić ze stanem konta?")
        print("1 – DODAJ (+)")
        print("2 – ODEJMIJ (-)")
        wybor = input("Wybierz 1 lub 2: ").strip()
        if wybor == "1":
            kwota = wczytaj_float("Ile chcesz DODAĆ? ")
            if kwota is None:
                continue
            stan_konta += kwota
            zapisz_konto(stan_konta)
            linia_hist = f"saldo;{kwota}"
            dopisz_do_historii(linia_hist)
            historia.append(linia_hist)
            print("Dodano (+):", kwota, "zł")

        elif wybor == "2":
            kwota = wczytaj_float("Ile chcesz ODJĄĆ? ")
            if kwota is None:
                continue
            stan_konta -= kwota
            zapisz_konto(stan_konta)
            linia_hist = f"saldo;{-kwota}"
            dopisz_do_historii(linia_hist)
            historia.append(linia_hist)
            print(f"Odjęto (-): {kwota} zł")
        else:
            print("Niepoprawny wybór – wracam do menu.")

        print("Aktualny stan konta:", stan_konta, "zł")

    # --------------- SPRZEDAZ -------------------
    elif komenda == "SPRZEDAZ":
        wybrany_produkt = input("\nJaki produkt chcesz sprzedać? ").strip().upper()
        try:
            ilosc_produktu = int(input("Ile szt? ").strip())
        except ValueError:
            print("Błąd: ilość musi być liczbą całkowitą.")
            continue

        produkt = znajdz_produkt(wybrany_produkt)
        if produkt is None:
            print("Brak produktu w magazynie")
            continue
        if ilosc_produktu <= 0:
            print("Ilość musi być dodatnia.")
            continue
        if ilosc_produktu > produkt["ilosc_dostepna"]:
            print("Brak wystarczającej ilości produktu.")
            continue


        produkt["ilosc_dostepna"] -= ilosc_produktu
        przychod = produkt["cena_produktu"] * ilosc_produktu
        stan_konta += przychod


        zapisz_magazyn(magazyn)
        zapisz_konto(stan_konta)
        linia_hist = f"sprzedaz;{wybrany_produkt};{produkt['cena_produktu']};{ilosc_produktu}"
        dopisz_do_historii(linia_hist)
        historia.append(linia_hist)

        print(f"Sprzedano {ilosc_produktu} x {wybrany_produkt} po {produkt['cena_produktu']} zł. +{przychod} zł")
        print(f"Stan konta: {stan_konta} zł")

    # ----------------- ZAKUP ----------------
    elif komenda == "ZAKUP":
        wybrany_produkt = input("\nJaki produkt chcesz kupić? ").strip().upper()
        cena = wczytaj_float("Podaj cenę za sztukę: ")
        if cena is None:
            continue
        try:
            ilosc = int(input("Ile sztuk kupujesz? ").strip())
        except ValueError:
            print("Błąd: ilość musi być liczbą całkowitą.")
            continue

        if cena <= 0 or ilosc <= 0:
            print("Cena i ilość muszą być dodatnie.")
            continue

        koszt = cena * ilosc
        if koszt > stan_konta:
            print("Nie masz tyle środków na koncie.")
            continue

        produkt = znajdz_produkt(wybrany_produkt)
        if produkt:
            produkt["ilosc_dostepna"] += ilosc
            produkt["cena_produktu"] = cena  # aktualizacja ceny
        else:
            magazyn.append({
                "nazwa_produktu": wybrany_produkt,
                "cena_produktu": cena,
                "ilosc_dostepna": ilosc
            })

        stan_konta -= koszt

        # persist
        zapisz_magazyn(magazyn)
        zapisz_konto(stan_konta)
        linia_hist = f"zakup;{wybrany_produkt};{cena};{ilosc}"
        dopisz_do_historii(linia_hist)
        historia.append(linia_hist)

        print(f"Zakup udany. -{koszt} zł. Stan konta: {stan_konta} zł")

    # --------------------- KONTO -----------------
    elif komenda == "KONTO":
        print(f"\nStan konta: {stan_konta} zł")

    # ---------------- LISTA -----------------
    elif komenda == "LISTA":
        if not magazyn:
            print("Magazyn jest pusty.")
        else:
            print("\n=== MAGAZYN (Nazwa | Cena | Ilość) ===")
            for p in magazyn:
                print(f"{p['nazwa_produktu']} | {p['cena_produktu']} zł | {p['ilosc_dostepna']} szt.")

    # --------------- MAGAZYN --------------------------
    elif komenda == "MAGAZYN":
        wybrany_produkt = input("\nJaki wybierasz produkt? ").strip().upper()
        produkt = znajdz_produkt(wybrany_produkt)
        if produkt is None:
            print("Brak produktu w magazynie")
        else:
            print(produkt)

    # -------------------- PRZEGLAD -----------------------
    elif komenda == "PRZEGLAD":
        od = input("\nPodaj zakres (od) (ENTER = początek): ").strip()
        do = input("Podaj zakres (do) (ENTER = koniec): ").strip()

        if od == "":
            od_i = 0
        else:
            try:
                od_i = int(od)
            except ValueError:
                print("Błąd: 'od' musi być liczbą.")
                continue

        if do == "":
            do_i = len(historia) - 1
        else:
            try:
                do_i = int(do)
            except ValueError:
                print("Błąd: 'do' musi być liczbą.")
                continue

        if len(historia) == 0:
            print("Historia jest pusta.")
            continue

        if od_i < 0 or do_i >= len(historia) or od_i > do_i:
            print(f"Zakres poza listą! Masz {len(historia)} zapisanych komend.")
            continue

        print("\n--- HISTORIA ---")
        for idx in range(od_i, do_i + 1):
            print(idx, historia[idx])
        print("---------------------")

    else:
        print("Nie znam takiej komendy. Spróbuj ponownie.")

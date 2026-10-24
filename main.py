import argparse
from pathlib import Path
import csv
import random
import json

def zapisz_csv(katalog):
    sciezka_pliku = katalog / "Dane.csv"

    model = random.choice(["A", "B", "C"])
    wynik = random.randint(0, 1000)
    czas = random.randint(0, 1000)

    with open(sciezka_pliku, "w", newline="", encoding="utf-8") as plik:
        writer = csv.writer(
            plik,
            delimiter=";",
            lineterminator="\n"
        )

        writer.writerow(["Model", " Wynik", " Czas", ""])
        writer.writerow([f"{model} ", f" {wynik} ", f" {czas}s", ""])

def odczytaj_csv(sciezka_pliku):
    with open(sciezka_pliku, "r", newline="", encoding="utf-8") as plik:
        reader = csv.reader(plik, delimiter=";")

        next(reader)
        wiersz = next(reader)

    if wiersz[0].strip() == "A":
        czas_tekst = wiersz[2].strip()
        czas_tekst = czas_tekst.removesuffix("s")

        return int(czas_tekst)

    return 0



def zapisz_json(katalog):
    sciezka_pliku = katalog / "Dane.json"
    model = random.choice(["A", "B", "C"])
    wynik = random.randint(0, 1000)
    czas = random.randint(0, 1000)
    dane = {"model": model, "wynik": wynik, "czas": czas}

    with open(sciezka_pliku, "w", newline="",encoding="utf-8") as plik:
        json.dump(dane, plik)


def odczytaj_json(sciezka_pliku):
    with open(sciezka_pliku, "r", encoding="utf-8") as plik:
        odczyt = json.load(plik)

        if odczyt["model"] == "A":
            return odczyt["czas"]
        else: 
            return 0

    


def rozwin_dni(zakres):
    dni_mapa = {
        "pn": "poniedziałek",
        "wt": "wtorek",
        "śr": "środa",
        "cz": "czwartek",
        "pt": "piątek",
        "sb": "sobota",
        "nd": "niedziela",
    }

    if "-" not in zakres:
        return [dni_mapa[zakres]]

    od_dnia, do_dnia = zakres.split("-")
    wynik = []
    dodawaj = False

    for skrot, pelna_nazwa in dni_mapa.items():
        if skrot == od_dnia:
            dodawaj = True
        if dodawaj:
            wynik.append(pelna_nazwa)
        if skrot == do_dnia:
            break

    return wynik


def generuj_sciezki(miesiace, zakresy_dni, pory):
    dni_w_miesiacach = [rozwin_dni(z) for z in zakresy_dni]

    sciezki = []
    pora_idx = 0

    for miesiac, dni in zip(miesiace, dni_w_miesiacach):
        for dzien in dni:
            pora = "wieczorem" if pora_idx < len(pory) and pory[pora_idx] == "w" else "rano"
            sciezki.append(Path(miesiac) / dzien / pora)
            pora_idx += 1

    return sciezki


def parsuj_argumenty():
    parser = argparse.ArgumentParser(
        description="Skrypt do tworzenia i odczytu ustrukturyzowanych danych w katalogach."
    )

    parser.add_argument(
        "-m", "--miesiace",
        nargs="+",
        required=True,
        help="Lista miesięcy (np. styczeń luty)",
    )
    parser.add_argument(
        "-d", "--dni",
        nargs="+",
        required=True,
        help="Zakresy dni tygodnia dla każdego miesiąca (np. pn-wt lub cz)",
    )
    parser.add_argument(
        "-p", "--pory",
        nargs="*",
        default=[],
        help="Pory dnia: r (rano) lub w (wieczorem). Domyślnie rano",
    )
    parser.add_argument(
        "-t", "--tworz",
        action="store_true",
        help="Tworzy strukturę katalogów i pliki (brak flagi oznacza tryb odczytu)",
    )
    parser.add_argument(
        "-c", "--csv",
        action="store_true",
        help="Obsługa formatu CSV",
    )
    parser.add_argument(
        "-j", "--json",
        action="store_true",
        help="Obsługa formatu JSON",
    )

    args = parser.parse_args()

    if len(args.miesiace) != len(args.dni):
        parser.error("Liczba podanych zakresów dni (-d) musi być dokładnie równa liczbie miesięcy (-m)!")

    if not args.csv and not args.json:
        args.csv = True
        args.json = True

    return args


def main():
    args = parsuj_argumenty()
    sciezki = generuj_sciezki(args.miesiace, args.dni, args.pory)

    if args.tworz:
        print("TRYB TWORZENIA")
        for sciezka in sciezki:
            sciezka.mkdir(parents=True, exist_ok=True)
            print(f"Katalog: {sciezka}")

            if args.csv:
                zapisz_csv(sciezka)
            if args.json:
                zapisz_json(sciezka)

        print("Zakończono tworzenie plików.")
    else:
        print("TRYB ODCZYTU")
        czas_csv = 0
        czas_json = 0

        for sciezka in sciezki:
            if not sciezka.exists():
                print(f"Pominięto (ścieżka nie istnieje): {sciezka}")
                continue

            plik_csv = sciezka / "Dane.csv"
            plik_json = sciezka / "Dane.json"

            if args.csv and plik_csv.exists():
                czas_csv += odczytaj_csv(plik_csv)

            if args.json and plik_json.exists():
                czas_json += odczytaj_json(plik_json)

        if args.csv:
            print(f"Łączny czas dla modelu A (CSV): {czas_csv}s")
        if args.json:
            print(f"Łączny czas dla modelu A (JSON): {czas_json}s")


main()

import pandas as pd
import os


def add_drug(drug_id, name, price, prescription_required, stock, file_path="drugs.xlsx"):
    """
    Dodaje nowy lek do pliku Excel. Jeśli plik nie istnieje lub jest pusty, tworzy go od nowa.

    :param drug_id: ID leku (int)
    :param name: nazwa leku (str)
    :param price: cena leku (float)
    :param prescription_required: czy wymaga recepty (bool)
    :param stock: ilość dostępnych sztuk (int)
    :param file_path: ścieżka do pliku Excel
    """
    try:
        # Jeśli plik nie istnieje lub jest pusty/uszkodzony
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            df = pd.DataFrame(columns=["ID", "Name", "Price", "Prescription", "Stock"])
        else:
            try:
                df = pd.read_excel(file_path)
                # Jeśli brakuje kolumn, nadpisz nagłówki
                required_columns = {"ID", "Name", "Price", "Prescription", "Stock"}
                if not required_columns.issubset(set(df.columns)):
                    df = pd.DataFrame(columns=list(required_columns))
            except Exception:
                # W razie błędu podczas odczytu pliku — utwórz nowy DataFrame
                df = pd.DataFrame(columns=["ID", "Name", "Price", "Prescription", "Stock"])

        # Sprawdź, czy ID już istnieje
        if not df.empty and drug_id in df["ID"].values:
            print(f"Lek o ID {drug_id} już istnieje!")
            return

        new_row = {
            "ID": drug_id,
            "Name": name,
            "Price": price,
            "Prescription": "Yes" if prescription_required else "No",
            "Stock": stock
        }

        new_df = pd.DataFrame([new_row])

        if df.empty:
            df = new_df
        else:
            df = pd.concat([df, new_df], ignore_index=True)
        df.to_excel(file_path, index=False)
        print(f"Lek '{name}' został dodany.")
    except Exception as e:
        print("Błąd podczas dodawania leku:", e)


def remove_drug(identifier, file_path="drugs.xlsx"):
    """
    Usuwa lek z pliku na podstawie ID (int) lub nazwy (str).

    :param identifier: ID lub nazwa leku
    :param file_path: ścieżka do pliku Excel
    """
    try:
        if not os.path.exists(file_path):
            print("Plik leków nie istnieje!")
            return

        df = pd.read_excel(file_path)

        if isinstance(identifier, int):
            df = df[df["ID"] != identifier]
        elif isinstance(identifier, str):
            df = df[df["Name"].str.lower() != identifier.lower()]
        else:
            raise ValueError("Nieprawidłowy identyfikator (ID lub nazwa).")

        df.to_excel(file_path, index=False)
        print(f"Lek '{identifier}' został usunięty.")
    except Exception as e:
        print("Błąd podczas usuwania leku:", e)
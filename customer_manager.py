import csv
import os
import random
import pandas as pd
from datetime import datetime, timedelta

def generate_unique_id(existing_ids):
    while True:
        new_id = random.randint(1000, 9999)
        if new_id not in existing_ids:
            return new_id

def generate_next_id(existing_ids):
    return max(existing_ids) + 1 if existing_ids else 1000

def register_customer(customer_file="customer.csv", address_file="address.csv", database_folder="DATABASE"):
    try:
        # Dane osobowe klienta
        full_name = input("Imię i nazwisko: ").strip()
        email = input("Adres e-mail: ").strip()
        phone = input("Numer telefonu: ").strip()
        # Dane adresowe
        street = input("Ulica i numer: ").strip()
        city = input("Miasto: ").strip()
        zip_code = input("Kod pocztowy: ").strip()

        # Sprawdzenie istniejących ID
        existing_ids = set()
        if os.path.exists(customer_file):
            with open(customer_file, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                existing_ids = set()
                for row in reader:
                    try:
                        existing_ids.add(int(row["ID"]))
                    except (KeyError, ValueError):
                        continue

        customer_id = generate_unique_id(existing_ids)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Zapis do customer.csv
        customer_exists = os.path.exists(customer_file)
        with open(customer_file, "a", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not customer_exists:
                writer.writerow(["ID", "Name", "E-mail", "Phone", "Created", "Updated"])
            writer.writerow([customer_id, full_name, email, phone, now, now])

        # Zapis do address.csv
        address_exists = os.path.exists(address_file)
        with open(address_file, "a", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not address_exists:
                writer.writerow(["Customer ID", "Street", "City", "ZIP"])
            writer.writerow([customer_id, street, city, zip_code])

        # Utworzenie pliku zakupów klienta
        os.makedirs(database_folder, exist_ok=True)
        client_file_path = os.path.join(database_folder, f"{customer_id}.txt")
        with open(client_file_path, "w", encoding='utf-8') as f:
            f.write(f"Zakupy klienta {full_name} (ID: {customer_id})\n")
            f.write("-" * 30 + "\n")

        print(f"Zarejestrowano nowego klienta. Numer ID: {customer_id}")

    except Exception as e:
        print("Błąd podczas rejestracji klienta:", e)
def remove_customer(identifier, customer_file="customer.csv", address_file="address.csv", database_folder="DATABASE"):
    """
    Usuwa klienta na podstawie ID (int). Usuwa dane z customer.csv, address.csv i plik z DATABASE/.
    """
    try:
        identifier = str(identifier)
        removed_id = None
        remaining_customers = []

        # --- Część 1: usuwanie z customer.csv ---
        if os.path.exists(customer_file):
            with open(customer_file, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get("ID") == identifier:
                        removed_id = row.get("ID")
                        continue
                    remaining_customers.append(row)

            if removed_id:
                with open(customer_file, "w", newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=remaining_customers[0].keys())
                    writer.writeheader()
                    writer.writerows(remaining_customers)

        # --- Część 2: usuwanie z address.csv ---
        if removed_id and os.path.exists(address_file):
            remaining_addresses = []
            with open(address_file, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get("ID") != removed_id:
                        remaining_addresses.append(row)

            if remaining_addresses:
                with open(address_file, "w", newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=remaining_addresses[0].keys())
                    writer.writeheader()
                    writer.writerows(remaining_addresses)
            else:
                # Jeśli wszystkie adresy zostały usunięte
                with open(address_file, "w", newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["ID", "STREET", "CITY", "COUNTRY"])

        # --- Część 3: usuwanie pliku z DATABASE ---
        if removed_id:
            client_file = os.path.join(database_folder, f"{removed_id}.txt")
            if os.path.exists(client_file):
                os.remove(client_file)

            print(f"✅ Klient o ID {removed_id} został całkowicie usunięty.")
        else:
            print("❌ Nie znaleziono klienta o podanym ID.")

    except Exception as e:
        print("❌ Błąd podczas usuwania klienta:", e)


def update_customer(customer_file="customer.csv"):
    """
    Aktualizuje e-mail i telefon klienta na podstawie jego ID.
    """
    try:
        if not os.path.exists(customer_file):
            print("Brak pliku z klientami.")
            return

        customer_id = input("Podaj ID klienta do aktualizacji: ").strip()

        updated = False
        updated_rows = []

        with open(customer_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        for row in rows:
            if row["ID"] == customer_id:
                print(f"Obecne dane klienta:\n📛 {row['NAME']}\n📧 {row['E-MAIL']}\n📱 {row['PHONE']}")

                new_email = input("Nowy e-mail (Enter = bez zmian): ").strip()
                new_phone = input("Nowy telefon (Enter = bez zmian): ").strip()

                if new_email:
                    row["E-MAIL"] = new_email
                if new_phone:
                    row["PHONE"] = new_phone

                row["UPDATED"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                updated = True

            updated_rows.append(row)

        if updated:
            with open(customer_file, "w", newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=updated_rows[0].keys())
                writer.writeheader()
                writer.writerows(updated_rows)
            print("✅ Dane klienta zostały zaktualizowane.")
        else:
            print("❌ Nie znaleziono klienta o podanym ID.")

    except Exception as e:
        print("❌ Błąd podczas aktualizacji klienta:", e)

def purchase_drugs(customer_id, file_path="drugs.xlsx", database_folder="DATABASE"):
    """
    Klient kupuje dowolną liczbę leków. Jeśli lek wymaga recepty, system o nią zapyta.
    """
    try:
        if not os.path.exists(file_path):
            print("Baza leków nie istnieje.")
            return

        df = pd.read_excel(file_path)

        print("Podaj leki w formacie: nazwa:ilość, np. paracetamol:2, ibuprofen:1")
        user_input = input("Leki: ")

        requested = {}
        for item in user_input.split(","):
            try:
                name, qty = item.strip().split(":")
                requested[name.strip().lower()] = int(qty)
            except ValueError:
                print(f"Błędny format wpisu: {item}")
                continue

        purchased = []

        for name, quantity in requested.items():
            match = df[df["Name"].str.lower() == name]

            if match.empty:
                print(f"Lek '{name}' nie istnieje.")
                continue

            index = match.index[0]
            stock = int(match.at[index, "Stock"])
            prescription_required = match.at[index, "Prescription"] == "Yes"

            if stock < quantity:
                print(f"Za mało leku '{name}' (dostępne: {stock}, żądane: {quantity})")
                continue

            if prescription_required:
                has_prescription = input(f"Lek '{name}' wymaga recepty. Podaj numer recepty lub zostaw puste, aby anulować: ").strip()
                if not has_prescription:
                    print(f"Lek '{name}' nie został zakupiony – brak recepty.")
                    continue
                note = f"{name} x{quantity} (z receptą: {has_prescription})"
            else:
                note = f"{name} x{quantity} (bez recepty)"

            # Odejmij stan magazynowy
            df.at[index, "Stock"] -= quantity
            purchased.append(note)

        if not purchased:
            print("Nie dokonano żadnych zakupów.")
            return

        df.to_excel(file_path, index=False)

        os.makedirs(database_folder, exist_ok=True)
        file_path = os.path.join(database_folder, f"{customer_id}.txt")

        with open(file_path, "a", encoding="utf-8") as f:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            expiry = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
            f.write(f"{now} | Zakupiono: {', '.join(purchased)} | Ważne do: {expiry}\n")

        print(f"Zakup zakończony: {', '.join(purchased)}")

    except Exception as e:
        print("Błąd podczas zakupu:", e)
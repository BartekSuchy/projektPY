import os
import pandas as pd
from collections import Counter


def count_customers(customer_file="customer.csv"):
    try:
        if not os.path.exists(customer_file):
            return 0
        df = pd.read_csv(customer_file)
        return len(df)
    except Exception as e:
        print("Błąd przy liczeniu klientów:", e)
        return 0

def count_available_drugs(drug_file="drugs.xlsx"):
    try:
        if not os.path.exists(drug_file):
            return 0
        df = pd.read_excel(drug_file)
        return df["Stock"].sum()
    except Exception as e:
        print("Błąd przy liczeniu leków:", e)
        return 0

def analyze_purchases(database_folder="DATABASE"):
    try:
        if not os.path.exists(database_folder):
            return 0, 0, 0

        purchase_counts = []
        for file in os.listdir(database_folder):
            if file.endswith(".txt"):
                path = os.path.join(database_folder, file)
                with open(path, encoding="utf-8") as f:
                    lines = f.readlines()
                    count = sum(line.count(" x") for line in lines)
                    purchase_counts.append(count)

        if not purchase_counts:
            return 0, 0, 0

        return (
            round(sum(purchase_counts) / len(purchase_counts), 2),
            max(purchase_counts),
            min(purchase_counts)
        )
    except Exception as e:
        print("Błąd przy analizie zakupów:", e)
        return 0, 0, 0

def generate_customer_report(customer_file="customer.csv", database_folder="DATABASE", output_file="raport_klientow.xlsx"):
    import pandas as pd
    import os
    from collections import Counter

    if not os.path.exists(customer_file):
        print("Brak pliku z klientami.")
        return

    df = pd.read_csv(customer_file)
    raport_data = []

    for _, row in df.iterrows():
        customer_id = str(row["ID"])
        file_path = os.path.join(database_folder, f"{customer_id}.txt")
        purchases = 0

        if os.path.exists(file_path):
            with open(file_path, encoding="utf-8") as f:
                for line in f:
                    if "Zakupiono" in line:
                        purchases += 1

        raport_data.append({
            "ID": customer_id,
            "NAME": row.get("NAME", ""),
            "E-MAIL": row.get("E-MAIL", ""),
            "ZAKUPY": purchases
        })

    if raport_data:
        df_export = pd.DataFrame(raport_data)
        df_export.to_excel(output_file, index=False)
        print(f"Raport klientów zapisany jako {output_file}")
    else:
        print("Brak danych do zapisania.")
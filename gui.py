import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import pandas as pd
import os
from datetime import datetime

def client_window(customer_id):
    win = tk.Toplevel()
    win.title("Panel klienta")
    win.geometry("300x200")

    tk.Label(win, text=f"Zalogowano jako klient PESEL: {customer_id}").pack(pady=10)

    def buy():
        buy_window = tk.Toplevel()
        buy_window.title("Zakup leków")
        buy_window.geometry("600x500")

        ttk.Label(buy_window, text="Dostępne leki bez recepty:", font=("Arial", 12)).pack(pady=10)

        try:
            df = pd.read_excel("drugs.xlsx", dtype={"ID": str})
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie można wczytać pliku leków:\n{e}")
            buy_window.destroy()
            return

        df = df[(df["Prescription"] == "No") & (df["Stock"] > 0)].reset_index(drop=True)

        if df.empty:
            messagebox.showinfo("Brak leków", "Brak dostępnych leków bez recepty.")
            buy_window.destroy()
            return

        entries = []

        frame = ttk.Frame(buy_window)
        frame.pack()

        ttk.Label(frame, text="Nazwa", width=20).grid(row=0, column=0)
        ttk.Label(frame, text="Cena", width=10).grid(row=0, column=1)
        ttk.Label(frame, text="Dostępne", width=10).grid(row=0, column=2)
        ttk.Label(frame, text="Ilość", width=10).grid(row=0, column=3)

        for idx, row in df.iterrows():
            ttk.Label(frame, text=row["Name"]).grid(row=idx+1, column=0)
            ttk.Label(frame, text=f'{row["Price"]:.2f} zł').grid(row=idx+1, column=1)
            ttk.Label(frame, text=row["Stock"]).grid(row=idx+1, column=2)
            qty = tk.Entry(frame, width=5)
            qty.grid(row=idx+1, column=3)
            entries.append((row, qty))

        def confirm_purchase():
            purchases = []
            updated = False

            for r, entry in entries:
                try:
                    qty = int(entry.get()) if entry.get() else 0
                except ValueError:
                    messagebox.showerror("Błąd", f"Niepoprawna ilość dla leku {r['Name']}")
                    return

                if qty < 0:
                    messagebox.showerror("Błąd", f"Ilość nie może być ujemna ({r['Name']})")
                    return
                if qty > r["Stock"]:
                    messagebox.showerror("Błąd", f"Brak wystarczającej ilości leku {r['Name']}")
                    return
                if qty > 0:
                    purchases.append((r["ID"], r["Name"], qty, r["Price"]))
                    df.loc[df["ID"] == r["ID"], "Stock"] -= qty
                    updated = True

            if not updated:
                messagebox.showinfo("Brak zakupu", "Nie wybrano żadnych leków.")
                return

            zakupy_txt = "\n".join([f"{n} x{q} ({p:.2f} zł)" for _, n, q, p in purchases])
            total = sum(q * p for _, _, q, p in purchases)

            with open(f"DATABASE/{customer_id}.txt", "a", encoding="utf-8") as f:
                f.write(f"\nZakupiono: {', '.join([f'{n} x{q}' for _, n, q, _ in purchases])} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

            df_all = pd.read_excel("drugs.xlsx", dtype={"ID": str})
            for _, row in df.iterrows():
                df_all.loc[df_all["ID"] == row["ID"], "Stock"] = row["Stock"]
            df_all.to_excel("drugs.xlsx", index=False)

            messagebox.showinfo("Sukces", f"Zakup zrealizowany!\n\n{zakupy_txt}\n\nSuma: {total:.2f} zł")
            buy_window.destroy()

        ttk.Button(buy_window, text="Kupuję", command=confirm_purchase).pack(pady=15)
        ttk.Button(buy_window, text="Anuluj", command=buy_window.destroy).pack()

    tk.Button(win, text="Zakup leków", command=buy).pack(pady=5)
    tk.Button(win, text="Wyloguj", command=win.destroy).pack(pady=5)

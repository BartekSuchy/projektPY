import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import pandas as pd
import os
from stats import generate_customer_report

def open_admin_panel():
    window = tk.Toplevel()
    window.title("Panel administratora")
    window.geometry("700x550")

    ttk.Label(window, text="Panel administratora", font=("Arial", 16)).pack(pady=10)

    tree = ttk.Treeview(window, columns=("ID", "Name", "Price", "Prescription", "Stock"), show="headings")
    for col in ("ID", "Name", "Price", "Prescription", "Stock"):
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.pack(pady=10, fill="both", expand=True)

    def load_drugs():
        tree.delete(*tree.get_children())
        try:
            df = pd.read_excel("drugs.xlsx", dtype={"ID": str})
            for _, row in df.iterrows():
                tree.insert("", "end", values=(
                    row["ID"], row["Name"], f'{row["Price"]:.2f}', row["Prescription"], row["Stock"]
                ))
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie można wczytać leków: {e}")

    def add_drug():
        if hasattr(window, "add_window") and window.add_window.winfo_exists():
            window.add_window.lift()
            return

        def submit():
            try:
                drug_id = entry_id.get()
                name = entry_name.get()
                price = float(entry_price.get())
                presc = "Yes" if var_presc.get() else "No"
                stock = int(entry_stock.get())

                if not os.path.exists("drugs.xlsx"):
                    df = pd.DataFrame(columns=["ID", "Name", "Price", "Prescription", "Stock"])
                else:
                    df = pd.read_excel("drugs.xlsx", dtype={"ID": str})

                if drug_id in df["ID"].astype(str).values:
                    messagebox.showerror("Błąd", "Lek o tym ID już istnieje.")
                    return

                new_row = pd.DataFrame([{
                    "ID": drug_id,
                    "Name": name,
                    "Price": price,
                    "Prescription": presc,
                    "Stock": stock
                }])

                df = pd.concat([df, new_row], ignore_index=True)
                df.to_excel("drugs.xlsx", index=False)
                messagebox.showinfo("Sukces", "Lek dodany.")
                add_win.destroy()
                load_drugs()
            except Exception as e:
                messagebox.showerror("Błąd", str(e))

        window.add_window = tk.Toplevel(window)
        add_win = window.add_window
        add_win.title("Dodaj lek")
        add_win.geometry("300x300")

        tk.Label(add_win, text="ID:").pack()
        entry_id = tk.Entry(add_win)
        entry_id.pack()

        tk.Label(add_win, text="Nazwa:").pack()
        entry_name = tk.Entry(add_win)
        entry_name.pack()

        tk.Label(add_win, text="Cena:").pack()
        entry_price = tk.Entry(add_win)
        entry_price.pack()

        tk.Label(add_win, text="Na receptę?").pack()
        var_presc = tk.BooleanVar()
        tk.Checkbutton(add_win, text="Tak", variable=var_presc).pack()

        tk.Label(add_win, text="Ilość:").pack()
        entry_stock = tk.Entry(add_win)
        entry_stock.pack()

        tk.Button(add_win, text="Dodaj lek", command=submit).pack(pady=10)

    def remove_selected():
        if hasattr(window, "removal_in_progress") and window.removal_in_progress:
            return

        window.removal_in_progress = True
        try:
            selected = tree.selection()
            if not selected:
                messagebox.showinfo("Uwaga", "Zaznacz lek do usunięcia.")
                return
            item = tree.item(selected[0])
            drug_id = item["values"][0]

            df = pd.read_excel("drugs.xlsx", dtype={"ID": str})
            df = df[df["ID"] != drug_id]
            df.to_excel("drugs.xlsx", index=False)
            messagebox.showinfo("Usunięto", f"Lek {drug_id} został usunięty.")
            load_drugs()
        except Exception as e:
            messagebox.showerror("Błąd", str(e))
        finally:
            window.removal_in_progress = False

    def export_report():
        generate_customer_report()
        messagebox.showinfo("Eksport", "Raport klientów zapisany jako raport_klientow.xlsx")

    button_frame = ttk.Frame(window)
    button_frame.pack(pady=10)

    ttk.Button(button_frame, text="Dodaj lek", command=add_drug).grid(row=0, column=0, padx=5)
    ttk.Button(button_frame, text="Usuń zaznaczony lek", command=remove_selected).grid(row=0, column=1, padx=5)
    ttk.Button(button_frame, text="Eksportuj raport klientów", command=export_report).grid(row=0, column=2, padx=5)
    ttk.Button(button_frame, text="Odśwież", command=load_drugs).grid(row=0, column=3, padx=5)
    ttk.Button(button_frame, text="Wyloguj", command=window.destroy).grid(row=0, column=4, padx=5)

    load_drugs()

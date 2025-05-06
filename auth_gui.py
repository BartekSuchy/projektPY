import tkinter as tk
from tkinter import messagebox

def login_gui(callback_client, callback_admin):
    def submit_client():
        user_id = entry_user.get().strip()
        if len(user_id) != 11 or not user_id.isdigit():
            messagebox.showerror("Błąd", "PESEL musi mieć dokładnie 11 cyfr.")
            return
        login_window.destroy()
        callback_client(user_id)

    def submit_admin():
        login = entry_user.get().strip()
        password = entry_pass.get().strip()
        if login == "admin" and password == "admin123":
            login_window.destroy()
            callback_admin()
        else:
            messagebox.showerror("Błąd", "Nieprawidłowe dane administratora.")

    login_window = tk.Toplevel() if tk._default_root else tk.Tk()
    login_window.title("Logowanie")
    login_window.geometry("350x200")

    tk.Label(login_window, text="PESEL (klient) lub login (admin):").pack(pady=5)
    entry_user = tk.Entry(login_window)
    entry_user.pack(pady=5)

    tk.Label(login_window, text="Hasło (admin):").pack()
    entry_pass = tk.Entry(login_window, show="*")
    entry_pass.pack(pady=5)

    btn_frame = tk.Frame(login_window)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Zaloguj jako klient", command=submit_client).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Zaloguj jako administrator", command=submit_admin).grid(row=0, column=1, padx=5)

    login_window.grab_set()
    login_window.mainloop()

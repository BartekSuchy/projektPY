import tkinter as tk
from auth_gui import login_gui
from gui_admin import open_admin_panel
from gui import client_window

def start_app():
    def handle_login():
        def on_client_login(user_id):
            client_window(user_id)

        def on_admin_login():
            open_admin_panel()

        login_gui(callback_client=on_client_login, callback_admin=on_admin_login)

    root = tk.Tk()
    root.title("Apteka Online - Start")
    root.geometry("350x200")

    tk.Label(root, text="Witaj w systemie apteki!", font=("Arial", 14)).pack(pady=20)
    tk.Button(root, text="Zaloguj się", width=20, command=handle_login).pack(pady=10)
    tk.Button(root, text="Zamknij", width=20, command=root.destroy).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    start_app()

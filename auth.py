from datetime import datetime
import os

def login(log_file="login_log.txt"):
    print("=== LOGOWANIE ===")
    user_type = input("Zaloguj się jako (admin / klient): ").strip().lower()

    if user_type == "admin":
        username = input("Login: ").strip()
        password = input("Hasło: ").strip()
        if username == "admin" and password == "admin123":
            log_login("admin", username, log_file)
            print("✅ Zalogowano jako administrator.")
            return "admin", None
        else:
            print("❌ Niepoprawny login lub hasło.")
            return None, None

    elif user_type == "klient":
        try:
            user_id = int(input("Podaj swoje ID klienta: "))
            log_login("klient", user_id, log_file)
            return "client", user_id
        except ValueError:
            print("❌ Niepoprawny ID.")
            return None, None
    else:
        print("❌ Nieznany typ użytkownika.")
        return None, None

def log_login(user_type, identifier, log_file):
    """
    Zapisuje informację o logowaniu do pliku tekstowego.
    """
    try:
        os.makedirs(os.path.dirname(log_file), exist_ok=True) if os.path.dirname(log_file) else None
        with open(log_file, "a", encoding="utf-8") as f:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{now} | {user_type.upper()} | {identifier}\n")
    except Exception as e:
        print("❌ Błąd zapisu logu logowania:", e)
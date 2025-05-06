from drug_manager import add_drug, remove_drug
from customer_manager import register_customer, remove_customer, purchase_drugs, update_customer
from stats import count_customers, count_available_drugs, analyze_purchases, generate_customer_report
from auth import login
from stats import generate_customer_report

def __main__():
    user_type, user_id = login()
    if user_type is None:
        return

    if user_type == "admin":
        while True:
            print("\nADMIN MENU")
            print("1 - Dodaj nowy lek")
            print("2 - Usuń lek")
            print("3 - Zarejestruj nowego klienta")
            print("4 - Usuń klienta")
            print("5 - Zakup leków (testowo jako klient)")
            print("6 - Statystyki systemu")
            print("7 - Eksportuj raport klientów do .xlsx")
            print("8 - Zaktualizuj dane klienta")
            print("0 - Wyloguj")

            choice = input("Wybierz opcję: ")

            if choice == "1":
                try:
                    drug_id = int(input("ID leku: "))
                    name = input("Nazwa leku: ")
                    price = float(input("Cena: "))
                    prescription = input("Czy na receptę? (tak/nie): ").lower() == "tak"
                    stock = int(input("Ilość: "))
                    add_drug(drug_id, name, price, prescription, stock)
                except ValueError:
                    print("❌ Błąd danych.")
            elif choice == "2":
                ident = input("ID lub nazwa leku: ")
                try:
                    ident = int(ident)
                except ValueError:
                    pass
                remove_drug(ident)
            elif choice == "3":
                register_customer()
            elif choice == "4":
                ident = input("Podaj ID klienta do usunięcia: ")
                try:
                    ident = int(ident)
                    remove_customer(ident)
                except ValueError:
                    print("❌ Podano nieprawidłowe ID.")
            elif choice == "5":
                try:
                    test_id = int(input("Podaj ID klienta: "))
                    purchase_drugs(test_id)
                except ValueError:
                    print("❌ Nieprawidłowy ID.")
            elif choice == "6":
                total_clients = count_customers()
                total_stock = count_available_drugs()
                avg, max_, min_ = analyze_purchases()
                print(f"\n📊 Statystyki:")
                print(f"🧑‍💼 Klientów: {total_clients}")
                print(f"💊 Leki dostępne: {total_stock}")
                print(f"🧾 Śr. zakupy: {avg}, Max: {max_}, Min: {min_}")
            elif choice == "7":
                generate_customer_report()
            elif choice == "8":
                update_customer()
            elif choice == "0":
                print("Wylogowano.")
                break
            else:
                print("Nieznana opcja.")

    elif user_type == "client":
        while True:
            print("\nKLIENT MENU")
            print("1 - Zakup leków")
            print("0 - Wyloguj")

            choice = input("Wybierz opcję: ")
            if choice == "1":
                purchase_drugs(user_id)
            elif choice == "0":
                print("Wylogowano.")
                break
            else:
                print("Nieznana opcja.")


if __name__ == "__main__":
    __main__()
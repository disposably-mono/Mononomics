import json

# Finance Tracker
# disposably-mono

# =========================
# CONFIGURATION & CONSTANTS
# =========================

INITIAL_BALANCE = 0.0
USERNAME = "Mono"
PASSWORD = "122876"
TRANSACTIONS = []
DATA_FILE = "data.json"

# ==============
# JSON FUNCTIONS
# ==============


def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
            return data["balance"], data["transactions"]
    except (FileNotFoundError, json.JSONDecodeError):
        return INITIAL_BALANCE, []


def save_data(balance, transactions):
    data = {"balance": balance, "transactions": transactions}
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


# ========================
# AUTHENTICATION FUNCTIONS
# ========================


def authenticate_user(username, password):
    login_username = str(input("What is your username? "))
    login_password = str(input("What is your password "))

    if username == login_username and password == login_password:
        print("Login successful!")
        return True
    elif username != login_username or password != login_password:
        print("Authentication failed!")
        return False


# ===================
# FINANCIAL FUNCTIONS
# ===================


def view_balance(balance):
    print("Your currrent balance is: ", balance)
    return balance


def view_transactions():
    for transaction in TRANSACTIONS:
        print(transaction)


def process_income(balance):
    income = float(input("How much did you earn today: "))
    description = str(input("Enter a short description: "))

    balance = balance + income
    transaction_type = "income"

    transaction = {
        "transaction_type": transaction_type,
        "amount": income,
        "description": description,
    }

    TRANSACTIONS.append(transaction)

    print("Your updated balance is: ", balance)
    return balance


def process_expense(balance):
    expense = float(input("How much did you spend today: "))
    description = str(input("Enter a short description: "))

    balance = balance - expense
    transaction_type = "expense"

    transaction = {
        "transaction_type": transaction_type,
        "amount": expense,
        "description": description,
    }

    TRANSACTIONS.append(transaction)

    print("Your updated balance is: ", balance)
    return balance


# ===================
# INTERFACE FUNCTIONS
# ===================


def display_menu():
    print("==Finance Tracker==")
    print("1. Check Current Balance")
    print("2. Add Income")
    print("3. Add Expense")
    print("4. Check Transactions")
    print("5. Exit")


# ======================
# MAIN APPLICATION LOGIC
# ======================


def main():
    login_successful = authenticate_user(USERNAME, PASSWORD)
    balance, transactions = load_data()

    global TRANSACTIONS
    TRANSACTIONS = transactions

    while not login_successful:
        login_successful = authenticate_user(USERNAME, PASSWORD)

    while True:
        display_menu()

        choice = input("What would you like to do?")

        if choice == "1":
            view_balance(balance)
        elif choice == "2":
            balance = process_income(balance)
            save_data(balance, TRANSACTIONS)
        elif choice == "3":
            balance = process_expense(balance)
            save_data(balance, TRANSACTIONS)
        elif choice == "4":
            view_transactions()
        elif choice == "5":
            save_data(balance, TRANSACTIONS)
            print("Finances tracked successfully, stay wealthy!")
            break


if __name__ == "__main__":
    main()

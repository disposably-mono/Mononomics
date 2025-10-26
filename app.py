import json

# Monomonics Finance Tracker
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
    login_password = str(input("What is your password? "))

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
    print("Your current balance is:", balance)
    return balance


def view_transactions():
    for i, transaction in enumerate(TRANSACTIONS, start=1):
        print(f"{i}. {transaction}")


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

    print("Your updated balance is:", balance)
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

    print("Your updated balance is:", balance)
    return balance


def remove_transaction(balance):
    view_transactions()

    target_id = int(
        input("Enter the ID number of the transaction you want to remove: ")
    )
    transaction = TRANSACTIONS[target_id - 1]

    if transaction["transaction_type"] == "income":
        balance -= transaction["amount"]
    if transaction["transaction_type"] == "expense":
        balance += transaction["amount"]

    print(f"Removing {transaction}...")
    TRANSACTIONS.pop(target_id - 1)

    print("Your updated balance is:", balance)
    return balance


def update_transaction(balance):
    view_transactions()

    target_id = int(
        input("Enter the ID number of the transaction you want to update: ")
    )
    transaction = TRANSACTIONS[target_id - 1]

    if transaction["transaction_type"] == "income":
        balance -= transaction["amount"]
    if transaction["transaction_type"] == "expense":
        balance += transaction["amount"]

    print(f"Updating {transaction}...")
    TRANSACTIONS.pop(target_id - 1)

    new_type = input("Is this an income or expense? ").lower().strip()
    new_amount = float(input("Enter the new amount: "))
    new_description = input("Enter a short description: ")

    if new_type == "income":
        balance += new_amount
    elif new_type == "expense":
        balance -= new_amount
    else:
        print("Invalid transaction type. No changes made.")
        return balance

    new_transaction = {
        "transaction_type": new_type,
        "amount": new_amount,
        "description": new_description,
    }

    TRANSACTIONS.insert(target_id - 1, new_transaction)

    print("Your updated balance is:", balance)
    return balance


# ===================
# INTERFACE FUNCTIONS
# ===================


def display_menu():
    print("== Finance Tracker ==")
    print("1. Check Current Balance")
    print("2. Add Income")
    print("3. Add Expense")
    print("4. Check Transactions")
    print("5. Update Transaction")
    print("6. Delete Transaction")
    print("7. Exit")


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

        choice = input("What would you like to do? ")

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
            balance = update_transaction(balance)
        elif choice == "6":
            balance = remove_transaction(balance)
        elif choice == "7":
            save_data(balance, TRANSACTIONS)
            print("Finances tracked successfully. Stay wealthy!")
            break


if __name__ == "__main__":
    main()

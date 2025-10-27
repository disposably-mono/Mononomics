# Monomonics Finance Tracker
# disposably-monom

import json
from datetime import datetime


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
        print("No data file found or data corrupted. Starting fresh.")
        return INITIAL_BALANCE, []


def save_data(balance, transactions):
    data = {"balance": balance, "transactions": transactions}
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(data, file, indent=4)
    except OSError as e:
        print(f"Error saving data: {e}")


# ========================
# AUTHENTICATION FUNCTIONS
# ========================


def authenticate_user(username, password):
    while True:
        login_username = input("What is your username? ").strip()
        login_password = input("What is your password? ").strip()

        if not login_username or not login_password:
            print("Username and password cannot be empty.")
            continue

        if username == login_username and password == login_password:
            print("Login successful!")
            return True
        else:
            print("Authentication failed! Try again.")


# ===================
# FINANCIAL FUNCTIONS
# ===================


def view_balance(balance):
    print("Your current balance is:", balance)
    return balance


def view_transactions():
    if not TRANSACTIONS:
        print("No transactions found.")
        return

    print("\n=== Transactions ===")
    for i, t in enumerate(TRANSACTIONS, start=1):
        timestamp = t.get("timestamp", "N/A")
        print(
            f"[{i}] {t['transaction_type'].upper():<8} ₱{t['amount']:>8.2f}  —  {t['description']:<30} | {timestamp}"
        )


def process_income(balance):
    try:
        income = float(input("How much did you earn today: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return balance

    description = input("Enter a short description: ").strip()

    balance += income
    transaction = {
        "transaction_type": "income",
        "amount": income,
        "description": description,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    TRANSACTIONS.append(transaction)
    print("Income added successfully!")
    print("Your updated balance is:", balance)
    return balance


def process_expense(balance):
    try:
        expense = float(input("How much did you spend today: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return balance

    description = input("Enter a short description: ").strip()

    balance -= expense
    transaction = {
        "transaction_type": "expense",
        "amount": expense,
        "description": description,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    TRANSACTIONS.append(transaction)
    print("Expense added successfully!")
    print("Your updated balance is:", balance)
    return balance


def remove_transaction(balance):
    if not TRANSACTIONS:
        print("No transactions to remove.")
        return balance
    view_transactions()
    try:
        target_id = int(input("Enter the ID number of the transaction to remove: "))
        transaction = TRANSACTIONS[target_id - 1]
    except (ValueError, IndexError):
        print("Invalid ID. Please enter a valid transaction number.")
        return balance
    if transaction["transaction_type"] == "income":
        balance -= transaction["amount"]
    elif transaction["transaction_type"] == "expense":
        balance += transaction["amount"]

    timestamp = transaction.get("timestamp", "N/A")
    print(
        f"Removing: {transaction['transaction_type'].upper():<8} ₱{transaction['amount']:>8.2f}  —  {transaction['description']:<30} | {timestamp}"
    )
    TRANSACTIONS.pop(target_id - 1)
    print("Transaction removed successfully!")
    print("Your updated balance is:", balance)
    return balance


def update_transaction(balance):
    if not TRANSACTIONS:
        print("No transactions to update.")
        return balance
    view_transactions()
    try:
        target_id = int(input("Enter the ID number of the transaction to update: "))
        transaction = TRANSACTIONS[target_id - 1]
    except (ValueError, IndexError):
        print("Invalid ID. Please enter a valid transaction number.")
        return balance
    if transaction["transaction_type"] == "income":
        balance -= transaction["amount"]
    elif transaction["transaction_type"] == "expense":
        balance += transaction["amount"]

    timestamp = transaction.get("timestamp", "N/A")
    print(
        f"Updating: {transaction['transaction_type'].upper():<8} ₱{transaction['amount']:>8.2f}  —  {transaction['description']:<30} | {timestamp}"
    )
    TRANSACTIONS.pop(target_id - 1)

    new_type = input("Is this an income or expense? ").lower().strip()
    if new_type not in ["income", "expense"]:
        print("Invalid transaction type. Update cancelled.")
        TRANSACTIONS.insert(target_id - 1, transaction)
        return balance
    try:
        new_amount = float(input("Enter the new amount: "))
    except ValueError:
        print("Invalid amount. Update cancelled.")
        TRANSACTIONS.insert(target_id - 1, transaction)
        return balance
    new_description = input("Enter a short description: ").strip()
    if new_type == "income":
        balance += new_amount
    else:
        balance -= new_amount
    new_transaction = {
        "transaction_type": new_type,
        "amount": new_amount,
        "description": new_description,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    TRANSACTIONS.insert(target_id - 1, new_transaction)
    print("Transaction updated successfully!")
    print("Your updated balance is:", balance)
    return balance


# ===================
# INTERFACE FUNCTIONS
# ===================


def display_menu():
    print("\n== Mononomics Finance Tracker ==")
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
            save_data(balance, TRANSACTIONS)
        elif choice == "6":
            balance = remove_transaction(balance)
            save_data(balance, TRANSACTIONS)
        elif choice == "7":
            save_data(balance, TRANSACTIONS)
            print("Finances tracked successfully. Stay wealthy!")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram exited manually. Goodbye!")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

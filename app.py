"""
Mononomics Finance Tracker
Personal finance management for tracking income, expenses, and savings goals.
"""

import json
from datetime import datetime


# =========================
# CONFIGURATION
# =========================

INITIAL_BALANCE = 0.0
USERNAME = "Mono"
PASSWORD = "122876"
DATA_FILE = "data.json"


# =========================
# DATA PERSISTENCE
# =========================


def load_data():
    """Load balance, transactions, and savings from file."""
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
            balance = data.get("balance", INITIAL_BALANCE)
            transactions = data.get("transactions", [])
            savings = data.get("savings", [])
            return balance, transactions, savings
    except FileNotFoundError:
        print("No data file found. Starting fresh.")
        return INITIAL_BALANCE, [], []
    except json.JSONDecodeError:
        print("Data file corrupted. Starting fresh.")
        return INITIAL_BALANCE, [], []


def save_data(balance, transactions, savings):
    """Save balance, transactions, and savings to file."""
    data = {"balance": balance, "transactions": transactions, "savings": savings}
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(data, file, indent=4)
        return True
    except OSError as e:
        print(f"Error saving data: {e}")
        return False


# =========================
# INPUT HELPERS
# =========================


def get_float_input(prompt, allow_empty=False, default=None):
    """Get validated float input from user."""
    while True:
        user_input = input(prompt).strip()

        if not user_input:
            if allow_empty and default is not None:
                return default
            elif allow_empty:
                return 0.0
            print("Input cannot be empty.")
            continue

        try:
            value = float(user_input)
            if value < 0:
                print("Amount cannot be negative.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def get_int_input(prompt, min_value=None, max_value=None):
    """Get validated integer input from user."""
    while True:
        try:
            value = int(input(prompt).strip())

            if min_value is not None and value < min_value:
                print(f"Value must be at least {min_value}.")
                continue

            if max_value is not None and value > max_value:
                print(f"Value must be at most {max_value}.")
                continue

            return value
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def get_string_input(prompt, allow_empty=False, default=""):
    """Get string input from user."""
    user_input = input(prompt).strip()

    if not user_input:
        if allow_empty:
            return default
        print("Input cannot be empty.")
        return get_string_input(prompt, allow_empty, default)

    return user_input


# =========================
# AUTHENTICATION
# =========================


def authenticate_user():
    """Authenticate user with username and password."""
    print("\n=== Login Required ===")

    while True:
        login_username = input("Username: ").strip()
        login_password = input("Password: ").strip()

        if not login_username or not login_password:
            print("Username and password cannot be empty.\n")
            continue

        if login_username == USERNAME and login_password == PASSWORD:
            print("Login successful!\n")
            return True
        else:
            print("Authentication failed. Please try again.\n")


# =========================
# DISPLAY FUNCTIONS
# =========================


def display_menu():
    """Display the main menu."""
    print("\n" + "=" * 40)
    print("  Mononomics Finance Tracker")
    print("=" * 40)
    print("1.  Check Current Balance")
    print("2.  Add Income")
    print("3.  Add Expense")
    print("4.  View Transactions")
    print("5.  Update Transaction")
    print("6.  Delete Transaction")
    print("7.  Add Savings Goal")
    print("8.  Update Savings Goal")
    print("9.  Delete Savings Goal")
    print("10. View Savings Goals")
    print("11. Exit")
    print("=" * 40)


def view_balance(balance):
    """Display current balance."""
    print(f"\nYour current balance: P{balance:.2f}")


def view_transactions(transactions):
    """Display all transactions."""
    if not transactions:
        print("\nNo transactions found.")
        return

    print("\n=== Transaction History ===")
    for i, transaction in enumerate(transactions, start=1):
        trans_type = transaction["transaction_type"].upper()
        amount = transaction["amount"]
        description = transaction["description"]
        timestamp = transaction.get("timestamp", "N/A")

        print(
            f"[{i}] {trans_type:<8} P{amount:>8.2f}  —  {description:<30} | {timestamp}"
        )


def view_savings_goals(savings):
    """Display all savings goals."""
    if not savings:
        print("\nNo savings goals found.")
        return

    print("\n=== Savings Goals ===")
    for i, goal in enumerate(savings, start=1):
        name = goal["savings_goal"].upper()
        target = goal["savings_amount"]
        description = goal["savings_description"]
        progress = goal["savings_progress"]
        timestamp = goal.get("timestamp", "N/A")
        percentage = (progress / target * 100) if target > 0 else 0

        print(f"[{i}] {name:<20} P{target:>8.2f}  —  {description:<30}")
        print(f"     Progress: P{progress:.2f} ({percentage:.1f}%) | {timestamp}")


# =========================
# TRANSACTION FUNCTIONS
# =========================


def create_transaction(trans_type, amount, description):
    """Create a new transaction dictionary."""
    return {
        "transaction_type": trans_type,
        "amount": amount,
        "description": description,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def add_income(balance, transactions):
    """Add an income transaction."""
    print("\n=== Add Income ===")

    amount = get_float_input("How much did you earn: P")
    if not amount or amount == 0:
        print("Amount must be greater than zero.")
        return balance

    description = get_string_input(
        "Enter description: ", allow_empty=True, default="Income"
    )

    balance += amount
    transactions.append(create_transaction("income", amount, description))

    print("Income added successfully!")
    print(f"Updated balance: P{balance:.2f}")
    return balance


def add_expense(balance, transactions):
    """Add an expense transaction."""
    print("\n=== Add Expense ===")

    amount = get_float_input("How much did you spend: P")
    if not amount or amount == 0:
        print("Amount must be greater than zero.")
        return balance

    description = get_string_input(
        "Enter description: ", allow_empty=True, default="Expense"
    )

    balance -= amount
    transactions.append(create_transaction("expense", amount, description))

    print("Expense added successfully!")
    print(f"Updated balance: P{balance:.2f}")
    return balance


def remove_transaction(balance, transactions):
    """Remove a transaction."""
    if not transactions:
        print("\nNo transactions to remove.")
        return balance

    view_transactions(transactions)
    print()

    trans_id = get_int_input(
        "Enter transaction ID to remove: ", min_value=1, max_value=len(transactions)
    )

    transaction = transactions[trans_id - 1]

    if transaction["transaction_type"] == "income":
        balance -= transaction["amount"]
    else:
        balance += transaction["amount"]

    print(
        f"\nRemoving: {transaction['transaction_type'].upper()} - "
        f"P{transaction['amount']:.2f} - {transaction['description']}"
    )

    transactions.pop(trans_id - 1)

    print("Transaction removed successfully!")
    print(f"Updated balance: P{balance:.2f}")
    return balance


def update_transaction(balance, transactions):
    """Update an existing transaction."""
    if not transactions:
        print("\nNo transactions to update.")
        return balance

    view_transactions(transactions)
    print()

    trans_id = get_int_input(
        "Enter transaction ID to update: ", min_value=1, max_value=len(transactions)
    )

    old_transaction = transactions[trans_id - 1]

    if old_transaction["transaction_type"] == "income":
        balance -= old_transaction["amount"]
    else:
        balance += old_transaction["amount"]

    print(
        f"\nUpdating: {old_transaction['transaction_type'].upper()} - "
        f"P{old_transaction['amount']:.2f} - {old_transaction['description']}"
    )

    while True:
        trans_type = input("Type (income/expense): ").lower().strip()
        if trans_type in ["income", "expense"]:
            break
        print("Invalid type. Please enter 'income' or 'expense'.")

    amount = get_float_input("Enter new amount: P")
    if not amount or amount == 0:
        print("Amount must be greater than zero. Update cancelled.")

        if old_transaction["transaction_type"] == "income":
            balance += old_transaction["amount"]
        else:
            balance -= old_transaction["amount"]
        return balance

    description = get_string_input(
        "Enter description: ", allow_empty=True, default=old_transaction["description"]
    )

    if trans_type == "income":
        balance += amount
    else:
        balance -= amount

    transactions[trans_id - 1] = create_transaction(trans_type, amount, description)

    print("Transaction updated successfully!")
    print(f"Updated balance: P{balance:.2f}")
    return balance


# =========================
# SAVINGS FUNCTIONS
# =========================
def create_savings_goal(name, target_amount, description, progress=0.0):
    """Create a new savings goal dictionary."""
    return {
        "savings_goal": name,
        "savings_amount": target_amount,
        "savings_description": description,
        "savings_progress": progress,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def add_savings_goal(balance, transactions, savings):
    """Add a new savings goal."""
    print("\n=== Add Savings Goal ===")

    name = get_string_input("What are you saving for: ")

    target_amount = get_float_input("Target amount: P")
    if target_amount == 0:
        print("Target amount must be greater than zero.")
        return balance

    description = get_string_input(
        "Enter description: ", allow_empty=True, default=name
    )

    initial_progress = get_float_input(
        "Initial savings amount (press Enter for 0): P", allow_empty=True, default=0.0
    )

    if initial_progress > balance:
        print(f"Insufficient balance. Available: P{balance:.2f}")
        return balance

    balance -= initial_progress
    savings.append(
        create_savings_goal(name, target_amount, description, initial_progress)
    )

    if initial_progress > 0:
        transactions.append(
            create_transaction(
                "expense", initial_progress, f"Initial allocation to savings: {name}"
            )
        )

    print("Savings goal added successfully!")
    print(f"Updated balance: P{balance:.2f}")
    return balance


def update_savings_goal(balance, transactions, savings):
    """Update an existing savings goal."""
    if not savings:
        print("\nNo savings goals to update.")
        return balance

    view_savings_goals(savings)
    print()

    goal_id = get_int_input(
        "Enter savings goal ID to update: ", min_value=1, max_value=len(savings)
    )

    goal = savings[goal_id - 1]
    old_progress = goal["savings_progress"]

    print(f"\nCurrent goal: {goal['savings_goal']}")
    print(f"Target: P{goal['savings_amount']:.2f}")
    print(f"Progress: P{old_progress:.2f}\n")

    name = input(f"New name (press Enter to keep '{goal['savings_goal']}'): ").strip()
    if not name:
        name = goal["savings_goal"]

    target_amount = get_float_input(
        f"New target (press Enter to keep P{goal['savings_amount']:.2f}): P",
        allow_empty=True,
        default=goal["savings_amount"],
    )

    new_progress = get_float_input(
        f"New progress (press Enter to keep P{old_progress:.2f}): P",
        allow_empty=True,
        default=old_progress,
    )

    progress_diff = new_progress - old_progress

    if progress_diff > balance:
        print(f"Insufficient balance. Available: P{balance:.2f}")
        return balance

    description = input("New description (press Enter to keep): ").strip()
    if not description:
        description = goal["savings_description"]

    balance -= progress_diff

    if progress_diff != 0:
        trans_type = "expense" if progress_diff > 0 else "income"
        transactions.append(
            create_transaction(
                trans_type,
                abs(progress_diff),
                f"Progress update for: {goal['savings_goal']}",
            )
        )

    savings[goal_id - 1] = create_savings_goal(
        name, target_amount, description, new_progress
    )

    print("Savings goal updated successfully!")
    print(f"Updated balance: P{balance:.2f}")
    return balance


def remove_savings_goal(balance, transactions, savings):
    """Remove a savings goal and refund the saved amount."""
    if not savings:
        print("\nNo savings goals to delete.")
        return balance

    view_savings_goals(savings)
    print()

    goal_id = get_int_input(
        "Enter savings goal ID to delete: ", min_value=1, max_value=len(savings)
    )

    goal = savings.pop(goal_id - 1)
    refund = goal["savings_progress"]

    # Refund saved amount
    balance += refund

    if refund > 0:
        transactions.append(
            create_transaction(
                "income", refund, f"Refund from deleted savings: {goal['savings_goal']}"
            )
        )

    print(f"Savings goal '{goal['savings_goal']}' deleted!")
    print(f"Refunded: P{refund:.2f}")
    print(f"Updated balance: P{balance:.2f}")
    return balance


# =========================
# MAIN PROGRAM
# =========================


def main():
    """Main program loop."""
    print("=" * 40)
    print("  Welcome to Mononomics Finance Tracker!")
    print("=" * 40)

    authenticate_user()

    balance, transactions, savings = load_data()

    while True:
        display_menu()
        choice = input("\nWhat would you like to do? ").strip()

        if choice == "1":
            view_balance(balance)

        elif choice == "2":
            balance = add_income(balance, transactions)
            save_data(balance, transactions, savings)

        elif choice == "3":
            balance = add_expense(balance, transactions)
            save_data(balance, transactions, savings)

        elif choice == "4":
            view_transactions(transactions)

        elif choice == "5":
            balance = update_transaction(balance, transactions)
            save_data(balance, transactions, savings)

        elif choice == "6":
            balance = remove_transaction(balance, transactions)
            save_data(balance, transactions, savings)

        elif choice == "7":
            balance = add_savings_goal(balance, transactions, savings)
            save_data(balance, transactions, savings)

        elif choice == "8":
            balance = update_savings_goal(balance, transactions, savings)
            save_data(balance, transactions, savings)

        elif choice == "9":
            balance = remove_savings_goal(balance, transactions, savings)
            save_data(balance, transactions, savings)

        elif choice == "10":
            view_savings_goals(savings)

        elif choice == "11":
            save_data(balance, transactions, savings)
            print("\nData saved successfully!")
            print("Stay wealthy!")
            break

        else:
            print("Invalid choice. Please enter a number from the menu.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Goodbye!")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        print("Please report this issue if it persists.")

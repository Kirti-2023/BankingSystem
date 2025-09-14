import os
import csv
import hashlib
from datetime import datetime

# ===============================
# File names used in the project
# ===============================
ACCOUNTS_FILE = "accounts.txt"       # Stores account details
TRANSACTIONS_FILE = "transactions.txt"  # Stores transaction logs


# ===============================
# Utility Functions
# ===============================
def hash_password(password):
    """Convert a plain password into a SHA-256 hash for security."""
    return hashlib.sha256(password.encode()).hexdigest()


def generate_account_number():
    """Generate unique account number by checking last account in accounts.txt"""
    if not os.path.exists(ACCOUNTS_FILE) or os.stat(ACCOUNTS_FILE).st_size == 0:
        return 100001  # first account number
    else:
        with open(ACCOUNTS_FILE, "r") as f:
            lines = f.readlines()
            last_account = int(lines[-1].split(",")[0])  # take last account number
            return last_account + 1


def log_transaction(account_no, txn_type, amount, target_account=None):
    """Record a transaction in transactions.txt with timestamp."""
    with open(TRANSACTIONS_FILE, "a", newline='') as f:
        writer = csv.writer(f)
        if target_account:  # if transfer, log with target account
            writer.writerow([account_no, f"{txn_type} to {target_account}", amount, datetime.now()])
        else:  # deposit/withdraw
            writer.writerow([account_no, txn_type, amount, datetime.now()])


# ===============================
# Account Class
# ===============================
class Account:
    def __init__(self, account_no, name, password, balance, acc_type):
        """Initialize an account object."""
        self.account_no = account_no
        self.name = name
        self.password = password  # hashed password
        self.balance = float(balance)
        self.acc_type = acc_type

    def deposit(self, amount):
        """Deposit money into the account."""
        self.balance += amount
        log_transaction(self.account_no, "Deposit", amount)

    def withdraw(self, amount):
        """Withdraw money from the account if sufficient balance exists."""
        if amount > self.balance:
            print("❌ Insufficient balance.")
            return False
        self.balance -= amount
        log_transaction(self.account_no, "Withdrawal", amount)
        return True

    def transfer(self, target_account, amount):
        """Transfer money to another account."""
        if amount > self.balance:
            print("❌ Insufficient balance for transfer.")
            return False
        # Deduct from sender
        self.balance -= amount
        # Add to receiver
        target_account.balance += amount
        # Log both transactions
        log_transaction(self.account_no, "Transfer", amount, target_account.account_no)
        log_transaction(target_account.account_no, "Received", amount, self.account_no)
        return True


# ===============================
# Banking System
# ===============================
class BankingSystem:
    def __init__(self):
        """Initialize banking system and create files if not present."""
        self.logged_in_account = None
        for file in [ACCOUNTS_FILE, TRANSACTIONS_FILE]:
            if not os.path.exists(file):
                with open(file, "w") as f:
                    pass  # create empty file

    # ---------- Account Creation ----------
    def create_account(self):
        """Create a new account with user details."""
        name = input("Enter your name: ")
        password = input("Set a password: ")
        acc_type = input("Enter account type (Savings/Current): ")
        deposit = float(input("Enter initial deposit: "))

        account_no = generate_account_number()
        hashed_password = hash_password(password)

        # Save to accounts.txt
        with open(ACCOUNTS_FILE, "a") as f:
            f.write(f"{account_no},{name},{hashed_password},{deposit},{acc_type}\n")

        print(f"✅ Account created successfully! Your account number is {account_no}")

    # ---------- Login ----------
    def login(self):
        """Login to an existing account."""
        acc_no = input("Enter account number: ")
        password = input("Enter password: ")
        hashed_password = hash_password(password)

        with open(ACCOUNTS_FILE, "r") as f:
            for line in f:
                account_no, name, pwd, balance, acc_type = line.strip().split(",")
                if account_no == acc_no and pwd == hashed_password:
                    # Create an Account object for the logged-in user
                    self.logged_in_account = Account(account_no, name, pwd, balance, acc_type)
                    print(f"✅ Welcome {name}!")
                    return True

        print("❌ Invalid account number or password.")
        return False

    # ---------- Helper Methods ----------
    def save_accounts(self, accounts):
        """Save all accounts back to accounts.txt"""
        with open(ACCOUNTS_FILE, "w") as f:
            for acc in accounts:
                f.write(f"{acc.account_no},{acc.name},{acc.password},{acc.balance},{acc.acc_type}\n")

    def get_all_accounts(self):
        """Read all accounts from accounts.txt into a list of Account objects"""
        accounts = []
        with open(ACCOUNTS_FILE, "r") as f:
            for line in f:
                if line.strip():
                    account_no, name, pwd, balance, acc_type = line.strip().split(",")
                    accounts.append(Account(account_no, name, pwd, balance, acc_type))
        return accounts

    def update_account(self):
        """Update the logged-in account details in accounts.txt"""
        accounts = self.get_all_accounts()
        for acc in accounts:
            if acc.account_no == self.logged_in_account.account_no:
                acc.balance = self.logged_in_account.balance
        self.save_accounts(accounts)

    # ---------- Transaction Operations ----------
    def deposit(self):
        """Deposit money into the logged-in account"""
        amount = float(input("Enter deposit amount: "))
        self.logged_in_account.deposit(amount)
        self.update_account()
        print("✅ Deposit successful!")

    def withdraw(self):
        """Withdraw money from the logged-in account"""
        amount = float(input("Enter withdrawal amount: "))
        if self.logged_in_account.withdraw(amount):
            self.update_account()
            print("✅ Withdrawal successful!")

    def check_balance(self):
        """Display current balance of the logged-in account"""
        print(f"💰 Current Balance: {self.logged_in_account.balance}")

    def transfer(self):
        """Transfer money from logged-in account to another account"""
        target_no = input("Enter target account number: ")
        amount = float(input("Enter transfer amount: "))

        accounts = self.get_all_accounts()
        target_account = None
        for acc in accounts:
            if acc.account_no == target_no:
                target_account = acc
                break

        if target_account:
            if self.logged_in_account.transfer(target_account, amount):
                self.update_account()
                self.save_accounts(accounts)
                print("✅ Transfer successful!")
        else:
            print("❌ Target account not found.")

    # ---------- Password Management ----------
    def change_password(self):
        """Change the password of the logged-in account"""
        old_pwd = input("Enter old password: ")
        if hash_password(old_pwd) != self.logged_in_account.password:
            print("❌ Incorrect old password.")
            return
        new_pwd = input("Enter new password: ")
        self.logged_in_account.password = hash_password(new_pwd)

        accounts = self.get_all_accounts()
        for acc in accounts:
            if acc.account_no == self.logged_in_account.account_no:
                acc.password = self.logged_in_account.password
        self.save_accounts(accounts)
        print("✅ Password changed successfully!")

    # ---------- Close Account ----------
    def close_account(self):
        """Close the logged-in account"""
        confirm = input("Are you sure you want to close your account? (yes/no): ")
        if confirm.lower() == "yes":
            accounts = self.get_all_accounts()
            accounts = [acc for acc in accounts if acc.account_no != self.logged_in_account.account_no]
            self.save_accounts(accounts)
            print("✅ Account closed successfully.")
            self.logged_in_account = None

    # ---------- Main Menu ----------
    def main_menu(self):
        """Main entry point for users"""
        while True:
            print("\n===== Banking System =====")
            print("1. Create Account")
            print("2. Login")
            print("3. Exit")

            choice = input("Enter choice: ")

            if choice == "1":
                self.create_account()
            elif choice == "2":
                if self.login():
                    self.account_menu()
            elif choice == "3":
                print("👋 Thank you for using the Banking System.")
                break
            else:
                print("❌ Invalid choice. Try again.")

    # ---------- Account Menu ----------
    def account_menu(self):
        """Menu after login"""
        while True:
            print("\n===== Account Menu =====")
            print("1. Deposit")
            print("2. Withdraw")
            print("3. Balance Inquiry")
            print("4. Fund Transfer")
            print("5. Change Password")
            print("6. Close Account")
            print("7. Logout")

            choice = input("Enter choice: ")

            if choice == "1":
                self.deposit()
            elif choice == "2":
                self.withdraw()
            elif choice == "3":
                self.check_balance()
            elif choice == "4":
                self.transfer()
            elif choice == "5":
                self.change_password()
            elif choice == "6":
                self.close_account()
                break
            elif choice == "7":
                print("👋 Logged out.")
                break
            else:
                print("❌ Invalid choice. Try again.")


# ===============================
# Run Program
# ===============================
if __name__ == "__main__":
    system = BankingSystem()
    system.main_menu()

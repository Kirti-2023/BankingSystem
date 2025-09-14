# 🏦 Banking System in Python

A simple **console-based banking system** implemented in Python using **txt file handling**.  
This project allows users to create accounts, log in, and perform various banking operations like deposits, withdrawals, transfers, and checking transaction history.  

---

## ✨ Features
- 👤 **Account Management**
  - Create a new account (Savings/Current)
  - Login/Logout functionality  
- 💰 **Transactions**
  - Deposit money
  - Withdraw money (with balance check)
  - Transfer between accounts  
- 📊 **Banking Services**
  - Check account balance
  - View transaction history  
- 📂 **Data Persistence**
  - Accounts stored in `accounts.txt`  
  - Transactions stored in `transactions.txt`  

---

## 📂 Project Structure
BankingSystem/
│── banking_system.py # Main Python program
│── accounts.txt # Stores account details (auto-generated)
│── transactions.txt # Stores transaction records (auto-generated)
│── README.md # Project documentation

## 🚀 How to Run

1. **Clone this repository**:
   ```bash
   git clone https://github.com/your-username/BankingSystem.git
   
2. **Navigate into the project folder**:
   ```bash
   cd BankingSystem
   
3. **Run the program**:
    ```bash
   python banking_system.py

## ⚙ Requirements

Python 3.8+

No external libraries required (uses only built-in modules: os, csv, datetime

## 📜 Usage Flow
### 🔑 Main Menu (before login)

Create Account

Login

Exit

### 📲 Logged-In Menu (after login)

Deposit

Withdraw

Transfer

Check Balance

View Transactions

Logout

## 🗂 Data Storage

### 📌 `accounts.csv`
This file stores account details in the following format:

account_no, name, password, balance, acc_type
 
**Example:**
100001,kirti,03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4,14000.0,Saving

### 📌 `transactions.csv`
This file stores all transactions in the following format:

date_time, account_no, type, amount, target_acc_no

**Example:**
100001,Deposit,7000.0,2025-09-14 14:46:06.223209


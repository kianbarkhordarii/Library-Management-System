import pandas as pd
from getpass import getpass
import os

# File names
USER_FILE = 'users.xlsx'
BOOK_FILE = 'books.xlsx'
LOAN_FILE = 'loans.xlsx'

# Initialize files if they don't exist
def init_db():
    if not os.path.exists(USER_FILE):
        pd.DataFrame(columns=['name', 'national_id', 'phone']).to_excel(USER_FILE, index=False)
    if not os.path.exists(BOOK_FILE):
        pd.DataFrame(columns=['book_code', 'title', 'quantity']).to_excel(BOOK_FILE, index=False)
    if not os.path.exists(LOAN_FILE):
        pd.DataFrame(columns=['member_name', 'book_title', 'issue_date', 'return_date']).to_excel(LOAN_FILE, index=False)

def admin_login():
    username = input("Username: ")
    password = getpass("Password: ")
    return username == "kian" and password == "123"

def add_member():
    df = pd.read_excel(USER_FILE)
    name = input("Name: ")
    national_id = input("National ID: ")
    phone = input("Phone: ")
    df.loc[len(df)] = [name, national_id, phone]
    df.to_excel(USER_FILE, index=False)
    print("✅ Member added successfully.")

def add_book():
    df = pd.read_excel(BOOK_FILE)
    code = input("Book Code: ")
    title = input("Title: ")
    qty = int(input("Quantity: "))
    df.loc[len(df)] = [code, title, qty]
    df.to_excel(BOOK_FILE, index=False)
    print("✅ Book added successfully.")

def issue_book():
    member_name = input("Member Name: ").strip()
    book_code = input("Book Code: ").strip()
    
    # Validate User
    df_users = pd.read_excel(USER_FILE)
    if member_name not in df_users['name'].astype(str).values:
        print("❌ Member not found.")
        return

    # Validate Book
    df_books = pd.read_excel(BOOK_FILE)
    book_idx = df_books.index[df_books['book_code'].astype(str) == book_code]
    
    if book_idx.empty:
        print("❌ Book not found.")
        return
    if df_books.at[book_idx[0], 'quantity'] <= 0:
        print("❌ Out of stock.")
        return

    # Process Loan
    issue_date = input("Issue Date (YYYY-MM-DD): ")
    return_date = input("Return Date (YYYY-MM-DD): ")
    
    # Update inventory
    df_books.at[book_idx[0], 'quantity'] -= 1
    df_books.to_excel(BOOK_FILE, index=False)

    # Record loan in a SEPARATE file (Fixed bug)
    df_loans = pd.read_excel(LOAN_FILE)
    df_loans.loc[len(df_loans)] = [member_name, df_books.at[book_idx[0], 'title'], issue_date, return_date]
    df_loans.to_excel(LOAN_FILE, index=False)
    print("✅ Book issued successfully.")

def display_status():
    df_loans = pd.read_excel(LOAN_FILE)
    print("\n📋 Current Loans:\n")
    if df_loans.empty:
        print("No active loans.")
    else:
        print(df_loans.to_string(index=False))

def main():
    init_db()
    if not admin_login():
        print("❌ Login failed.")
        return

    menu = {
        "1": ("Add Member", add_member),
        "2": ("Add Book", add_book),
        "3": ("Issue Book", issue_book),
        "4": ("View Loans", display_status),
        "0": ("Exit", exit)
    }

    while True:
        print("\n📚 Library System")
        for k, v in menu.items():
            print(f"{k}. {v[0]}")
        
        choice = input(">> ")
        if choice in menu:
            menu[choice][1]()
        else:
            print("❗ Invalid choice.")

if __name__ == "__main__":
    main()
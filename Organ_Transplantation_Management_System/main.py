import csv
import json
import hashlib
import time
import bcrypt
import os

USERS_FILE = "users.json"
DATA_FILE = "organ_data.csv"
BLOCKCHAIN_FILE = "blockchain.json"

# ---------------- UTILITY ---------------- #

def load_json(file):
    if not os.path.exists(file):
        return {}
    with open(file, "r") as f:
        return json.load(f)

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# ---------------- AUTH SYSTEM ---------------- #

def register():
    users = load_json(USERS_FILE)

    username = input("Enter username: ")
    if username in users:
        print("User already exists!")
        return

    password = input("Enter password: ")
    role = input("Enter role (admin/management/user): ").lower()

    if role not in ["admin", "management", "user"]:
        print("Invalid role!")
        return

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    users[username] = {
        "password": hashed,
        "role": role
    }

    save_json(USERS_FILE, users)
    print("User registered successfully!")

def login():
    users = load_json(USERS_FILE)

    username = input("Username: ")
    password = input("Password: ")

    if username in users:
        stored = users[username]["password"].encode()
        if bcrypt.checkpw(password.encode(), stored):
            print(f"Login successful! Role: {users[username]['role']}")
            return username, users[username]["role"]

    print("Invalid credentials!")
    return None, None

# ---------------- BLOCKCHAIN ---------------- #

def load_chain():
    if not os.path.exists(BLOCKCHAIN_FILE):
        return []
    with open(BLOCKCHAIN_FILE, "r") as f:
        return json.load(f)

def save_chain(chain):
    with open(BLOCKCHAIN_FILE, "w") as f:
        json.dump(chain, f, indent=4)

def generate_hash(data, prev_hash):
    text = str(data) + str(time.time()) + prev_hash
    return hashlib.sha256(text.encode()).hexdigest()

def add_block(data):
    chain = load_chain()
    prev_hash = chain[-1]["hash"] if chain else "0"

    block = {
        "index": len(chain) + 1,
        "timestamp": time.ctime(),
        "data": data,
        "previous_hash": prev_hash,
        "hash": generate_hash(data, prev_hash)
    }

    chain.append(block)
    save_chain(chain)

# ---------------- DATA ---------------- #

def add_record():
    organ = input("Organ: ")
    blood = input("Blood Group: ")
    hospital = input("Hospital: ")
    contact = input("Contact: ")
    location = input("Location: ")

    record = [organ, blood, hospital, contact, location]

    file_exists = os.path.exists(DATA_FILE)

    with open(DATA_FILE, "a", newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Organ", "Blood", "Hospital", "Contact", "Location"])
        writer.writerow(record)

    add_block(record)
    print("Record added!")

def view_records():
    if not os.path.exists(DATA_FILE):
        print("No data found!")
        return

    with open(DATA_FILE, "r") as f:
        for row in csv.reader(f):
            print(row)

def search_records():
    key = input("Enter keyword: ").lower()

    with open(DATA_FILE, "r") as f:
        for row in csv.reader(f):
            if any(key in item.lower() for item in row):
                print(row)

# ---------------- ADMIN FUNCTIONS ---------------- #

def delete_user():
    users = load_json(USERS_FILE)
    username = input("Enter username to delete: ")

    if username in users:
        del users[username]
        save_json(USERS_FILE, users)
        print("User deleted!")
    else:
        print("User not found!")

# ---------------- MENUS ---------------- #

def admin_menu():
    while True:
        print("\n--- ADMIN MENU ---")
        print("1. Add Record")
        print("2. View Records")
        print("3. Search Records")
        print("4. Delete User")
        print("5. Logout")

        ch = input("Choice: ")

        if ch == "1":
            add_record()
        elif ch == "2":
            view_records()
        elif ch == "3":
            search_records()
        elif ch == "4":
            delete_user()
        elif ch == "5":
            break

def management_menu():
    while True:
        print("\n--- MANAGEMENT MENU ---")
        print("1. Add Record")
        print("2. View Records")
        print("3. Search Records")
        print("4. Logout")

        ch = input("Choice: ")

        if ch == "1":
            add_record()
        elif ch == "2":
            view_records()
        elif ch == "3":
            search_records()
        elif ch == "4":
            break

def user_menu():
    while True:
        print("\n--- USER MENU ---")
        print("1. View Records")
        print("2. Search Records")
        print("3. Logout")

        ch = input("Choice: ")

        if ch == "1":
            view_records()
        elif ch == "2":
            search_records()
        elif ch == "3":
            break

# ---------------- MAIN ---------------- #

def main():
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Select: ")

        if choice == "1":
            register()
        elif choice == "2":
            user, role = login()
            if role == "admin":
                admin_menu()
            elif role == "management":
                management_menu()
            elif role == "user":
                user_menu()
        elif choice == "3":
            break

if __name__ == "__main__":
    main()
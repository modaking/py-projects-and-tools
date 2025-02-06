import json
import os
import base64
import pyperclip
import csv
import hashlib
import secrets
import getpass
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# File to store encrypted passwords
PASSWORD_FILE = "passwords.json"
SALT_FILE = "salt.key"


def generate_salt():
    """Generate and save a new salt if it doesn't exist."""
    if not os.path.exists(SALT_FILE):
        salt = secrets.token_bytes(16)
        with open(SALT_FILE, "wb") as f:
            f.write(salt)


def load_salt():
    """Load the salt from file."""
    with open(SALT_FILE, "rb") as f:
        return f.read()


def derive_key(master_password, salt):
    """Derive a 32-byte key from the master password using PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(master_password.encode()))


def encrypt_password(password, key):
    """Encrypt a password using the provided key."""
    cipher = Fernet(key)
    return cipher.encrypt(password.encode()).decode()


def decrypt_password(encrypted_password, key):
    """Decrypt a password using the provided key."""
    cipher = Fernet(key)
    return cipher.decrypt(encrypted_password.encode()).decode()


def save_passwords(passwords, key):
    """Save encrypted passwords to file."""
    encrypted_data = {site: encrypt_password(passwd, key) for site, passwd in passwords.items()}
    with open(PASSWORD_FILE, "w") as f:
        json.dump(encrypted_data, f, indent=4)


def load_passwords(key):
    """Load and decrypt passwords from file."""
    if not os.path.exists(PASSWORD_FILE):
        return {}
    with open(PASSWORD_FILE, "r") as f:
        encrypted_data = json.load(f)
    try:
        return {site: decrypt_password(passwd, key) for site, passwd in encrypted_data.items()}
    except:
        return None  # Invalid password case


def import_from_google(csv_file, key):
    """Import passwords from Google Password Manager CSV and encrypt them."""
    passwords = load_passwords(key)
    if passwords is None:
        print("Invalid master password!")
        return
    with open(csv_file, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if "name" in row and "password" in row:
                passwords[row["name"]] = row["password"]
    save_passwords(passwords, key)
    print("Passwords imported successfully!")


def copy_to_clipboard(site, key):
    """Copy a password to the clipboard."""
    passwords = load_passwords(key)
    if passwords is None:
        print("Invalid master password!")
        return
    if site in passwords:
        pyperclip.copy(passwords[site])
        print(f"Password for {site} copied to clipboard!")
    else:
        print("Site not found!")


if __name__ == "__main__":
    master_password = getpass.getpass("Enter master password: ")
    generate_salt()
    salt = load_salt()
    key = derive_key(master_password, salt)
    passwords = load_passwords(key)

    if passwords is None:
        print("Invalid master password! Exiting...")
        exit()

    while True:
        print("\nOptions:")
        print("1. Add password")
        print("2. Retrieve password")
        print("3. Import from Google CSV")
        print("4. Copy password to clipboard")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            site = input("Enter site name: ")
            password = getpass.getpass("Enter password: ")
            passwords[site] = password
            save_passwords(passwords, key)
            print("Password saved!")

        elif choice == "2":
            site = input("Enter site name: ")
            print(f"Password: {passwords.get(site, 'Not found')}")

        elif choice == "3":
            csv_file = input("Enter Google CSV file path: ")
            import_from_google(csv_file, key)

        elif choice == "4":
            site = input("Enter site name: ")
            copy_to_clipboard(site, key)

        elif choice == "5":
            break

        else:
            print("Invalid choice. Try again.")

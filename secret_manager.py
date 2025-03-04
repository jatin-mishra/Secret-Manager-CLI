#!/usr/bin/env python3


from cryptography.fernet import Fernet
import getpass
import json
import os
import pyperclip
import base64
import random
import string

# File to store encrypted secrets
SECRETS_FILE = os.getenv("SECRETS_FILE", os.path.expanduser("~/Desktop/secrets.enc"))
AUTH_FILE = os.getenv("AUTH_FILE", os.path.expanduser("~/Desktop/auth")) 


def encrypt_data(data, secret_key):
    """Encrypts given data using the provided secret key."""
    cipher = Fernet(secret_key)
    return cipher.encrypt(json.dumps(data).encode())

def decrypt_data(encrypted_data, secret_key):
    """Decrypts data using the provided secret key."""
    cipher = Fernet(secret_key)
    return json.loads(cipher.decrypt(encrypted_data).decode())

def load_encrypted_data():
    """Load encrypted API keys from file."""
    if not os.path.exists(SECRETS_FILE):
        return None
    with open(SECRETS_FILE, "rb") as f:
        return f.read()

def save_encrypted_data(encrypted_data):
    """Save encrypted API keys to file."""
    with open(SECRETS_FILE, "wb") as f:
        f.write(encrypted_data)

def prompt_secret_key():
    """Prompts user for a secret key and encodes it properly."""
    secret_key_input = getpass.getpass("Enter your secret key: ").strip()
    return base64.urlsafe_b64encode(secret_key_input.ljust(32).encode()[:32])

def bulk_add_api_keys():
    """Bulk add API keys from a file and encrypt them."""
    if not os.path.exists(AUTH_FILE):
        print(f"Error: '{AUTH_FILE}' not found.")
        return

    user_secret_key = prompt_secret_key()
    
    encrypted_data = load_encrypted_data()
    api_keys = {}

    if encrypted_data:
        try:
            api_keys = decrypt_data(encrypted_data, user_secret_key)
        except:
            print("Warning: Existing keys may have a different secret key. Proceeding with a new encryption.")

    with open(AUTH_FILE, "r") as file:
        for line in file:
            line = line.strip()
            if "=" not in line:
                print(f"Skipping invalid line: {line}")
                continue
            
            key, value = line.split("=", 1)
            key, value = key.strip(), value.strip()

            if key in api_keys:
                if api_keys[key] == value:
                    print(f"Skipping {key} (Already exists with same value)")
                    continue

                consent = input(f"API key '{key}' already exists. Overwrite? (yes/no): ").strip().lower()
                if consent != "yes":
                    print(f"Skipping update for '{key}'.")
                    continue  

            api_keys[key] = value

    encrypted_data = encrypt_data(api_keys, user_secret_key)
    save_encrypted_data(encrypted_data)

    print("API keys added successfully!")

def compare_api_keys():
    """Compares API keys from a file with stored values."""
    if not os.path.exists(AUTH_FILE):
        print(f"Error: '{AUTH_FILE}' not found.")
        return

    user_secret_key = prompt_secret_key()

    encrypted_data = load_encrypted_data()
    if not encrypted_data:
        print("No API keys found! Please add some first.")
        return

    try:
        stored_api_keys = decrypt_data(encrypted_data, user_secret_key)
    except:
        print("Incorrect secret key! Unable to decrypt stored API keys.")
        return

    mismatched_keys = []
    
    with open(AUTH_FILE, "r") as file:
        for line in file:
            line = line.strip()
            if "=" not in line:
                continue
            
            key, value = line.split("=", 1)
            key, value = key.strip(), value.strip()

            if key in stored_api_keys and stored_api_keys[key] != value:
                mismatched_keys.append(key)

    if mismatched_keys:
        print("\nMismatched keys found:")
        for key in mismatched_keys:
            print(f"- {key}")
    else:
        print("\nAll keys match the stored values!")


# Function to load encrypted data from file
def load_encrypted_data():
    if not os.path.exists(SECRETS_FILE):
        return None
    with open(SECRETS_FILE, "rb") as f:
        return f.read()

# Function to save encrypted data to file
def save_encrypted_data(encrypted_data):
    with open(SECRETS_FILE, "wb") as f:
        f.write(encrypted_data)


def clear_all_keys():
    """Delete all stored API keys after user confirmation."""
    if not os.path.exists(SECRETS_FILE):
        print("No API keys stored.")
        return

    consent = input("Are you sure you want to delete all API keys? (yes/no): ").strip().lower()
    if consent == "yes":
        os.remove(SECRETS_FILE)
        print("All API keys have been deleted!")
    else:
        print("Operation canceled.")


def generate_strong_password():
    """Generate a strong random password with a length between 10 and 20 characters."""
    length = random.randint(10, 20)  # Randomly select password length between 10 and 20

    characters = (
        string.ascii_uppercase +
        string.ascii_lowercase +
        string.digits +
        string.punctuation
    )

    # Ensure the password has at least one of each required character type
    password = [
        random.choice(string.ascii_uppercase),
        random.choice(string.ascii_lowercase),
        random.choice(string.digits),
        random.choice(string.punctuation)
    ]

    # Fill the rest of the password length with random choices
    password += random.choices(characters, k=length - 4)
    
    # Shuffle to ensure randomness
    random.shuffle(password)
    
    return ''.join(password)



# Function to add API keys
def add_api_keys():
    # Let user enter a key OR generate a new one
    secret_key_input = getpass.getpass("Enter your secret key (Encryption Key) (or press Enter to generate a new one): ").strip()

    if secret_key_input:
        try:
            user_secret_key = base64.urlsafe_b64encode(secret_key_input.ljust(32).encode()[:32])  # Ensure 32 bytes
            cipher = Fernet(user_secret_key)
        except ValueError:
            print("Invalid key! Ensure it's a valid 32-byte base64-encoded key.")
            return
    else:
        user_secret_key = Fernet.generate_key()
        cipher = Fernet(user_secret_key)
        print("Generated new secret key (SAVE THIS!):", user_secret_key.decode())

    # Load existing keys (if any)
    encrypted_data = load_encrypted_data()
    api_keys = {}

    if encrypted_data:
        try:
            decrypted_data = cipher.decrypt(encrypted_data).decode()
            api_keys = json.loads(decrypted_data)
        except:
            print("Warning: Existing keys may have a different secret key. Proceeding with a new encryption.")

    # Ask the user to enter API keys dynamically
    key = input("Enter key name for which you want to store password. Ex: email, okta etc (or press Enter to finish): ").strip()
    if not key:
        return
    
    if key in api_keys:
        consent = input(f"API key '{key}' already exists. Do you want to override it? (yes/no): ").strip().lower()
        if consent != "yes":
            print(f"Skipping update for '{key}'.")
            return

    value = getpass.getpass(f"Enter value for {key}, Or press enter to use strong auto generated password").strip()
    if not value:
        value = generate_strong_password()
    api_keys[key] = value

    # Encrypt and store updated API keys
    encrypted_data = cipher.encrypt(json.dumps(api_keys).encode())
    save_encrypted_data(encrypted_data)

    print("API keys encrypted and stored successfully!")

# Function to retrieve an API key
def get_api_key():
    # Ask for user secret key
    secret_key_input = getpass.getpass("Enter your secret key: ").strip()

    try:
        user_secret_key = base64.urlsafe_b64encode(secret_key_input.ljust(32).encode()[:32])  # Ensure 32 bytes
        cipher = Fernet(user_secret_key)
    except ValueError:
        print("Invalid key! Ensure it's a valid 32-byte base64-encoded key.")
        return

    # Load and decrypt data
    encrypted_data = load_encrypted_data()
    if not encrypted_data:
        print("No API keys found! Please add some first.")
        return

    try:
        decrypted_data = cipher.decrypt(encrypted_data).decode()
        api_keys = json.loads(decrypted_data)
    except:
        print("Incorrect secret key! Cannot retrieve data.")
        return

    # Ask for the API key name
    key_name = input("Enter the key name for which you want to retrieve value: ").strip()
    if key_name in api_keys:
        pyperclip.copy(api_keys[key_name])  # Copy to clipboard
        print(f"API key for '{key_name}' copied to clipboard!")
    else:
        print("API key not found!")

def change_secret_key():
    """Change the secret key and re-encrypt stored API keys."""
    if not os.path.exists(SECRETS_FILE):
        print("No stored API keys found! Add some first before changing the secret key.")
        return

    # Ask for the old secret key
    old_secret_key_input = getpass.getpass("Enter your old secret key: ").strip()
    
    try:
        old_secret_key = base64.urlsafe_b64encode(old_secret_key_input.ljust(32).encode()[:32])  # Ensure 32 bytes
        cipher_old = Fernet(old_secret_key)
    except ValueError:
        print("Invalid key! Ensure it's a valid 32-byte base64-encoded key.")
        return

    # Load existing data
    encrypted_data = load_encrypted_data()
    if not encrypted_data:
        print("No stored API keys found!")
        return

    # Decrypt using old key
    try:
        decrypted_data = cipher_old.decrypt(encrypted_data).decode()
        api_keys = json.loads(decrypted_data)
    except:
        print("Incorrect old secret key! Unable to decrypt stored API keys.")
        return
    
    # Ask for the new secret key
    print("\nEnter a **NEW** secret key (or press Enter to generate a new one): ")
    new_secret_key_input = getpass.getpass().strip()

    if new_secret_key_input:
        new_secret_key = base64.urlsafe_b64encode(new_secret_key_input.ljust(32).encode()[:32])  # Ensure 32 bytes
    else:
        new_secret_key = Fernet.generate_key()
        print("Generated new secret key (SAVE THIS!):", new_secret_key.decode())

    cipher_new = Fernet(new_secret_key)

    # Encrypt with the new key
    encrypted_data = cipher_new.encrypt(json.dumps(api_keys).encode())

    # Save back to file
    save_encrypted_data(encrypted_data)

    print("\n✅ Secret key successfully changed! Make sure to **save the new key safely.**")


def list_api_keys():
    """List all API keys matching a given prefix (or all if no prefix is provided)."""
    secret_key_input = getpass.getpass("Enter your secret key: ").strip()
    
    try:
        user_secret_key = base64.urlsafe_b64encode(secret_key_input.ljust(32).encode()[:32])  # Ensure 32 bytes
        cipher = Fernet(user_secret_key)
    except ValueError:
        print("Invalid key! Ensure it's a valid 32-byte base64-encoded key.")
        return
    
    encrypted_data = load_encrypted_data()
    if not encrypted_data:
        print("No API keys found! Please add some first.")
        return
    
    try:
        decrypted_data = cipher.decrypt(encrypted_data).decode()
        api_keys = json.loads(decrypted_data)
    except:
        print("Incorrect secret key! Cannot retrieve data.")
        return
    
    prefix = input("Enter key prefix (or leave empty to list all): ").strip()
    matching_keys = [key for key in api_keys if key.startswith(prefix)]
    
    if matching_keys:
        print("Stored API keys:")
        for key in matching_keys:
            print(f"- {key}")
    else:
        print("No matching keys found!")

# Main program flow
if __name__ == "__main__":
    action = input("Do you want to add or get API keys? (add/get/clear/list_keys/change_secret/add_in_bulk/compare_with_file): ").strip().lower()
    print(f"SECRETS_FILE: {SECRETS_FILE}")

    if action == "add":
        add_api_keys()
    elif action == "get":
        get_api_key()
    elif action == "clear":
        clear_all_keys()
    elif action == "change_secret":
        change_secret_key()
    elif action == "list_keys":
        list_api_keys()
    elif action == "add_in_bulk":
        bulk_add_api_keys()
    elif action == "compare_with_file" :
        compare_api_keys()
    else:
        print("Invalid option! Please enter 'add' or 'get'.")

from cryptography.fernet import Fernet

def generate_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    return open("key.key", "rb").read()

def encrypt_file(filename):
    key = load_key()
    fernet = Fernet(key)

    with open(filename, "rb") as file:
        original_data = file.read()
    
    encrypted_data = fernet.encrypt(original_data)

    with open(filename + ".enc", "wb") as encrypted_file:
        encrypted_file.write(encrypted_data)

def decrypt_file(encrypted_filename):
    key = load_key()
    fernet = Fernet(key)

    with open(encrypted_filename, "rb") as enc_file:
        encrypted_data = enc_file.read()

    decrypted_data = fernet.decrypt(encrypted_data)

    with open(encrypted_filename.replace(".enc", ""), "wb") as dec_file:
        dec_file.write(decrypted_data)

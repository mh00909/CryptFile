import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64

def generate_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    return open("key.key", "rb").read()

def generate_key_from_password(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32, 
        salt=salt,
        iterations=100000, 
        backend=default_backend()
    )
    
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt_file(filename, password, delete_original=True):
    key, salt = generate_key_from_password(password)  
    cipher = Fernet(key)  

    with open(filename, "rb") as file:
        original_data = file.read()

    encrypted_data = cipher.encrypt(original_data)

    # Zapisanie sól + zaszyfrowane dane do pliku
    encrypted_filename = filename + ".enc"
    with open(encrypted_filename, "wb") as encrypted_file:
        encrypted_file.write(salt + encrypted_data)  

    if delete_original:
        os.remove(filename)  


def decrypt_file(encrypted_filename, password):
    with open(encrypted_filename, "rb") as enc_file:
        salt = enc_file.read(16)  # Pierwsze 16 bajtów jako sól
        encrypted_data = enc_file.read()  # Reszta to zaszyfrowane dane

    key, _ = generate_key_from_password(password, salt)  
    cipher = Fernet(key)

    try:
        decrypted_data = cipher.decrypt(encrypted_data)
        original_filename = encrypted_filename.replace(".enc", "")

        with open(original_filename, "wb") as dec_file:
            dec_file.write(decrypted_data)

        os.remove(encrypted_filename)
        return True
    except Exception:
        return False




def encrypt_folder(folder_path, password, delete_original=True):
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            encrypt_file(file_path, password, delete_original)

def decrypt_folder(folder_path, password):
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".enc"):  # Odszyfruj tylko zaszyfrowane pliki
                file_path = os.path.join(root, file)
                decrypt_file(file_path, password)
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64

def generate_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    return open("key.key", "rb").read()

def generate_key_from_password(password, salt, for_fernet=False):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )

    key = kdf.derive(password.encode())

    if for_fernet:
        return base64.urlsafe_b64encode(key)  # Base64 dla Fernet
    return key  # Surowe bajty dla AES

def encrypt_file_aes(filename, password, delete_original=True):
    salt = os.urandom(16)
    key = generate_key_from_password(password, salt, for_fernet=False)  

    with open(filename, "rb") as file:
        data = file.read()

    iv = os.urandom(12)  
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(data) + encryptor.finalize()
    tag = encryptor.tag

    encrypted_filename = filename + ".aes"
    with open(encrypted_filename, "wb") as enc_file:
        enc_file.write(salt + iv + tag + encrypted_data) 

    if delete_original:
        os.remove(filename)

def decrypt_file_aes(encrypted_filename, password):
    try:
        with open(encrypted_filename, "rb") as enc_file:
            salt = enc_file.read(16)  
            iv = enc_file.read(12)  
            tag = enc_file.read(16)   
            encrypted_data = enc_file.read()  

        key = generate_key_from_password(password, salt, for_fernet=False)

        cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

        original_filename = encrypted_filename.replace(".aes", "")
        with open(original_filename, "wb") as dec_file:
            dec_file.write(decrypted_data)

        os.remove(encrypted_filename)
        return True

    except Exception as e:
        print(f"❌ Błąd deszyfrowania AES: {e}")
        return False



def encrypt_file_fernet(filename, password, delete_original=True):
    salt = os.urandom(16)
    key = generate_key_from_password(password, salt, for_fernet=True)  
    cipher = Fernet(key)

    with open(filename, "rb") as file:
        original_data = file.read()

    encrypted_data = cipher.encrypt(original_data)
    encrypted_filename = filename + ".fernet"

    with open(encrypted_filename, "wb") as encrypted_file:
        encrypted_file.write(salt + encrypted_data)

    if delete_original:
        os.remove(filename)


def decrypt_file_fernet(encrypted_filename, password):
    try:
        with open(encrypted_filename, "rb") as enc_file:
            salt = enc_file.read(16) 
            encrypted_data = enc_file.read() 

        key = generate_key_from_password(password, salt, for_fernet=True)
        cipher = Fernet(key)

        decrypted_data = cipher.decrypt(encrypted_data)

        original_filename = encrypted_filename.replace(".fernet", "")
        with open(original_filename, "wb") as dec_file:
            dec_file.write(decrypted_data)

        os.remove(encrypted_filename)
        return True

    except Exception as e:
        print(f"❌ Błąd deszyfrowania Fernet: {e}")
        return False



def encrypt_folder(folder_path, password, delete_original=True, algorithm="AES-GCM"):
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if algorithm == "AES-GCM":
                encrypt_file_aes(file_path, password, delete_original)
            elif algorithm == "Fernet":
                encrypt_file_fernet(file_path, password, delete_original)

def decrypt_folder(folder_path, password, algorithm="AES-GCM"):
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith(".aes"):
                decrypt_file_aes(file_path, password)
            elif file.endswith(".fernet"):
                decrypt_file_fernet(file_path, password)

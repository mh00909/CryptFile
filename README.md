# CryptFile
CryptFile is a secure file encryption application that allows users to encrypt and decrypt files using AES-GCM and Fernet encryption methods. It includes a user authentication system with email verification.

## Features
### User Authentication
- Register and login system with SQLite database
- Password hashing using SHA-256
- Salting for added security
- Two-Factor Authentication (2FA) via email
- Password strength validation to prevent weak passwords
### File Encryption & Decryption
- AES-GCM (Advanced Encryption Standard) – highly secure encryption
- Fernet (Symmetric encryption) – simple and effective
- Custom encryption key derivation from a user password
- Automatic file renaming (.aes or .fernet)
- Optional original file deletion after encryption
### Folder Encryption & Decryption
- Recursively encrypt and decrypt all files in a directory
- Option to retain or delete original files
### Graphical User Interface (GUI)
- Built with PyQt5
- File selection & management
- Real-time list of encrypted files
- Error handling using QMessageBox
### Email-based Verification
- Generates a 6-digit verification code for email confirmation
- Uses SMTP protocol for email sending
### Additional Features
- Select encryption algorithm (AES-GCM or Fernet)
- User-friendly file selection
- Prevents incorrect decryption attempts
- Logs important actions (optional enhancement)

## Installation & Setup
### Clone the Repository
```
git clone https://github.com/mh00909/CryptFile.git
cd CryptFile
```
### Set Up Environment Variables
Create a .env file in the root directory and configure SMTP settings for email verification:
```
SMTP_SERVER=smtp.your-email.com
SMTP_PORT=465
SENDER_EMAIL=your-email@example.com
SENDER_PASSWORD=your-email-password
```
### Initialize the Database
Run the following command to create the SQLite database:
```
python database.py
```
### Run the Application
```
python main.py
```
### Usage
1. Register a new account 
- Enter an email, username, and password.
- Verify your email using the 2FA code sent to your inbox.
2. Login 
- Enter your credentials.
- Upon successful login, the main encryption UI appears.
3. Encrypt Files 
- Select a file using the "Choose File" button.
- Enter a secure password for encryption.
- Choose the encryption algorithm (AES-GCM or Fernet).
- Click "Encrypt" – the file is encrypted and listed.
4. Decrypt Files 
- Select an encrypted file from the list.
- Enter the correct decryption password.
- Click "Decrypt" to restore the file.
5. Encrypt / Decrypt Folders 
- Encrypt all files in a directory recursively.
- Retain or delete original files after encryption.

### Technologies Used
- Python 3.10+
- PyQt5 – GUI framework
- cryptography – Encryption (AES-GCM, Fernet)
- sqlite3 – Database for user authentication
- smtplib & email – Email verification via SMTP
- dotenv – Secure environment variable management

### Screenshots
![image](https://github.com/user-attachments/assets/a2506247-c141-4396-a5fb-49e0246ace3d)
![image](https://github.com/user-attachments/assets/0b14d409-a90b-4e9e-845b-b8e7feaa56ad)

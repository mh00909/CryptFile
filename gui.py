import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QComboBox, QPushButton, QCheckBox, QFileDialog, QVBoxLayout, QLabel, 
    QLineEdit, QMessageBox, QHBoxLayout, QListWidget, QFrame
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
import encryption

class CryptFileApp(QWidget):
    def __init__(self, username, salt):
        super().__init__()

        self.selected_file = None
        self.salt = salt
        self.username = username
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f"CryptFile - Witaj {self.username}!")
        self.setGeometry(100, 100, 500, 450)  

        self.setStyleSheet("""
            QWidget {
                background-color: #2E2E2E;
                color: #FFFFFF;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLineEdit {
                padding: 8px;
                border-radius: 5px;
                border: 1px solid #5E5E5E;
                background-color: #3E3E3E;
                color: #FFFFFF;
            }
            QLabel {
                font-size: 14px;
            }
            QCheckBox {
                font-size: 12px;
            }
            QListWidget {
                background-color: #3E3E3E;
                color: white;
                border: 1px solid #5E5E5E;
                padding: 5px;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(12)

        header = QLabel("🔐 CryptFile - Bezpieczne szyfrowanie plików")
        header.setFont(QFont("Arial", 16, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        # Sekcja wyboru pliku
        file_section = QVBoxLayout()
        self.label = QLabel("🔍 Wybierz plik do szyfrowania:")
        self.button_select = QPushButton(" Wybierz plik")
        self.button_select.setIcon(QIcon("icons/folder.png"))
        self.button_select.clicked.connect(self.choose_file)
        file_section.addWidget(self.label)
        file_section.addWidget(self.button_select)
        layout.addLayout(file_section)

        # Sekcja hasła
        password_section = QVBoxLayout()
        self.password_label = QLabel("🔑 Podaj hasło:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        password_section.addWidget(self.password_label)
        password_section.addWidget(self.password_input)
        layout.addLayout(password_section)

        # Sekcja przycisków szyfrowania
        encryption_buttons = QHBoxLayout()
        self.button_encrypt = QPushButton("🔒 Szyfruj plik")
        self.button_encrypt.clicked.connect(self.encrypt_file)
        self.button_decrypt = QPushButton("🔓 Deszyfruj plik")
        self.button_decrypt.clicked.connect(self.decrypt_file)
        encryption_buttons.addWidget(self.button_encrypt)
        encryption_buttons.addWidget(self.button_decrypt)
        layout.addLayout(encryption_buttons)

        # Sekcja przycisków szyfrowania folderów
        folder_buttons = QHBoxLayout()
        self.button_encrypt_folder = QPushButton("📁 Szyfruj folder")
        self.button_encrypt_folder.clicked.connect(self.encrypt_folder)
        self.button_decrypt_folder = QPushButton("📁 Deszyfruj folder")
        self.button_decrypt_folder.clicked.connect(self.decrypt_folder)
        folder_buttons.addWidget(self.button_encrypt_folder)
        folder_buttons.addWidget(self.button_decrypt_folder)
        layout.addLayout(folder_buttons)

        # Usuwanie pliku po szyfrowaniu
        self.delete_original_checkbox = QCheckBox("🗑 Usuń oryginalny plik po szyfrowaniu")
        layout.addWidget(self.delete_original_checkbox)

        frame = QFrame()
        options_layout = QVBoxLayout(frame)
        self.algorithm_label = QLabel("🔒 Wybierz algorytm szyfrowania:")
        self.algorithm_select = QComboBox()
        self.algorithm_select.addItems(["AES-GCM", "Fernet"])
        options_layout.addWidget(self.algorithm_label)
        options_layout.addWidget(self.algorithm_select)
        layout.addWidget(frame)

        # Lista zaszyfrowanych plików
        self.encrypted_files_list = QListWidget()
        self.encrypted_files_list.itemClicked.connect(self.decrypt_selected_file)
        layout.addWidget(QLabel("📂 Zaszyfrowane pliki:"))
        layout.addWidget(self.encrypted_files_list)

        self.setLayout(layout)
        self.load_encrypted_files()

    def choose_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Wybierz plik")
        if file_name:
            self.selected_file = file_name
            self.label.setText(f"📄 Wybrano: {file_name}")

    def encrypt_file(self):
        if not self.selected_file:
            QMessageBox.warning(self, "Błąd", "Wybierz plik przed szyfrowaniem!")
            return
        
        password = self.password_input.text()
        if not password:
            QMessageBox.warning(self, "Błąd", "Podaj hasło do szyfrowania!")
            return

        algorithm = self.algorithm_select.currentText()
        delete_original = self.delete_original_checkbox.isChecked()

        if algorithm == "AES-GCM":
            encryption.encrypt_file_aes(self.selected_file, password, delete_original)
            encrypted_filename = self.selected_file + ".aes"
        else:
            encryption.encrypt_file_fernet(self.selected_file, password, delete_original)
            encrypted_filename = self.selected_file + ".fernet"

        QMessageBox.information(self, "Sukces", "Plik został zaszyfrowany!")
        self.update_file_list(encrypted_filename)


    def decrypt_file(self):
        if not self.selected_file:
            QMessageBox.warning(self, "Błąd", "Wybierz plik przed deszyfrowaniem!")
            return
        
        password = self.password_input.text()
        if not password:
            QMessageBox.warning(self, "Błąd", "Podaj hasło do deszyfrowania!")
            return

        if self.selected_file.endswith(".aes"):
            success = encryption.decrypt_file_aes(self.selected_file, password)
        elif self.selected_file.endswith(".fernet"):
            success = encryption.decrypt_file_fernet(self.selected_file, password)
        else:
            QMessageBox.warning(self, "Błąd", "Nieznany format pliku!")
            return

        if success:
            QMessageBox.information(self, "Sukces", "Plik został odszyfrowany!")
            self.remove_from_list(self.selected_file)
        else:
            QMessageBox.critical(self, "Błąd", "Niepoprawne hasło lub uszkodzony plik!")


    def encrypt_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Wybierz folder do szyfrowania")
        if not folder_path:
            return

        password = self.password_input.text()
        if not password:
            QMessageBox.warning(self, "Błąd", "Podaj hasło do szyfrowania!")
            return

        delete_original = self.delete_original_checkbox.isChecked()
        encryption.encrypt_folder(folder_path, password, delete_original)
        QMessageBox.information(self, "Sukces", "Folder został zaszyfrowany!")

        self.load_encrypted_files()

    def decrypt_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Wybierz folder do deszyfrowania")
        if not folder_path:
            return

        password = self.password_input.text()
        if not password:
            QMessageBox.warning(self, "Błąd", "Podaj hasło do deszyfrowania!")
            return

        encryption.decrypt_folder(folder_path, password)
        QMessageBox.information(self, "Sukces", "Folder został odszyfrowany!")
        self.load_encrypted_files()

    def load_encrypted_files(self):
        self.encrypted_files_list.clear()
        for file in os.listdir():
            if file.endswith(".enc"):
                self.encrypted_files_list.addItem(f"🔒 {file}")

    def update_file_list(self, filename):
        self.encrypted_files_list.addItem(f"🔒 {filename}")

    def decrypt_selected_file(self, item):
        self.selected_file = item.text()[2:]  
        self.decrypt_file()

    def remove_from_list(self, filename):
        for index in range(self.encrypted_files_list.count()):
            item = self.encrypted_files_list.item(index)
            if item.text()[2:] == filename: 
                self.encrypted_files_list.takeItem(index)
                break

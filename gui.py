import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QCheckBox, QFileDialog, QVBoxLayout, QLabel, 
    QLineEdit, QMessageBox, QHBoxLayout, QFrame
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
        self.setGeometry(100, 100, 500, 400)  # Większe okno

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
        """)

        layout = QVBoxLayout()
        layout.setSpacing(12)

        header = QLabel("🔐 CryptFile - Bezpieczne szyfrowanie plików")
        header.setFont(QFont("Arial", 16, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        file_section = QVBoxLayout()
        self.label = QLabel("🔍 Wybierz plik lub folder do szyfrowania:")
        self.label.setFont(QFont("Arial", 12))
        self.button_select = QPushButton(" Wybierz")
        self.button_select.setIcon(QIcon("icons/find.png"))  
        self.button_select.clicked.connect(self.choose_file)

        file_section.addWidget(self.label)
        file_section.addWidget(self.button_select)
        layout.addLayout(file_section)

        password_section = QVBoxLayout()
        self.password_label = QLabel("🔑 Podaj hasło:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        password_section.addWidget(self.password_label)
        password_section.addWidget(self.password_input)
        layout.addLayout(password_section)

        encryption_buttons = QHBoxLayout()
        self.button_encrypt = QPushButton(" Szyfruj plik")
        self.button_encrypt.setIcon(QIcon("icons/document.png"))
        self.button_encrypt.clicked.connect(self.encrypt_file)
        self.button_decrypt = QPushButton(" Deszyfruj plik")
        self.button_decrypt.setIcon(QIcon("icons/document.png"))
        self.button_decrypt.clicked.connect(self.decrypt_file)
        encryption_buttons.addWidget(self.button_encrypt)
        encryption_buttons.addWidget(self.button_decrypt)
        layout.addLayout(encryption_buttons)

        folder_buttons = QHBoxLayout()
        self.button_encrypt_folder = QPushButton(" Szyfruj folder")
        self.button_encrypt_folder.setIcon(QIcon("icons/folder.png"))  
        self.button_encrypt_folder.clicked.connect(self.encrypt_folder)
        self.button_decrypt_folder = QPushButton(" Deszyfruj folder")
        self.button_decrypt_folder.setIcon(QIcon("icons/folder.png"))  
        self.button_decrypt_folder.clicked.connect(self.decrypt_folder)
        folder_buttons.addWidget(self.button_encrypt_folder)
        folder_buttons.addWidget(self.button_decrypt_folder)
        layout.addLayout(folder_buttons)

        self.delete_original_checkbox = QCheckBox("🗑 Usuń oryginalny plik po szyfrowaniu")
        layout.addWidget(self.delete_original_checkbox)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background-color: #5E5E5E;")
        layout.addWidget(line)

        user_label = QLabel(f"👤 Zalogowany jako: {self.username}")
        user_label.setFont(QFont("Arial", 12, QFont.Bold))
        user_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(user_label)

        self.setLayout(layout)

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

        delete_original = self.delete_original_checkbox.isChecked()
        encryption.encrypt_file(self.selected_file, password, delete_original)
        QMessageBox.information(self, "Sukces", "Plik został zaszyfrowany!")

    def decrypt_file(self):
        if not self.selected_file:
            QMessageBox.warning(self, "Błąd", "Wybierz plik przed deszyfrowaniem!")
            return
        
        password = self.password_input.text()
        if not password:
            QMessageBox.warning(self, "Błąd", "Podaj hasło do deszyfrowania!")
            return

        success = encryption.decrypt_file(self.selected_file, password)
        if success:
            QMessageBox.information(self, "Sukces", "Plik został odszyfrowany!")
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CryptFileApp("DemoUser", "salt")
    window.show()
    sys.exit(app.exec_())

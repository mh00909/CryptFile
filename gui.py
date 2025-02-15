import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout, QLabel, QLineEdit, QMessageBox
import encryption

class CryptFileApp(QWidget):
    def __init__(self):
        super().__init__()

        self.selected_file = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("CryptFile - Bezpieczne szyfrowanie plików")
        self.setGeometry(100, 100, 400, 200)

        # Etykieta i przycisk do wyboru pliku
        self.label = QLabel("Wybierz plik:", self)
        self.button_select = QPushButton("Wybierz plik", self)
        self.button_select.clicked.connect(self.choose_file)

        self.password_label = QLabel("Podaj hasło:", self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)  # Ukrywanie hasła

        # Przycisk szyfrowania
        self.button_encrypt = QPushButton("🔒 Szyfruj", self)
        self.button_encrypt.clicked.connect(self.encrypt_file)

        # Przycisk deszyfrowania
        self.button_decrypt = QPushButton("🔓 Deszyfruj", self)
        self.button_decrypt.clicked.connect(self.decrypt_file)

        # Układ GUI
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button_select)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.button_encrypt)
        layout.addWidget(self.button_decrypt)
        self.setLayout(layout)

    def choose_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Wybierz plik")
        if file_name:
            self.selected_file = file_name
            self.label.setText(f"Wybrano: {file_name}")

    def encrypt_file(self):
        if not self.selected_file:
            QMessageBox.warning(self, "Błąd", "Wybierz plik przed szyfrowaniem!")
            return
        
        password = self.password_input.text()
        if not password:
            QMessageBox.warning(self, "Błąd", "Podaj hasło do szyfrowania!")
            return

        encryption.encrypt_file(self.selected_file, password)
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CryptFileApp()
    window.show()
    sys.exit(app.exec_())

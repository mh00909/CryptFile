from PyQt5.QtWidgets import QDialog, QInputDialog, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QCheckBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import database
import email_sender

class RegisterDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Rejestracja - CryptFile")
        self.setGeometry(100, 100, 400, 350)
        self.setStyleSheet("background-color: #f4f4f4;")

        layout = QVBoxLayout()

        title_label = QLabel("📝 Rejestracja")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Pole na e-mail
        email_container, self.email_input = self.create_input_field("E-mail:")
        username_container, self.username_input = self.create_input_field("Nazwa użytkownika:")
        password_container, self.password_input = self.create_input_field("Hasło:", password=True)
        confirm_password_container, self.confirm_password_input = self.create_input_field("Potwierdź hasło:", password=True)

        # Dodajemy kontenery (zawierające pola + "Pokaż hasło" dla haseł)
        layout.addWidget(email_container)
        layout.addWidget(username_container)
        layout.addWidget(password_container)
        layout.addWidget(confirm_password_container)

        # Przycisk rejestracji
        self.register_button = QPushButton("✅ Zarejestruj")
        self.register_button.setStyleSheet("background-color: #008CBA; color: white; font-size: 14px; padding: 8px;")
        self.register_button.clicked.connect(self.handle_register)
        layout.addWidget(self.register_button)

        self.setLayout(layout)


    def create_input_field(self, label_text, password=False):
        """Funkcja pomocnicza do tworzenia pól wejściowych"""
        container = QVBoxLayout()
        input_field = QLineEdit()
        input_field.setPlaceholderText(label_text)
        input_field.setFont(QFont("Arial", 12))
        input_field.setStyleSheet("padding: 5px; border-radius: 5px; border: 1px solid gray;")

        if password:
            input_field.setEchoMode(QLineEdit.Password)
            show_password = QCheckBox("Pokaż hasło")
            show_password.toggled.connect(lambda: input_field.setEchoMode(QLineEdit.Normal if show_password.isChecked() else QLineEdit.Password))
            container.addWidget(show_password)  # Dodajemy checkbox osobno

        container.addWidget(input_field)
        
        widget = QWidget()
        widget.setLayout(container)
        
        return widget, input_field  # 🛠️ Teraz zwracamy osobno kontener (dla layoutu) i pole tekstowe


    def handle_register(self):
        email = self.email_input.text()
        username = self.username_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        # Walidacja pól
        if not email or "@" not in email or "." not in email:
            QMessageBox.warning(self, "Błąd", "Podaj poprawny adres e-mail!")
            return

        if not username or len(username) < 4:
            QMessageBox.warning(self, "Błąd", "Nazwa użytkownika musi mieć co najmniej 4 znaki!")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Błąd", "Hasła nie są identyczne!")
            return

        password_error = database.check_password_strength(password)
        if password_error:
            QMessageBox.warning(self, "Błąd", password_error)
            return

        # Generowanie kodu 2FA i wysyłanie na e-mail
        registration_code = email_sender.generate_2fa_code()
        email_sender.send_2fa_email(email, registration_code)

        user_code, ok = QInputDialog.getText(self, "Kod potwierdzenia", "Podaj kod wysłany na e-mail:")
        if not ok or user_code != registration_code:
            QMessageBox.critical(self, "Błąd", "Niepoprawny kod potwierdzenia e-maila!")
            return

        register_result = database.register_user(username, password, email)
        if register_result == "Rejestracja zakończona sukcesem!":
            QMessageBox.information(self, "Sukces", register_result)
            self.accept()  # Zamykamy okno po sukcesie
        else:
            QMessageBox.warning(self, "Błąd", register_result)

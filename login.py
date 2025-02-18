from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QCheckBox, QLineEdit, QPushButton, QInputDialog, QMessageBox, QHBoxLayout, QWidget
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
import database
import email_sender
from gui import CryptFileApp

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Logowanie do CryptFile")
        self.setGeometry(100, 100, 400, 250)
        self.setStyleSheet("background-color: #f4f4f4;")

        self.username = None
        self.salt = None  

        layout = QVBoxLayout()

        title_label = QLabel("🔐 CryptFile - Logowanie")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        username_container, self.username_input = self.create_input_field("Nazwa użytkownika:")
        password_container, self.password_input = self.create_input_field("Hasło:", password=True)

        layout.addWidget(username_container)
        layout.addWidget(password_container)

        self.login_button = QPushButton("🔑 Zaloguj")
        self.login_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 14px; padding: 8px;")
        self.login_button.clicked.connect(self.handle_login)

        self.register_button = QPushButton("📝 Zarejestruj się")
        self.register_button.setStyleSheet("background-color: #008CBA; color: white; font-size: 14px; padding: 8px;")
        self.register_button.clicked.connect(self.handle_register)

        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)
        self.setLayout(layout)


    def create_input_field(self, label_text, password=False):
        container = QWidget()
        layout = QVBoxLayout()
        label = QLabel(label_text)
        input_field = QLineEdit()
        input_field.setFont(QFont("Arial", 12))
        input_field.setStyleSheet("padding: 5px; border-radius: 5px; border: 1px solid gray;")

        if password:
            input_field.setEchoMode(QLineEdit.Password)
            show_password = QCheckBox("Pokaż hasło")
            show_password.toggled.connect(lambda: input_field.setEchoMode(QLineEdit.Normal if show_password.isChecked() else QLineEdit.Password))
            layout.addWidget(show_password)

        layout.addWidget(label)
        layout.addWidget(input_field)
        container.setLayout(layout)

        return container, input_field  


    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        error, salt, email = database.get_user_salt(username, password)
        if error:
            QMessageBox.critical(self, "Błąd", error)
            return

        self.username = username
        self.salt = salt
        QMessageBox.information(self, "Sukces", "Zalogowano pomyślnie!")
        self.crypt_app = CryptFileApp(self.username, self.salt)  
        self.crypt_app.show()
        self.accept()

    def handle_register(self):
        username = self.username_input.text()
        password = self.password_input.text()

        email, ok = QInputDialog.getText(self, "E-mail", "Podaj swój adres e-mail:")
        if not ok or not email:
            QMessageBox.warning(self, "Błąd", "E-mail jest wymagany!")
            return

        registration_code = email_sender.generate_2fa_code()
        email_sender.send_2fa_email(email, registration_code)

        user_code, ok = QInputDialog.getText(self, "Kod potwierdzenia", "Podaj kod wysłany na e-mail:")
        if not ok or user_code != registration_code:
            QMessageBox.critical(self, "Błąd", "Niepoprawny kod potwierdzenia e-maila!")
            return

        register_result = database.register_user(username, password, email)
        if register_result == "Rejestracja zakończona sukcesem!":
            QMessageBox.information(self, "Sukces", register_result)
        else:
            QMessageBox.warning(self, "Błąd", register_result)

def create_input_field(self, label_text, password=False):
    container = QWidget()
    layout = QVBoxLayout()
    label = QLabel(label_text)
    input_field = QLineEdit()
    input_field.setFont(QFont("Arial", 12))
    input_field.setStyleSheet("padding: 5px; border-radius: 5px; border: 1px solid gray;")

    if password:
        input_field.setEchoMode(QLineEdit.Password)
        show_password = QCheckBox("Pokaż hasło")
        show_password.toggled.connect(lambda: input_field.setEchoMode(QLineEdit.Normal if show_password.isChecked() else QLineEdit.Password))
        layout.addWidget(show_password)

    layout.addWidget(label)
    layout.addWidget(input_field)
    container.setLayout(layout)
    self.layout().addWidget(container)

    return input_field

from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from gui import CryptFileApp
from login import LoginDialog
from register import RegisterDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CryptFile - Bezpieczne szyfrowanie plików")
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("background-color: #f4f4f4;")

        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        layout = QVBoxLayout()

        title_label = QLabel("🔐 CryptFile")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        description_label = QLabel("Wybierz opcję:")
        description_label.setFont(QFont("Arial", 12))
        description_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(description_label)

        self.login_button = QPushButton("🔑 Logowanie")
        self.login_button.setFont(QFont("Arial", 14))
        self.login_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px;")
        self.login_button.clicked.connect(self.open_login)
        layout.addWidget(self.login_button)

        self.register_button = QPushButton("📝 Rejestracja")
        self.register_button.setFont(QFont("Arial", 14))
        self.register_button.setStyleSheet("background-color: #008CBA; color: white; padding: 10px;")
        self.register_button.clicked.connect(self.open_register)
        layout.addWidget(self.register_button)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def open_login(self):
        login_dialog = LoginDialog()
        if login_dialog.exec_() == LoginDialog.Accepted:
            self.show_main_app(login_dialog.username, login_dialog.salt)

    def open_register(self):
        register_dialog = RegisterDialog()
        if register_dialog.exec_() == RegisterDialog.Accepted:
            print("✅ Rejestracja zakończona sukcesem!")
            
    def show_main_app(self, username, salt):
        self.crypt_app = CryptFileApp(username, salt) 
        self.crypt_app.show() 
        self.close() 
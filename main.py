import sys
from PyQt5.QtWidgets import QApplication, QDialog
from gui import CryptFileApp
from login import LoginDialog
import encryption
import database
from main_window import MainWindow

def main():
    data = database.create_database()
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    try:
        encryption.load_key()
    except FileNotFoundError:
        encryption.generate_key()
        print("🔑 Wygenerowano nowy klucz szyfrowania!")

    main()  
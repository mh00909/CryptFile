import sys
from PyQt5.QtWidgets import QApplication
from gui import CryptFileApp
import encryption

def main():
    app = QApplication(sys.argv)
    window = CryptFileApp()  
    window.show()
    sys.exit(app.exec_()) 

if __name__ == "__main__":
    try:
        encryption.load_key()
    except FileNotFoundError:
        encryption.generate_key()
        print("🔑 Wygenerowano nowy klucz szyfrowania!")

    main()  
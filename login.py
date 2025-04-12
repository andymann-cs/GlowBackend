from PySide6 import QtWidgets, QtGui, QtCore
import sys
import hashlib
import pymongo


def encrypt(password):
    return password


class LoginWidget(QtWidgets.QWidget):
    """
        A QWidget-based login interface with MongoDB authentication and custom signal on success.

        This widget presents a login form consisting of a username field, a password field (with obscured input),
        a login button, and dynamic error messaging. It authenticates users against a MongoDB Atlas database
        and emits a custom signal with the username upon successful login. The layout is styled for clarity and
        ease of use with large, accessible input fields and buttons.

        The login logic is modular and can be connected to other application components using the `login_successful` signal.

        Attributes:
            username_input (QLineEdit): Input field for the user's username.
            password_input (QLineEdit): Input field for the user's password (masked).
            login_button (QPushButton): Button to submit the login form.
            error_label (QLabel): Displays success or failure messages.
            client (MongoClient): MongoDB client connection to the remote database.
            db (Database): MongoDB database instance for user accounts.
            collection (Collection): MongoDB collection containing user credentials.
            login_successful (Signal): Custom PySide signal emitted with the username on successful login.

        Methods:
            init_ui(): Initializes the layout and UI components.
            verify_login(): Verifies user credentials and emits a success signal if valid.

        Author: Seb
        Created: 2025-03-27
    """

    login_successful = QtCore.Signal(str)  # Custom signal with username

    def __init__(self):
        super().__init__()
        self.setWindowTitle("LOGIN")
        self.setGeometry(100, 100, 900, 600)

        self.client = pymongo.MongoClient(
            "mongodb+srv://sam_user:9ireiEodVKBb3Owt@glowcluster.36bwm.mongodb.net/?retryWrites=true&w=majority&appName=GlowCluster",
            tls=True,
            tlsAllowInvalidCertificates=True
        )
        self.db = self.client["mood_tracker"]
        self.collection = self.db["accounts"]

        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()

        # Title
        title = QtWidgets.QLabel("Login")
        title.setFont(QtGui.QFont("Quicksand", 32))
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)

        # Username Field
        self.username_input = QtWidgets.QLineEdit()
        self.username_input.setPlaceholderText("Enter username:")
        self.username_input.setFont(QtGui.QFont("Quicksand", 14))
        self.username_input.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.username_input.setMinimumHeight(50)
        layout.addWidget(self.username_input)

        # Password Field
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setPlaceholderText("Enter password:")
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_input.setFont(QtGui.QFont("Quicksand", 14))
        self.password_input.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.password_input.setMinimumHeight(50)
        layout.addWidget(self.password_input)

        # Login Button
        self.login_button = QtWidgets.QPushButton("Enter")
        self.login_button.setFont(QtGui.QFont("Quicksand", 14))
        self.login_button.clicked.connect(self.verify_login)
        layout.addWidget(self.login_button)

        # Error Messages
        self.error_label = QtWidgets.QLabel()
        self.error_label.setFont(QtGui.QFont("Quicksand", 16))
        self.error_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.error_label)

        layout.addStretch()
        self.setLayout(layout)

    def verify_login(self):
        username = self.username_input.text()
        password = encrypt(self.password_input.text())

        user = self.collection.find_one({"username": username, "password": password})

        if user:
            self.error_label.setText("Login successful!")
            self.error_label.setStyleSheet("color: green")
            self.login_successful.emit(username)  # Emit signal with username
        else:
            self.error_label.setText("Username or password incorrect")
            self.error_label.setStyleSheet("color: red;")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LoginWidget()
    window.login_successful.connect(lambda username: print(f"Logged in as: {username}"))  # Test connection
    window.show()
    sys.exit(app.exec())

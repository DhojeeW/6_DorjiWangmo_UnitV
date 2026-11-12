import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox

app = QApplication(sys.argv)

# Create the main window

window = QWidget()
window.setWindowTitle("Hello PyQt6")
window.setGeometry(200, 200, 400, 250)

# Create a label

label = QLabel("Welcome to PyQt6!")

# Create a button

button = QPushButton("Click Me")

# Button click function

def show_message():
    QMessageBox.information(window, "Message", "Hello! You clicked the button.")

button.clicked.connect(show_message)

# Create layout

layout = QVBoxLayout()
layout.addWidget(label)
layout.addWidget(button)

window.setLayout(layout)

window.show()
sys.exit(app.exec())

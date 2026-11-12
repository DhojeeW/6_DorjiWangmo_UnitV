import sys

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel,
    QLineEdit, QTextEdit, QPushButton, QComboBox,
    QDateEdit, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QHBoxLayout, QGridLayout,
    QProgressBar, QMessageBox, QHeaderView
)

from PyQt6.QtCore import Qt, QDate

from task_manager import TaskStorage


class TaskManager(QMainWindow):

    def __init__(self):
        super().__init__()

        self.storage = TaskStorage()

        self.setWindowTitle("To-Do List Manager | Dorji Wangmo | Roll No. 6")
        self.setGeometry(200, 100, 1000, 700)

        # Menu bar
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)

        help_menu = menu_bar.addMenu("Help")
        about_action = help_menu.addAction("About")
        about_action.triggered.connect(self.show_about)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()

        # Heading
        title = QLabel("MY TO-DO TASK MANAGER")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title.setStyleSheet("""
            font-size: 26px;
            font-weight: bold;
            color: #263A5B;
            padding: 15px;
        """)

        subtitle = QLabel(
            "Organise your tasks. Manage your time. Stay productive."
        )
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Input form
        form_layout = QGridLayout()

        form_layout.addWidget(QLabel("Task Name:"), 0, 0)

        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter your task")
        form_layout.addWidget(self.task_input, 0, 1)

        form_layout.addWidget(QLabel("Description:"), 1, 0)

        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Enter task details")
        self.description_input.setFixedHeight(65)
        form_layout.addWidget(self.description_input, 1, 1)

        form_layout.addWidget(QLabel("Priority:"), 2, 0)

        self.priority_input = QComboBox()
        self.priority_input.addItems(["High", "Medium", "Low"])
        form_layout.addWidget(self.priority_input, 2, 1)

        form_layout.addWidget(QLabel("Due Date:"), 3, 0)

        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setMinimumDate(QDate.currentDate())
        self.date_input.setDate(QDate.currentDate())
        form_layout.addWidget(self.date_input, 3, 1)

        # Buttons
        self.add_button = QPushButton("Add Task")
        self.edit_button = QPushButton("Edit Task")
        self.delete_button = QPushButton("Delete Task")
        self.complete_button = QPushButton("Mark Complete")

        self.add_button.clicked.connect(self.add_task)
        self.edit_button.clicked.connect(self.edit_task)
        self.delete_button.clicked.connect(self.delete_task)
        self.complete_button.clicked.connect(self.complete_task)

        button_layout = QHBoxLayout()

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.complete_button)

        # Search
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search tasks...")
        self.search_input.textChanged.connect(self.search_tasks)

        # Task table
        self.task_table = QTableWidget()
        self.task_table.setColumnCount(5)

        self.task_table.setHorizontalHeaderLabels([
            "Task", "Description", "Priority", "Due Date", "Status"
        ])

        self.task_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.task_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.task_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.task_table.currentCellChanged.connect(
            self.load_selected_task
        )

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setFormat("Task Progress: %p%")

        # Arrange widgets
        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.search_input)
        main_layout.addWidget(self.task_table)
        main_layout.addWidget(self.progress_bar)

        central_widget.setLayout(main_layout)

        # Styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F2F5FA;
            }

            QLabel {
                color: #263A5B;
                font-size: 14px;
            }

            QLineEdit, QTextEdit, QComboBox, QDateEdit {
                background-color: white;
                border: 1px solid #B8C7DC;
                border-radius: 5px;
                padding: 8px;
                font-size: 13px;
            }

            QPushButton {
                background-color: #456C9B;
                color: white;
                padding: 10px;
                border-radius: 6px;
                font-size: 13px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #304F78;
            }

            QTableWidget {
                background-color: white;
                border: 1px solid #D0D9E5;
                gridline-color: #D0D9E5;
            }

            QHeaderView::section {
                background-color: #456C9B;
                color: white;
                padding: 8px;
                font-weight: bold;
            }

            QProgressBar {
                border: 1px solid #B8C7DC;
                border-radius: 5px;
                text-align: center;
                height: 20px;
            }

            QProgressBar::chunk {
                background-color: #4CAF50;
            }
        """)

        # Load previously saved tasks
        self.load_saved_tasks()

    # Add task
    def add_task(self):

        task_name = self.task_input.text().strip()

        if not task_name:
            QMessageBox.warning(
                self, "Invalid Input", "Please enter a task name."
            )
            return

        task = {
            "task": task_name,
            "description": self.description_input.toPlainText(),
            "priority": self.priority_input.currentText(),
            "due_date": self.date_input.date().toString("yyyy-MM-dd"),
            "status": "Pending"
        }

        tasks = self.storage.load_tasks()
        tasks.append(task)

        self.storage.save_tasks(tasks)

        self.display_tasks(tasks)
        self.clear_fields()

        QMessageBox.information(
            self, "Success", "Task added successfully!"
        )

    # Display tasks
    def display_tasks(self, tasks):

        self.task_table.setRowCount(0)

        for task in tasks:

            row = self.task_table.rowCount()
            self.task_table.insertRow(row)

            values = [
                task["task"],
                task["description"],
                task["priority"],
                task["due_date"],
                task["status"]
            ]

            for column, value in enumerate(values):
                self.task_table.setItem(
                    row, column, QTableWidgetItem(str(value))
                )

        self.update_progress()

    # Load saved tasks
    def load_saved_tasks(self):

        tasks = self.storage.load_tasks()
        self.display_tasks(tasks)

    # Load selected task
    def load_selected_task(self, row, column, previous_row, previous_column):

        if row < 0:
            return

        self.task_input.setText(
            self.task_table.item(row, 0).text()
        )

        self.description_input.setPlainText(
            self.task_table.item(row, 1).text()
        )

        self.priority_input.setCurrentText(
            self.task_table.item(row, 2).text()
        )

        date = QDate.fromString(
            self.task_table.item(row, 3).text(), "yyyy-MM-dd"
        )

        if date.isValid():
            self.date_input.setDate(date)

    # Edit task
    def edit_task(self):

        row = self.task_table.currentRow()

        if row < 0:
            QMessageBox.warning(
                self, "Selection Error", "Please select a task."
            )
            return

        task_name = self.task_input.text().strip()

        if not task_name:
            QMessageBox.warning(
                self, "Input Error", "Task name cannot be empty."
            )
            return

        tasks = self.storage.load_tasks()

        if row >= len(tasks):
            return

        tasks[row] = {
            "task": task_name,
            "description": self.description_input.toPlainText(),
            "priority": self.priority_input.currentText(),
            "due_date": self.date_input.date().toString("yyyy-MM-dd"),
            "status": tasks[row]["status"]
        }

        self.storage.save_tasks(tasks)
        self.display_tasks(tasks)
        self.clear_fields()

        QMessageBox.information(
            self, "Success", "Task updated successfully!"
        )

    # Delete task
    def delete_task(self):

        row = self.task_table.currentRow()

        if row < 0:
            QMessageBox.warning(
                self, "Selection Error", "Please select a task."
            )
            return

        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            "Are you sure you want to delete this task?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:

            tasks = self.storage.load_tasks()

            if row < len(tasks):
                tasks.pop(row)

                self.storage.save_tasks(tasks)
                self.display_tasks(tasks)
                self.clear_fields()

                QMessageBox.information(
                    self, "Deleted", "Task deleted successfully!"
                )

    # Complete task
    def complete_task(self):

        row = self.task_table.currentRow()

        if row < 0:
            QMessageBox.warning(
                self, "Selection Error", "Please select a task."
            )
            return

        tasks = self.storage.load_tasks()

        if row < len(tasks):
            tasks[row]["status"] = "Completed"

            self.storage.save_tasks(tasks)
            self.display_tasks(tasks)
            self.clear_fields()

            QMessageBox.information(
                self, "Success", "Task marked as completed!"
            )

    # Search tasks
    def search_tasks(self, text):

        for row in range(self.task_table.rowCount()):

            item = self.task_table.item(row, 0)

            if item:
                match = text.lower() in item.text().lower()

                self.task_table.setRowHidden(
                    row, not match
                )

    # Update progress
    def update_progress(self):

        total = self.task_table.rowCount()
        completed = 0

        for row in range(total):

            status = self.task_table.item(row, 4)

            if status and status.text() == "Completed":
                completed += 1

        percentage = int((completed / total) * 100) if total else 0

        self.progress_bar.setValue(percentage)

    # Clear fields
    def clear_fields(self):

        self.task_input.clear()
        self.description_input.clear()
        self.priority_input.setCurrentIndex(0)
        self.date_input.setDate(QDate.currentDate())
        self.task_table.clearSelection()

    # About dialog
    def show_about(self):

        QMessageBox.about(
            self,
            "About",
            "To-Do Task Manager\n\n"
            "Developed by: Dorji Wangmo\n"
            "Framework: PyQt6\n"
            "Purpose: Personal Task Management"
        )


# Run application
app = QApplication(sys.argv)

window = TaskManager()
window.show()

sys.exit(app.exec())
# To-Do List Manager

## 1. Project Description

The To-Do List Manager is a desktop application developed using Python and PyQt6. It allows users to add, edit, delete, search and mark tasks as completed. Users can also set task priorities and due dates.

The application stores task information in a JSON file so that saved tasks remain available when the application is reopened.

## 2. Requirements

- Python 3.14
- PyQt6 6.12.0
- Windows, macOS or Linux

## 3. Project Files

- `main.py` – Contains the main application interface and functionality.
- `task_manager.py` – Handles loading and saving task information.
- `tasks.json` – Stores task information.
- `requirements.txt` – Lists the required Python package and version.

## 4. Installation Instructions

1. Install Python 3.14 on your computer.
2. Download or extract the project folder.
3. Open the `ToDo_Manager` folder in VS Code or a terminal.
4. Create a virtual environment:

   `python -m venv .venv`

5. Activate the virtual environment.

   **Windows:**

   `.venv\Scripts\activate`

   **macOS/Linux:**

   `source .venv/bin/activate`

6. Install the required package:

   `python -m pip install -r requirements.txt`

## 5. Running the Application

After installing the requirements, run:

`python main.py`

The To-Do List Manager window should open.

## 6. Data Storage

Task information is stored in `tasks.json`, which is located in the same folder as `task_manager.py`.

The application loads previously saved tasks when opened and saves changes to the JSON file.

## 7. Troubleshooting

If PyQt6 is not installed correctly, run:

`python -m pip install PyQt6==6.12.0`

Make sure that the virtual environment is activated before running the application.
import tkinter as tk
from tkinter import messagebox

# Create the main window

window = tk.Tk()
window.title("Hello Tkinter")
window.geometry("400x250")
window.configure(bg="lightblue")

# Create a welcome label

label = tk.Label(
window,
text="Welcome to Tkinter!",
font=("Arial", 18, "bold"),
bg="lightblue"
)
label.pack(pady=40)

# Function for button click

def show_message():
    messagebox.showinfo("Message", "Hello! You clicked the button.")

# Create a button

button = tk.Button(
window,
text="Click Me",
command=show_message,
font=("Arial", 12)
)
button.pack()

# Run the application

window.mainloop()

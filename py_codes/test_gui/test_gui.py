import tkinter as tk
from tkinter import messagebox

def on_submit():
    name = name_entry.get()
    messagebox.showinfo("Greeting", f"Hello, {name}!")

# Main window
root = tk.Tk()
root.title("Simple Greeting App")
root.geometry("300x150")

# Label
name_label = tk.Label(root, text="Enter your name:")
name_label.pack(pady=5)

# Entry
name_entry = tk.Entry(root)
name_entry.pack(pady=5)

# Button
submit_button = tk.Button(root, text="Greet Me", command=on_submit)
submit_button.pack(pady=10)

# Run loop
root.mainloop()
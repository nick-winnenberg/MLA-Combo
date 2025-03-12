import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("MLA Combo")

# Create a label
label = tk.Label(root, text="Hello, Tkinter!")
label.pack(pady=10)

# Create a button
def on_button_click():
    label.config(text="Button Clicked!")

button = tk.Button(root, text="Click Me", command=on_button_click)
button.pack(pady=10)

# Run the application
root.mainloop()
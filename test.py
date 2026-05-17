import tkinter as tk

# Create window
root = tk.Tk()
root.title("Simple Tkinter App")
root.geometry("300x200")

# Function
def greet():
    label.config(text="Hello, World!")

# Button
button = tk.Button(root, text="Click Me", command=greet)
button.pack(pady=20)

# Label
label = tk.Label(root, text="")
label.pack()

# Run window
root.mainloop()
import tkinter as tk
import ttkbootstrap as ttk
from password_generator import generate_password

# main window
window = ttk.Window(themename="darkly")
window.title("Password Generator")
window.geometry("400x310")

# Title label
title = ttk.Label(window, text="Password Generator", font="Galibri 20 bold")
title.pack()

def generate() -> None:
    try:
        pass_length = int(length.get())
        if pass_length < 8:
            output_var.set("Length cannot be < 8")
        else:
            output_var.set(generate_password(pass_length, numbers.get(), symbols.get()))
    except ValueError:
        output_var.set("Enter a valid number")

def copy_to_clipboard():
    window.clipboard_clear()
    window.clipboard_append(output_var.get())


#variables
length = tk.StringVar(value=8)
numbers = tk.BooleanVar(value=True)
symbols = tk.BooleanVar(value=True)

#input fields
input_frame = ttk.Frame(window)
input_label = ttk.Label(master=input_frame, text="Length").pack()
input_text = ttk.Entry(input_frame, textvariable=length).pack()

checkbox1 = ttk.Checkbutton(input_frame, text="Numbers", variable=numbers).pack(pady=10)
checkbox2 = ttk.Checkbutton(input_frame, text="Symbols", variable=symbols).pack()
generate_button = ttk.Button(input_frame, text="Generate", command=generate).pack(pady=10)
input_frame.pack(pady=20)


# Output
output_var = tk.StringVar()
output = ttk.Entry(window, textvariable=output_var).pack()
copy_button = ttk.Button(window, text="Copy", command=copy_to_clipboard).pack(pady=10)

window.mainloop()

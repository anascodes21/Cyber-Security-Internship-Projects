# Developed by: Anas Ahmed
# SkillCraft Technology Internship Project
# TASK 01 - Caesar Cipher Tool

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

# --- Caesar Cipher Functions --- #

def caesar_cipher(text, shift):
    result = ""

    for char in text:
        if char.isalpha():
            base = 65 if char.isupper() else 97
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char

    return result

def encrypt_text():
    text = input_text.get("1.0", tk.END).strip()
    shift = int(shift_entry.get())
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, caesar_cipher(text, shift))

def decrypt_text():
    text = input_text.get("1.0", tk.END).strip()
    shift = int(shift_entry.get())
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, caesar_cipher(text, -shift))

def brute_force():
    text = input_text.get("1.0", tk.END).strip()
    output_text.delete("1.0", tk.END)

    for shift in range(1, 26):
        decoded = caesar_cipher(text, -shift)
        output_text.insert(tk.END, f"Shift {shift}: {decoded}\n")

# --- File Support --- #

def open_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("Text Files", "*.txt")]
    )

    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        input_text.delete("1.0", tk.END)
        input_text.insert(tk.END, content)

def save_file():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")]
    )

    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(output_text.get("1.0", tk.END))

        messagebox.showinfo("Saved", "File saved successfully!")

# --- GUI --- #

root = tk.Tk()
root.title("Advanced Caesar Cipher Tool")
root.geometry("700x600")
root.config(bg="#1e1e1e")

title = tk.Label(root, text="Caesar Cipher Tool", font=("Arial", 20, "bold"),
                 fg="white", bg="#1e1e1e")
title.pack(pady=10)

tk.Label(root, text="Input Text:", fg="white", bg="#1e1e1e").pack()

input_text = scrolledtext.ScrolledText(root, width=80, height=10)
input_text.pack(pady=5)

frame = tk.Frame(root, bg="#1e1e1e")
frame.pack()

tk.Label(frame, text="Shift Value:", fg="white", bg="#1e1e1e").grid(row=0, column=0, padx=5)

shift_entry = tk.Entry(frame, width=10)
shift_entry.grid(row=0, column=1)
shift_entry.insert(0, "3")

btn_frame = tk.Frame(root, bg="#1e1e1e")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Encrypt", width=15, command=encrypt_text).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Decrypt", width=15, command=decrypt_text).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Brute Force", width=15, command=brute_force).grid(row=0, column=2, padx=5)

tk.Button(btn_frame, text="Open File", width=15, command=open_file).grid(row=1, column=0, padx=5, pady=5)
tk.Button(btn_frame, text="Save Output", width=15, command=save_file).grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Output:", fg="white", bg="#1e1e1e").pack()

output_text = scrolledtext.ScrolledText(root, width=80, height=12)
output_text.pack(pady=5)

root.mainloop()
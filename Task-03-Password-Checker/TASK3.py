# Developed by: Anas Ahmed
# SkillCraft Technology Internship Project
# TASK 03 - Password Strength Checker 

import tkinter as tk
from tkinter import messagebox
import math
import re

# --- Common Password List --- #

common_passwords = {
    "123456", "password", "qwerty", "admin",
    "welcome", "12345678", "abc123",
    "password123", "iloveyou", "000000"
}

breached_passwords = {
    "123456", "password", "admin123",
    "letmein", "welcome123"
}

# --- Password Analysis --- #

def calculate_entropy(password):
    charset = 0

    if re.search(r"[a-z]", password):
        charset += 26
    if re.search(r"[A-Z]", password):
        charset += 26
    if re.search(r"[0-9]", password):
        charset += 10
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        charset += 32

    if charset == 0:
        return 0

    entropy = len(password) * math.log2(charset)
    return round(entropy, 2)


def check_strength(password):
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Use at least 8 characters")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add uppercase letters")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Add lowercase letters")

    if re.search(r"[0-9]", password):
        score += 1
    else:
        feedback.append("Add numbers")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        feedback.append("Add symbols")

    return score, feedback


def get_rating(score):
    if score <= 2:
        return "Weak", "red"
    elif score == 3:
        return "Medium", "orange"
    elif score == 4:
        return "Strong", "blue"
    else:
        return "Very Strong", "green"


# --- Main Checker --- #

def analyze_password():
    password = password_entry.get()

    if password == "":
        messagebox.showerror("Error", "Enter password first")
        return

    score, feedback = check_strength(password)
    rating, color = get_rating(score)

    entropy = calculate_entropy(password)

    result_label.config(text=f"Strength: {rating}", fg=color)
    score_label.config(text=f"Security Score: {score}/5")
    entropy_label.config(text=f"Entropy Score: {entropy} bits")

    if password.lower() in common_passwords:
        common_label.config(text="⚠ Common Password Detected", fg="red")
    else:
        common_label.config(text="✓ Not Common Password", fg="green")

    if password.lower() in breached_passwords:
        breach_label.config(text="⚠ Found in Data Breach", fg="red")
    else:
        breach_label.config(text="✓ No Breach Found", fg="green")

    tips_box.delete("1.0", tk.END)

    if feedback:
        for item in feedback:
            tips_box.insert(tk.END, "- " + item + "\n")
    else:
        tips_box.insert(tk.END, "Excellent password security!")


# --- Show Hide Password --- #

def toggle_password():
    if password_entry.cget("show") == "*":
        password_entry.config(show="")
        show_btn.config(text="Hide")
    else:
        password_entry.config(show="*")
        show_btn.config(text="Show")


# --- GUI --- #

root = tk.Tk()
root.title("Advanced Password Strength Checker")
root.geometry("600x600")
root.config(bg="#1e1e1e")

title = tk.Label(root,
                 text="Password Strength Checker",
                 font=("Arial", 20, "bold"),
                 fg="white",
                 bg="#1e1e1e")
title.pack(pady=15)


frame = tk.Frame(root, bg="#1e1e1e")
frame.pack(pady=10)

password_entry = tk.Entry(frame,
                          width=35,
                          font=("Arial", 14),
                          show="*")
password_entry.grid(row=0, column=0, padx=5)

show_btn = tk.Button(frame,
                     text="Show",
                     width=10,
                     command=toggle_password)
show_btn.grid(row=0, column=1)

tk.Button(root,
          text="Check Password",
          width=20,
          height=2,
          command=analyze_password).pack(pady=10)

result_label = tk.Label(root,
                        text="Strength:",
                        font=("Arial", 18, "bold"),
                        bg="#1e1e1e")
result_label.pack()

score_label = tk.Label(root,
                       text="Security Score:",
                       fg="white",
                       bg="#1e1e1e",
                       font=("Arial", 12))
score_label.pack()

entropy_label = tk.Label(root,
                         text="Entropy Score:",
                         fg="white",
                         bg="#1e1e1e",
                         font=("Arial", 12))
entropy_label.pack()

common_label = tk.Label(root,
                        text="",
                        bg="#1e1e1e",
                        font=("Arial", 12))
common_label.pack()

breach_label = tk.Label(root,
                        text="",
                        bg="#1e1e1e",
                        font=("Arial", 12))
breach_label.pack()

tk.Label(root,
         text="Security Suggestions:",
         fg="white",
         bg="#1e1e1e",
         font=("Arial", 14)).pack(pady=10)

tips_box = tk.Text(root,
                   width=60,
                   height=10,
                   font=("Arial", 11))
tips_box.pack()

root.mainloop()

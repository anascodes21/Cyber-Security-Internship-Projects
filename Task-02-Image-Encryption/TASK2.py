# Developed by: Anas Ahmed
# SkillCraft Technology Internship Project
# TASK 02 - Image Encyrption Tool

import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np

img = None
encrypted_img = None
preview_original = None
preview_encrypted = None

def load_image():
    global img, preview_original

    file_path = filedialog.askopenfilename(
        filetypes=[
            ("Image Files", "*.png *.jpg *.jpeg *.bmp")
        ]
    )

    if file_path:
        img = cv2.imread(file_path)

        if img is None:
            messagebox.showerror("Error", "Unable to load image")
            return

        preview_original = convert_for_tk(img)
        original_label.config(image=preview_original)
        original_label.image = preview_original

        status_label.config(text="Image Loaded Successfully")

# --- Image Convert --- #

def convert_for_tk(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (300, 300))

    img_pil = tk.PhotoImage(
        width=300,
        height=300
    )

    for y in range(300):
        row = ""
        for x in range(300):
            r, g, b = image[y, x]
            row += "#%02x%02x%02x " % (r, g, b)
        img_pil.put("{" + row + "}", to=(0, y))

    return img_pil

def xor_encrypt(image, key):
    return cv2.bitwise_xor(image, key)

def shift_encrypt(image, key):
    return np.uint8((image + key) % 256)

def shift_decrypt(image, key):
    return np.uint8((image - key) % 256)

def reverse_pixels(image):
    flat = image.flatten()
    flat = flat[::-1]
    return flat.reshape(image.shape)

# --- Encrypt --- #

def encrypt_image():
    global img, encrypted_img, preview_encrypted

    if img is None:
        messagebox.showerror("Error", "Load image first")
        return

    try:
        key = int(key_entry.get())
    except:
        messagebox.showerror("Error", "Enter valid key")
        return

    algo = algo_var.get()

    encrypted_img = img.copy()

    if algo == "XOR":
        encrypted_img = xor_encrypt(encrypted_img, key)

    elif algo == "Shift":
        encrypted_img = shift_encrypt(encrypted_img, key)

    elif algo == "Reverse":
        encrypted_img = reverse_pixels(encrypted_img)

    preview_encrypted = convert_for_tk(encrypted_img)

    encrypted_label.config(image=preview_encrypted)
    encrypted_label.image = preview_encrypted

    status_label.config(text="Image Encrypted")

# --- Decrypt --- #

def decrypt_image():
    global encrypted_img, preview_original

    if encrypted_img is None:
        messagebox.showerror("Error", "Encrypt image first")
        return

    try:
        key = int(key_entry.get())
    except:
        messagebox.showerror("Error", "Enter valid key")
        return

    algo = algo_var.get()

    decrypted = encrypted_img.copy()

    if algo == "XOR":
        decrypted = xor_encrypt(decrypted, key)

    elif algo == "Shift":
        decrypted = shift_decrypt(decrypted, key)

    elif algo == "Reverse":
        decrypted = reverse_pixels(decrypted)

    preview_original = convert_for_tk(decrypted)

    original_label.config(image=preview_original)
    original_label.image = preview_original

    status_label.config(text="Image Decrypted")

# --- Save --- #

def save_image():
    global encrypted_img

    if encrypted_img is None:
        messagebox.showerror("Error", "No encrypted image")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG Files", "*.png")]
    )

    if file_path:
        cv2.imwrite(file_path, encrypted_img)
        messagebox.showinfo("Saved", "Image Saved Successfully")

# --- GUI --- #

root = tk.Tk()
root.title("Advanced Image Encryption Tool")
root.geometry("760x650")
root.config(bg="#1e1e1e")

title = tk.Label(
    root,
    text="Image Encryption Tool",
    font=("Arial", 20, "bold"),
    fg="white",
    bg="#1e1e1e"
)
title.pack(pady=10)

# Top Controls
frame = tk.Frame(root, bg="#1e1e1e")
frame.pack()

tk.Button(
    frame,
    text="Load Image",
    width=15,
    command=load_image
).grid(row=0, column=0, padx=5)

tk.Label(
    frame,
    text="Key:",
    fg="white",
    bg="#1e1e1e"
).grid(row=0, column=1)

key_entry = tk.Entry(frame, width=10)
key_entry.grid(row=0, column=2)
key_entry.insert(0, "25")

algo_var = tk.StringVar()
algo_var.set("XOR")

options = tk.OptionMenu(
    frame,
    algo_var,
    "XOR",
    "Shift",
    "Reverse"
)
options.grid(row=0, column=3, padx=5)

tk.Button(
    frame,
    text="Encrypt",
    width=15,
    command=encrypt_image
).grid(row=0, column=4, padx=5)

tk.Button(
    frame,
    text="Decrypt",
    width=15,
    command=decrypt_image
).grid(row=0, column=5, padx=5)

tk.Button(
    frame,
    text="Save Image",
    width=15,
    command=save_image
).grid(row=0, column=6, padx=5)

# Image Preview
img_frame = tk.Frame(root, bg="#1e1e1e")
img_frame.pack(pady=20)

original_label = tk.Label(
    img_frame,
    bg="gray",
    width=300,
    height=300
)
original_label.grid(row=0, column=0, padx=20)

encrypted_label = tk.Label(
    img_frame,
    bg="gray",
    width=300,
    height=300
)
encrypted_label.grid(row=0, column=1, padx=20)

tk.Label(
    root,
    text="Original / Decrypted",
    fg="white",
    bg="#1e1e1e"
).pack()

tk.Label(
    root,
    text="Encrypted Preview",
    fg="white",
    bg="#1e1e1e"
).pack()

status_label = tk.Label(
    root,
    text="Ready",
    fg="lightgreen",
    bg="#1e1e1e",
    font=("Arial", 12)
)
status_label.pack(pady=10)

root.mainloop()

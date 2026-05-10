# Developed by: Anas Ahmed
# SkillCraft Technology Internship Project
# TASK 04 - Safe Keyboard Activity Logger

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from pynput import keyboard 
from datetime import datetime
from collections import Counter
import time

listener = None
logging_active = False
key_counter = Counter()
total_keys = 0
start_time = None

def current_time():
    return datetime.now().strftime("%H:%M:%S")

def log_message(msg):
    log_box.insert(tk.END, msg + "\n")
    log_box.see(tk.END)

# --- Key Press Event --- #

def on_press(key):
    global total_keys

    if not logging_active:
        return False

    try:
        k = key.char
    except:
        k = str(key).replace("Key.", "")

    total_keys += 1
    key_counter[k] += 1

    log_message(f"[{current_time()}] Key Pressed: {k}")

    update_stats()

# --- Stats --- #

def update_stats():
    elapsed = max((time.time() - start_time), 1)

    words = total_keys / 5
    wpm = round((words / elapsed) * 60, 2)

    stats_label.config(
        text=f"Total Keys: {total_keys}   |   WPM: {wpm}"
    )

def show_frequency():
    freq_box.delete("1.0", tk.END)

    for key, count in key_counter.most_common():
        freq_box.insert(tk.END, f"{key}: {count}\n")

# --- Start / Stop --- #

def start_logging():
    global listener, logging_active, start_time
    global total_keys, key_counter

    if logging_active:
        return

    total_keys = 0
    key_counter = Counter()

    logging_active = True
    start_time = time.time()

    log_message("=== Logging Started ===")

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

def stop_logging():
    global logging_active, listener

    logging_active = False

    if listener:
        listener.stop()

    log_message("=== Logging Stopped ===")
    show_frequency()

# --- Save Logs --- #

def save_logs():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")]
    )

    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(log_box.get("1.0", tk.END))

        messagebox.showinfo("Saved", "Logs exported successfully")

# --- Clear --- #

def clear_logs():
    log_box.delete("1.0", tk.END)
    freq_box.delete("1.0", tk.END)
    stats_label.config(text="Total Keys: 0 | WPM: 0")

# --- GUI --- #

root = tk.Tk()
root.title("Safe Keyboard Activity Logger")
root.geometry("900x700")
root.config(bg="#1e1e1e")

title = tk.Label(
    root,
    text="Keyboard Activity Logger",
    font=("Arial", 22, "bold"),
    fg="white",
    bg="#1e1e1e"
)
title.pack(pady=10)

subtitle = tk.Label(
    root,
    text="Visible educational input monitoring tool",
    font=("Arial", 10),
    fg="lightgreen",
    bg="#1e1e1e"
)
subtitle.pack()

# Buttons
btn_frame = tk.Frame(root, bg="#1e1e1e")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Start", width=15, command=start_logging).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Stop", width=15, command=stop_logging).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Save Logs", width=15, command=save_logs).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="Clear", width=15, command=clear_logs).grid(row=0, column=3, padx=5)

# Stats
stats_label = tk.Label(
    root,
    text="Total Keys: 0 | WPM: 0",
    fg="white",
    bg="#1e1e1e",
    font=("Arial", 12)
)
stats_label.pack(pady=5)

# Main Area
main_frame = tk.Frame(root, bg="#1e1e1e")
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Log Box
left_frame = tk.Frame(main_frame)
left_frame.pack(side="left", fill="both", expand=True, padx=5)

tk.Label(left_frame, text="Live Activity Log").pack()
log_box = ScrolledText(left_frame, width=60, height=30, font=("Consolas", 10))
log_box.pack(fill="both", expand=True)

# Frequency Box
right_frame = tk.Frame(main_frame)
right_frame.pack(side="right", fill="both", expand=True, padx=5)

tk.Label(right_frame, text="Key Frequency").pack()
freq_box = ScrolledText(right_frame, width=25, height=30, font=("Consolas", 10))
freq_box.pack(fill="both", expand=True)

# Footer
footer = tk.Label(
    root,
    text="Use only on systems you own or are authorized to test.",
    fg="orange",
    bg="#1e1e1e"
)
footer.pack(pady=5)

root.mainloop()

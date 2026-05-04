import os
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import psutil

APP_DIR = "apps"

if not os.path.exists(APP_DIR):
    os.makedirs(APP_DIR)

# ---------- Functions ----------

def scan_apps():
    app_list.delete(0, tk.END)
    for file in os.listdir(APP_DIR):
        if file.endswith(".exe"):
            app_list.insert(tk.END, file)

def add_app():
    file_path = filedialog.askopenfilename(filetypes=[("EXE Files", "*.exe")])
    if file_path:
        filename = os.path.basename(file_path)
        dest = os.path.join(APP_DIR, filename)
        os.system(f'cp "{file_path}" "{dest}"')
        scan_apps()

def run_app():
    selected = app_list.get(tk.ACTIVE)
    if not selected:
        messagebox.showwarning("No selection", "Select an app first!")
        return
    
    exe_path = os.path.join(APP_DIR, selected)
    
    try:
        subprocess.Popen(["wine", exe_path])
    except Exception as e:
        messagebox.showerror("Error", str(e))

def system_info():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    info_label.config(text=f"CPU: {cpu}% | RAM: {ram}%")

# ---------- UI ----------

root = tk.Tk()
root.title("PiLator v2")
root.geometry("500x400")

title = tk.Label(root, text="PiLator v2", font=("Arial", 18))
title.pack()

frame = tk.Frame(root)
frame.pack(pady=10)

app_list = tk.Listbox(frame, width=40, height=10)
app_list.pack(side=tk.LEFT)

scroll = tk.Scrollbar(frame)
scroll.pack(side=tk.RIGHT, fill=tk.Y)

app_list.config(yscrollcommand=scroll.set)
scroll.config(command=app_list.yview)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Scan Apps", command=scan_apps).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Add EXE", command=add_app).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Run", command=run_app).grid(row=0, column=2, padx=5)

info_label = tk.Label(root, text="CPU: -- | RAM: --")
info_label.pack(pady=10)

tk.Button(root, text="Refresh System Info", command=system_info).pack()

scan_apps()
root.mainloop()

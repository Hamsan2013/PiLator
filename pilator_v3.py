import os
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import psutil

APP_DIR = "apps"
SIMULATION_MODE = True  # Works even without Wine

if not os.path.exists(APP_DIR):
    os.makedirs(APP_DIR)

# ---------- Functions ----------

def scan_apps():
    app_list.delete(0, tk.END)
    for file in os.listdir(APP_DIR):
        if file.endswith(".exe"):
            status = "[SIM]" if SIMULATION_MODE else "[READY]"
            app_list.insert(tk.END, f"{status} {file}")

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

    exe_name = selected.split(" ", 1)[1]
    exe_path = os.path.join(APP_DIR, exe_name)

    if SIMULATION_MODE:
        messagebox.showinfo("Simulation Mode", f"Pretending to run:\n{exe_name}")
        return

    try:
        subprocess.Popen(["wine", exe_path])
    except Exception as e:
        messagebox.showerror("Error", str(e))

def toggle_mode():
    global SIMULATION_MODE
    SIMULATION_MODE = not SIMULATION_MODE
    mode_label.config(text=f"Mode: {'SIMULATION' if SIMULATION_MODE else 'REAL'}")
    scan_apps()

def system_info():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    info_label.config(text=f"CPU: {cpu}% | RAM: {ram}%")

# ---------- UI ----------

root = tk.Tk()
root.title("PiLator v3")
root.geometry("520x420")
root.configure(bg="#1e1e1e")

# Title
label = tk.Label(root, text="PiLator v3", font=("Arial", 18), fg="white", bg="#1e1e1e")
label.pack()

mode_label = tk.Label(root, text="Mode: SIMULATION", fg="cyan", bg="#1e1e1e")
mode_label.pack()

frame = tk.Frame(root, bg="#1e1e1e")
frame.pack(pady=10)

app_list = tk.Listbox(frame, width=45, height=12, bg="#2e2e2e", fg="white")
app_list.pack(side=tk.LEFT)

scroll = tk.Scrollbar(frame)
scroll.pack(side=tk.RIGHT, fill=tk.Y)

app_list.config(yscrollcommand=scroll.set)
scroll.config(command=app_list.yview)

btn_frame = tk.Frame(root, bg="#1e1e1e")
btn_frame.pack(pady=10)

btn_style = {"bg": "#333", "fg": "white", "width": 12}

tk.Button(btn_frame, text="Scan", command=scan_apps, **btn_style).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Add EXE", command=add_app, **btn_style).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Run", command=run_app, **btn_style).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="Toggle Mode", command=toggle_mode, **btn_style).grid(row=1, column=1, pady=5)

info_label = tk.Label(root, text="CPU: -- | RAM: --", fg="lightgreen", bg="#1e1e1e")
info_label.pack(pady=10)

tk.Button(root, text="Refresh System Info", command=system_info, bg="#444", fg="white").pack()

scan_apps()
root.mainloop()

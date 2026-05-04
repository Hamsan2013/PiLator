# PiLator v3 (Unified Clean Version)
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import psutil

APP_DIR = "apps"
SIMULATION_MODE = True

os.makedirs(APP_DIR, exist_ok=True)

# ---------- Core ----------
def scan_apps():
    app_list.delete(0, tk.END)
    for f in os.listdir(APP_DIR):
        if f.endswith(".exe"):
            tag = "[SIM]" if SIMULATION_MODE else "[READY]"
            app_list.insert(tk.END, f"{tag} {f}")


def add_app():
    path = filedialog.askopenfilename(filetypes=[("EXE Files", "*.exe")])
    if path:
        name = os.path.basename(path)
        dest = os.path.join(APP_DIR, name)
        try:
            subprocess.run(["cp", path, dest])
        except:
            pass
        scan_apps()


def run_app():
    sel = app_list.get(tk.ACTIVE)
    if not sel:
        messagebox.showwarning("Warning", "Select app")
        return

    exe = sel.split(" ", 1)[1]
    exe_path = os.path.join(APP_DIR, exe)

    if SIMULATION_MODE:
        messagebox.showinfo("Simulation", f"Running (fake): {exe}")
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


def update_stats():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    info.config(text=f"CPU: {cpu}% | RAM: {ram}%")

# ---------- UI ----------
root = tk.Tk()
root.title("PiLator")
root.geometry("520x420")
root.configure(bg="#1e1e1e")

header = tk.Label(root, text="PiLator", font=("Arial", 18), fg="white", bg="#1e1e1e")
header.pack()

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

btns = tk.Frame(root, bg="#1e1e1e")
btns.pack(pady=10)

style = {"bg": "#333", "fg": "white", "width": 12}

tk.Button(btns, text="Scan", command=scan_apps, **style).grid(row=0, column=0, padx=5)
tk.Button(btns, text="Add EXE", command=add_app, **style).grid(row=0, column=1, padx=5)
tk.Button(btns, text="Run", command=run_app, **style).grid(row=0, column=2, padx=5)
tk.Button(btns, text="Toggle Mode", command=toggle_mode, **style).grid(row=1, column=1, pady=5)

info = tk.Label(root, text="CPU: -- | RAM: --", fg="lightgreen", bg="#1e1e1e")
info.pack(pady=10)

tk.Button(root, text="Refresh", command=update_stats, bg="#444", fg="white").pack()

scan_apps()
root.mainloop()

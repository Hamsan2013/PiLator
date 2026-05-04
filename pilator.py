import os, subprocess, json, tkinter as tk
from tkinter import filedialog, messagebox

BASE = os.path.expanduser("~/.pilator")
APPS = os.path.join(BASE, "apps")
STORE = os.path.join(BASE, "store")
WINE_PREFIX = os.path.join(BASE, "wineprefix")

for d in [APPS, STORE, WINE_PREFIX]:
    os.makedirs(d, exist_ok=True)

SIM_MODE = True

# ---------- APP SYSTEM ----------

def scan():
    app_list.delete(0, tk.END)
    for f in os.listdir(APPS):
        if f.endswith(".exe"):
            tag = "🧪" if SIM_MODE else "⚡"
            app_list.insert(tk.END, f"{tag} {f}")

def add():
    file = filedialog.askopenfilename(filetypes=[("EXE", "*.exe")])
    if file:
        subprocess.run(["cp", file, os.path.join(APPS, os.path.basename(file))])
        scan()

def run():
    sel = app_list.get(tk.ACTIVE)
    if not sel:
        return

    exe = sel.split(" ", 1)[1]
    path = os.path.join(APPS, exe)

    if SIM_MODE:
        messagebox.showinfo("Simulation", f"Running: {exe}")
        return

    env = os.environ.copy()
    env["WINEPREFIX"] = WINE_PREFIX

    subprocess.Popen(["wine", path], env=env)

# ---------- STORE SYSTEM ----------

def load_store():
    store_list.delete(0, tk.END)
    for f in os.listdir(STORE):
        if f.endswith(".json"):
            with open(os.path.join(STORE, f)) as j:
                data = json.load(j)
                store_list.insert(tk.END, data["name"])

def install():
    sel = store_list.get(tk.ACTIVE)
    if not sel:
        return

    for f in os.listdir(STORE):
        path = os.path.join(STORE, f)
        data = json.load(open(path))

        if data["name"] == sel:
            if "url" not in data:
                messagebox.showinfo("Info", "No download link")
                return

            dest = os.path.join(APPS, data["file"])
            subprocess.run(["wget", data["url"], "-O", dest])
            messagebox.showinfo("Done", f"{data['name']} installed")
            scan()

# ---------- SYSTEM ----------

def toggle():
    global SIM_MODE
    SIM_MODE = not SIM_MODE
    scan()

# ---------- UI ----------

root = tk.Tk()
root.title("PiLator Pro")
root.geometry("600x500")

tk.Label(root, text="🚀 PiLator Pro", font=("Arial", 16)).pack()

app_list = tk.Listbox(root, width=60, height=10)
app_list.pack()

btn = tk.Frame(root)
btn.pack()

tk.Button(btn, text="Add EXE", command=add).grid(row=0, column=0)
tk.Button(btn, text="Run", command=run).grid(row=0, column=1)
tk.Button(btn, text="Toggle Mode", command=toggle).grid(row=0, column=2)

tk.Label(root, text="🛒 App Store").pack()

store_list = tk.Listbox(root, width=60, height=6)
store_list.pack()

tk.Button(root, text="Install", command=install).pack()

scan()
load_store()
root.mainloop()

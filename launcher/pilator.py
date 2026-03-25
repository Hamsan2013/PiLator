import os
import tkinter as tk
from tkinter import filedialog
from icon_detector import detect_apps

APP_FOLDER = os.path.expanduser("~/PiLator/apps")

def install_exe():

    file = filedialog.askopenfilename(filetypes=[("EXE","*.exe")])

    if file:

        os.system(f"./install_exe.sh '{file}'")

        refresh_apps()

def run_app(path):

    os.system(f"./run_app.sh '{path}'")

def refresh_apps():

    for widget in frame.winfo_children():

        widget.destroy()

    apps = detect_apps()

    for name,path in apps:

        btn = tk.Button(frame,text=name,width=30,
                        command=lambda p=path: run_app(p))

        btn.pack(pady=5)

root = tk.Tk()

root.title("PiLator v2")

root.geometry("520x420")

title = tk.Label(root,text="PiLator v2",font=("Arial",22))

title.pack(pady=10)

install = tk.Button(root,text="Install EXE",command=install_exe,height=2)

install.pack(pady=10)

frame = tk.Frame(root)

frame.pack()

refresh_apps()

root.mainloop()

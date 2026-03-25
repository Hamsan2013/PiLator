import os

APP_DIR = os.path.expanduser("~/PiLator/apps")

def detect_apps():
    apps = []

    for folder in os.listdir(APP_DIR):

        path = os.path.join(APP_DIR, folder)

        if os.path.isdir(path):

            for file in os.listdir(path):

                if file.endswith(".exe"):

                    apps.append((folder, os.path.join(path,file)))

    return apps

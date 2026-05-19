# Web EXE Runner (prototype)

This folder contains a **prototype web app** that can trigger **pre-approved Windows `.exe` files** from a web page.

Important: a browser **cannot safely run `.exe` files on the visitor's computer**. This app runs the `.exe` **on the server machine** where this app is hosted.

## What it does

- Shows a web page with buttons for allowed apps
- When you click a button, the server starts the `.exe`
- The page polls job status and shows captured output

## Safety notes (read first)

- Only allow **trusted executables**.
- Do **not** expose this publicly as-is.
- Run on a locked-down machine/account (preferably a VM).
- Keep an allowlist (this project uses `app/allowed_apps.json`).

## Run locally (Windows)

1. Install Python 3.10+
2. Create a virtual environment and install deps:
   - `python -m venv .venv`
   - `.venv\Scripts\activate`
   - `pip install -r requirements.txt`
3. Edit `app/allowed_apps.json` to point to your `.exe`
4. Start the server:
   - `python -m app.main`
5. Open:
   - `http://127.0.0.1:8000`

## Configure allowed executables

Edit `app/allowed_apps.json`:

- `id`: stable identifier used by the UI
- `label`: shown in the UI
- `path`: full path to `.exe` on the server machine
- `args`: optional default args (array)

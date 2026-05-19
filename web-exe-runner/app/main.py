from __future__ import annotations

import json
import os
import subprocess
import threading
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


BASE_DIR = Path(__file__).resolve().parent
ALLOWED_APPS_PATH = BASE_DIR / "allowed_apps.json"

MAX_RUNTIME_SECONDS = 60
POLL_INTERVAL_SECONDS = 0.2


@dataclass
class Job:
    id: str
    app_id: str
    started_at: float = field(default_factory=time.time)
    ended_at: float | None = None
    return_code: int | None = None
    output: list[str] = field(default_factory=list)
    status: str = "running"  # running | finished | failed | timeout


jobs_lock = threading.Lock()
jobs: dict[str, Job] = {}


def load_allowed_apps() -> list[dict[str, Any]]:
    try:
        data = json.loads(ALLOWED_APPS_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Invalid JSON in {ALLOWED_APPS_PATH}: {e}") from e

    if not isinstance(data, list):
        raise RuntimeError("allowed_apps.json must be a JSON array")
    return data


def get_allowed_app(app_id: str) -> dict[str, Any] | None:
    for item in load_allowed_apps():
        if isinstance(item, dict) and item.get("id") == app_id:
            return item
    return None


def _reader_thread(proc: subprocess.Popen[str], job_id: str) -> None:
    try:
        assert proc.stdout is not None
        for line in proc.stdout:
            with jobs_lock:
                job = jobs.get(job_id)
                if job is None:
                    break
                job.output.append(line.rstrip("\n"))
    except Exception as e:
        with jobs_lock:
            job = jobs.get(job_id)
            if job is not None:
                job.output.append(f"[reader error] {e}")


def _run_job(job_id: str, exe_path: str, args: list[str]) -> None:
    with jobs_lock:
        job = jobs[job_id]

    if not os.path.isabs(exe_path):
        with jobs_lock:
            job.status = "failed"
            job.ended_at = time.time()
            job.output.append("Executable path must be absolute (server-side).")
        return

    if not Path(exe_path).exists():
        with jobs_lock:
            job.status = "failed"
            job.ended_at = time.time()
            job.output.append("Executable not found on server.")
        return

    try:
        proc = subprocess.Popen(
            [exe_path, *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
    except Exception as e:
        with jobs_lock:
            job.status = "failed"
            job.ended_at = time.time()
            job.output.append(f"Failed to start process: {e}")
        return

    t = threading.Thread(target=_reader_thread, args=(proc, job_id), daemon=True)
    t.start()

    deadline = job.started_at + MAX_RUNTIME_SECONDS
    while True:
        rc = proc.poll()
        if rc is not None:
            with jobs_lock:
                job.return_code = rc
                job.ended_at = time.time()
                job.status = "finished" if rc == 0 else "failed"
            return

        if time.time() > deadline:
            try:
                proc.terminate()
            except Exception:
                pass
            with jobs_lock:
                job.status = "timeout"
                job.ended_at = time.time()
                job.output.append(f"Timed out after {MAX_RUNTIME_SECONDS} seconds.")
            return

        time.sleep(POLL_INTERVAL_SECONDS)


app = FastAPI(title="Web EXE Runner (prototype)")

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    allowed = load_allowed_apps()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "allowed": allowed,
            "max_runtime_seconds": MAX_RUNTIME_SECONDS,
        },
    )


@app.post("/api/run/{app_id}")
def run_app(app_id: str) -> dict[str, Any]:
    allowed = get_allowed_app(app_id)
    if allowed is None:
        raise HTTPException(status_code=404, detail="Unknown app id")

    exe_path = str(allowed.get("path") or "")
    args = allowed.get("args") or []
    if not isinstance(args, list) or not all(isinstance(x, str) for x in args):
        raise HTTPException(status_code=400, detail="Invalid args in allowlist")

    job_id = str(uuid.uuid4())
    job = Job(id=job_id, app_id=app_id)
    with jobs_lock:
        jobs[job_id] = job

    thread = threading.Thread(
        target=_run_job,
        args=(job_id, exe_path, args),
        daemon=True,
    )
    thread.start()

    return {"job_id": job_id}


@app.get("/api/jobs/{job_id}")
def job_status(job_id: str) -> dict[str, Any]:
    with jobs_lock:
        job = jobs.get(job_id)
        if job is None:
            raise HTTPException(status_code=404, detail="Unknown job id")
        return {
            "job_id": job.id,
            "app_id": job.app_id,
            "status": job.status,
            "started_at": job.started_at,
            "ended_at": job.ended_at,
            "return_code": job.return_code,
            "output": job.output[-500:],
        }


def main() -> None:
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=False)


if __name__ == "__main__":
    main()

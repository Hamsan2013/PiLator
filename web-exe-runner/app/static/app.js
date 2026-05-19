const statusEl = document.getElementById("status");
const logEl = document.getElementById("log");
const buttons = Array.from(document.querySelectorAll("button[data-app-id]"));

function setStatus(text) {
  statusEl.textContent = text;
}

function setLog(lines) {
  logEl.textContent = (lines || []).join("\n");
  logEl.scrollTop = logEl.scrollHeight;
}

function setButtonsDisabled(disabled) {
  buttons.forEach((b) => (b.disabled = disabled));
}

async function postJson(url) {
  const res = await fetch(url, { method: "POST" });
  if (!res.ok) {
    const msg = await res.text();
    throw new Error(msg || `Request failed: ${res.status}`);
  }
  return await res.json();
}

async function getJson(url) {
  const res = await fetch(url);
  if (!res.ok) {
    const msg = await res.text();
    throw new Error(msg || `Request failed: ${res.status}`);
  }
  return await res.json();
}

async function pollJob(jobId) {
  setStatus(`Running (${jobId})`);
  while (true) {
    const j = await getJson(`/api/jobs/${encodeURIComponent(jobId)}`);
    setLog(j.output || []);
    if (j.status !== "running") {
      setStatus(`${j.status} (exit=${j.return_code ?? "?"})`);
      return;
    }
    await new Promise((r) => setTimeout(r, 400));
  }
}

buttons.forEach((btn) => {
  btn.addEventListener("click", async () => {
    const appId = btn.getAttribute("data-app-id");
    if (!appId) return;
    setButtonsDisabled(true);
    setLog([]);
    try {
      setStatus(`Starting ${appId}...`);
      const r = await postJson(`/api/run/${encodeURIComponent(appId)}`);
      await pollJob(r.job_id);
    } catch (e) {
      setStatus("Error");
      setLog([String(e && e.message ? e.message : e)]);
    } finally {
      setButtonsDisabled(false);
    }
  });
});

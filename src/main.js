const API_BASE = "http://127.0.0.1:8142";


async function waitForBackend(maxAttempts = 40) {
  for (let i = 0; i < maxAttempts; i++) {
    try {
      const resp = await fetch(`${API_BASE}/health`);
      if (resp.ok) return true;
    } catch (e) {}
    await new Promise((r) => setTimeout(r, 500));
  }
  return false;
}

(async () => {
  const banner = document.createElement("div");
  banner.style.cssText = "position:fixed; inset:0; background:#0f1115; color:#4ade80; display:flex; align-items:center; justify-content:center; font-size:16px; z-index:9999; font-family:sans-serif;";
  banner.textContent = "Starting DPULSE, please wait...";
  document.body.appendChild(banner);

  const ready = await waitForBackend();
  banner.remove();

  if (!ready) {
    document.body.innerHTML = '<div style="padding:40px; color:red; font-family:sans-serif;">Backend failed to start. Please reinstall the application or check antivirus settings.</div>';
  }
})();


async function openMiniBrowser(url, title) {
  try {
    if (window.__TAURI__ && window.__TAURI__.core) {
      await window.__TAURI__.core.invoke("open_url", { url });
      return;
    }
    throw new Error("Tauri global API not available");
  } catch (e) {
    console.warn("Native open_url failed, falling back to window.open:", e);
    window.open(url, "_blank");
  }
}

window.addEventListener("message", (event) => {
  if (event.data && event.data.type === "dpulse-open-external" && event.data.url) {
    openMiniBrowser(event.data.url, "DPULSE External Link");
  }
});


const navButtons = document.querySelectorAll(".nav-btn");
const views = document.querySelectorAll(".view");

navButtons.forEach((btn) => {
  btn.addEventListener("click", () => {
    navButtons.forEach((b) => b.classList.remove("active"));
    views.forEach((v) => v.classList.remove("active"));

    btn.classList.add("active");
    const viewName = btn.dataset.view;
    document.getElementById(`view-${viewName}`).classList.add("active");

    if (viewName === "settings") loadSettings();
    if (viewName === "db") loadReports();
    if (viewName === "api") loadApiKeys();
  });
});


const scanForm = document.getElementById("scan-form");
const resultBox = document.getElementById("scan-result");
const resultTitle = document.getElementById("scan-result-title");
const resultContent = document.getElementById("scan-result-content");
const submitBtn = scanForm.querySelector("button[type='submit']");

const useApiCb = document.getElementById("use-api");
const apiOptions = document.getElementById("api-options");

useApiCb.addEventListener("change", () => {
  apiOptions.classList.toggle("hidden", !useApiCb.checked);
});

const snapshotModeSelect = document.getElementById("snapshot-mode");
const waybackDatesWrap = document.getElementById("wayback-dates-wrap");

snapshotModeSelect.addEventListener("change", () => {
  waybackDatesWrap.classList.toggle("hidden", snapshotModeSelect.value !== "w");
});

const snapshotPanel = document.getElementById("snapshot-panel");
const snapshotContent = document.getElementById("snapshot-content");

function renderSnapshotPanel(data, reportFolder) {
  snapshotContent.innerHTML = "";

  if (!data.snapshot_type) {
    snapshotPanel.classList.add("hidden");
    return;
  }

  snapshotPanel.classList.remove("hidden");
  const encodedFolder = encodeURIComponent(reportFolder);

  if (data.snapshot_type === "s") {
    if (data.has_screenshot) {
      const imgUrl = `${API_BASE}/snapshot/screenshot?folder=${encodedFolder}`;
      snapshotContent.innerHTML = `
        <img src="${imgUrl}" class="snapshot-image" alt="Screenshot preview" />
        <div style="margin-top:10px;">
          <button class="secondary-btn small-btn" id="open-screenshot-btn">Open full size</button>
        </div>
      `;
      document.getElementById("open-screenshot-btn").addEventListener("click", () => {
        openMiniBrowser(imgUrl, "DPULSE Screenshot");
      });
    } else {
      snapshotContent.innerHTML = `<p class="hint error-text">Screenshot could not be captured. Check that the configured browser (Settings → SNAPSHOTTING) is installed on this machine.</p>`;
    }
  } else if (data.snapshot_type === "p") {
    if (data.has_html_copy) {
      const htmlUrl = `${API_BASE}/snapshot/html?folder=${encodedFolder}`;
      snapshotContent.innerHTML = `
        <p class="hint">A raw HTML copy of the page was captured.</p>
        <button class="secondary-btn small-btn" id="open-htmlcopy-btn">View HTML Snapshot</button>
      `;
      document.getElementById("open-htmlcopy-btn").addEventListener("click", () => {
        openMiniBrowser(htmlUrl, "DPULSE HTML Snapshot");
      });
    } else {
      snapshotContent.innerHTML = `<p class="hint error-text">HTML copy could not be captured.</p>`;
    }
  } else if (data.snapshot_type === "w") {
    if (data.wayback_files && data.wayback_files.length > 0) {
      const listHtml = data.wayback_files
        .map((f) => {
          const fileUrl = `${API_BASE}/snapshot/wayback/file?folder=${encodedFolder}&filename=${encodeURIComponent(f)}`;
          return `<li>${f} <button class="secondary-btn small-btn open-wayback-file" data-url="${fileUrl}">Open</button></li>`;
        })
        .join("");
      snapshotContent.innerHTML = `
        <p class="hint">${data.wayback_files.length} archived snapshot(s) downloaded.</p>
        <ul class="wayback-list">${listHtml}</ul>
        <button class="secondary-btn small-btn" id="open-live-wayback-btn">🌐 Browse live Wayback Machine</button>
      `;
      snapshotContent.querySelectorAll(".open-wayback-file").forEach((btn) => {
        btn.addEventListener("click", () => openMiniBrowser(btn.dataset.url, "DPULSE Wayback Snapshot"));
      });
      document.getElementById("open-live-wayback-btn").addEventListener("click", () => {
        const liveUrl = `https://web.archive.org/web/*/http://${data.domain}`;
        openMiniBrowser(liveUrl, "Wayback Machine — Live");
      });
    } else {
      snapshotContent.innerHTML = `<p class="hint error-text">No archived snapshots were found for this domain in the selected date range.</p>`;
    }
  }
}

scanForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const domain = document.getElementById("domain").value.trim();
  const comment = document.getElementById("comment").value.trim();
  const snapshotMode = snapshotModeSelect.value;

  if (!domain) return;

  const payload = {
    domain,
    comment,
    use_virustotal: useApiCb.checked && document.getElementById("api-virustotal").checked,
    use_securitytrails: useApiCb.checked && document.getElementById("api-securitytrails").checked,
    hudsonrock_username: document.getElementById("hudsonrock-username").value.trim() || null,
    snapshot_mode: snapshotMode,
    wayback_from: snapshotMode === "w" ? document.getElementById("wayback-from").value.trim() : null,
    wayback_to: snapshotMode === "w" ? document.getElementById("wayback-to").value.trim() : null,
  };

  submitBtn.disabled = true;
  submitBtn.textContent = "Scanning...";

  resultBox.classList.remove("hidden");
  resultTitle.textContent = "Scanning, please wait...";
  resultContent.innerHTML = "";
  snapshotPanel.classList.add("hidden");

  try {
    const response = await fetch(`${API_BASE}/scan`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await response.json();

    if (!response.ok) {
      resultTitle.textContent = "Scan failed";
      resultContent.innerHTML = `<p class="error-text">${data.detail || "Unknown error"}</p>`;
      return;
    }

    resultTitle.textContent = `Scan completed in ${data.elapsed} (Report ID: ${data.report_id})`;
    resultContent.innerHTML = `
      <p style="margin-bottom:10px; font-size:13px; color:#999;">
        Report saved at: ${data.report_file}
      </p>
      <iframe id="report-frame"></iframe>
    `;

    const iframe = document.getElementById("report-frame");
    iframe.srcdoc = data.report_html;

    data.domain = domain;
    renderSnapshotPanel(data, data.report_folder);

  } catch (err) {
    resultTitle.textContent = "Connection error";
    resultContent.innerHTML = `<p class="error-text">Cannot reach backend: ${err.message}</p>`;
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = "Start Scan";
  }
});


async function loadSettings() {
  const container = document.getElementById("settings-container");
  container.innerHTML = `<p class="hint">Loading configuration...</p>`;

  try {
    const response = await fetch(`${API_BASE}/config`);
    const config = await response.json();

    container.innerHTML = "";

    for (const [section, options] of Object.entries(config)) {
      const sectionBox = document.createElement("div");
      sectionBox.className = "config-section";

      const title = document.createElement("h3");
      title.textContent = section;
      sectionBox.appendChild(title);

      for (const [key, value] of Object.entries(options)) {
        const row = document.createElement("div");
        row.className = "config-row";

        const label = document.createElement("span");
        label.textContent = key;
        label.className = "config-key";

        const input = document.createElement("input");
        input.type = "text";
        input.value = value;
        input.className = "config-input";

        const saveBtn = document.createElement("button");
        saveBtn.textContent = "Save";
        saveBtn.className = "secondary-btn small-btn";
        saveBtn.addEventListener("click", async () => {
          saveBtn.textContent = "Saving...";
          saveBtn.disabled = true;
          try {
            const resp = await fetch(`${API_BASE}/config`, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ section, option: key, value: input.value }),
            });
            if (resp.ok) {
              saveBtn.textContent = "Saved ✓";
              setTimeout(() => { saveBtn.textContent = "Save"; saveBtn.disabled = false; }, 1200);
            } else {
              const err = await resp.json();
              alert(`Error: ${err.detail}`);
              saveBtn.textContent = "Save";
              saveBtn.disabled = false;
            }
          } catch (err) {
            alert(`Connection error: ${err.message}`);
            saveBtn.textContent = "Save";
            saveBtn.disabled = false;
          }
        });

        row.appendChild(label);
        row.appendChild(input);
        row.appendChild(saveBtn);
        sectionBox.appendChild(row);
      }

      container.appendChild(sectionBox);
    }
  } catch (err) {
    container.innerHTML = `<p class="error-text">Failed to load config: ${err.message}</p>`;
  }
}

document.getElementById("clear-journal-btn").addEventListener("click", async () => {
  try {
    const resp = await fetch(`${API_BASE}/journal/clear`, { method: "POST" });
    if (resp.ok) {
      alert("Journal log cleared successfully");
    }
  } catch (err) {
    alert(`Error: ${err.message}`);
  }
});


async function loadReports() {
  const tbody = document.getElementById("reports-tbody");
  tbody.innerHTML = `<tr><td colspan="6" class="hint">Loading...</td></tr>`;

  try {
    const response = await fetch(`${API_BASE}/reports`);
    const reports = await response.json();

    if (reports.length === 0) {
      tbody.innerHTML = `<tr><td colspan="6" class="hint">No reports found</td></tr>`;
      return;
    }

    tbody.innerHTML = "";
    reports.forEach((r) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${r.id}</td>
        <td>${r.target}</td>
        <td>${r.comment || "-"}</td>
        <td>${r.created}</td>
        <td>${r.api_scan}</td>
        <td>
          <button class="secondary-btn small-btn" data-view-id="${r.id}">View</button>
          <button class="secondary-btn small-btn" data-delete-id="${r.id}">Delete</button>
        </td>
      `;
      tbody.appendChild(tr);
    });

    tbody.querySelectorAll("[data-view-id]").forEach((btn) => {
      btn.addEventListener("click", () => viewReport(btn.dataset.viewId));
    });
    tbody.querySelectorAll("[data-delete-id]").forEach((btn) => {
      btn.addEventListener("click", () => deleteReport(btn.dataset.deleteId));
    });

  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="6" class="error-text">Failed to load: ${err.message}</td></tr>`;
  }
}

async function viewReport(id) {
  const box = document.getElementById("report-view-box");
  const title = document.getElementById("report-view-title");
  const frame = document.getElementById("report-view-frame");

  box.classList.remove("hidden");
  title.textContent = "Loading...";

  try {
    const response = await fetch(`${API_BASE}/reports/${id}`);
    const data = await response.json();

    if (!response.ok) {
      title.textContent = "Error";
      frame.srcdoc = `<p style="color:red;">${data.detail}</p>`;
      return;
    }

    title.textContent = `Report #${data.id} — ${data.target}`;
    frame.srcdoc = data.html;
    box.scrollIntoView({ behavior: "smooth" });

  } catch (err) {
    title.textContent = "Connection error";
    frame.srcdoc = `<p style="color:red;">${err.message}</p>`;
  }
}

async function deleteReport(id) {
  if (!confirm(`Delete report #${id}? This cannot be undone.`)) return;

  try {
    const response = await fetch(`${API_BASE}/reports/${id}`, { method: "DELETE" });
    if (response.ok) {
      loadReports();
    } else {
      const err = await response.json();
      alert(`Error: ${err.detail}`);
    }
  } catch (err) {
    alert(`Connection error: ${err.message}`);
  }
}

document.getElementById("refresh-reports-btn").addEventListener("click", loadReports);


async function loadApiKeys() {
  const tbody = document.getElementById("api-keys-tbody");
  tbody.innerHTML = `<tr><td colspan="5" class="hint">Loading...</td></tr>`;

  try {
    const response = await fetch(`${API_BASE}/api-keys`);
    const keys = await response.json();

    tbody.innerHTML = "";
    keys.forEach((k) => {
      const tr = document.createElement("tr");
      const statusClass = k.is_set ? "ok" : "missing";
      tr.innerHTML = `
        <td>${k.id}</td>
        <td>${k.name}</td>
        <td class="${statusClass}">${k.masked_key}</td>
        <td>${k.limitations}</td>
        <td>
          <button class="secondary-btn small-btn" data-edit-id="${k.id}">Update key</button>
        </td>
      `;
      tbody.appendChild(tr);
    });

    tbody.querySelectorAll("[data-edit-id]").forEach((btn) => {
      btn.addEventListener("click", () => updateApiKeyPrompt(btn.dataset.editId));
    });

  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="5" class="error-text">Failed to load: ${err.message}</td></tr>`;
  }
}

async function updateApiKeyPrompt(id) {
  const newKey = prompt(`Enter new API key for ID ${id}:`);
  if (!newKey || !newKey.trim()) return;

  try {
    const response = await fetch(`${API_BASE}/api-keys/${id}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ api_key: newKey.trim() }),
    });

    if (response.ok) {
      loadApiKeys();
    } else {
      const err = await response.json();
      alert(`Error: ${err.detail}`);
    }
  } catch (err) {
    alert(`Connection error: ${err.message}`);
  }
}


document.getElementById("open-docs-btn").addEventListener("click", () => {
  window.open("https://dpulse.readthedocs.io/en/latest/", "_blank");
});

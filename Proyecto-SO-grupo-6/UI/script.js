// Frontend: solo envía la entrada al backend Python (POST /simulate)
// y renderiza lo que devuelva. Toda la lógica vive en el backend.

const $ = (id) => document.getElementById(id);

$("run").addEventListener("click", async () => {
  const btn = $("run");
  const status = $("status");
  const backend = $("backend").value.trim().replace(/\/$/, "");
  const payload = {
    procesos: $("procesos").value.trim(),
    algoritmo: $("algoritmo").value,
    quantum: parseInt($("quantum").value, 10) || 3,
  };

  btn.disabled = true;
  status.className = "status";
  status.textContent = "Enviando al backend...";

  try {
    const res = await fetch(`${backend}/simulate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    if (!res.ok || data.error) throw new Error(data.error || `HTTP ${res.status}`);

    status.className = "status ok";
    status.textContent = "Simulación completada.";
    render(data);
  } catch (e) {
    status.className = "status err";
    status.textContent = `Error: ${e.message}. ¿El backend Python está en ${backend}?`;
    console.error(e);
  } finally {
    btn.disabled = false;
  }
});

function render(data) {
  $("resultsCard").classList.remove("hidden");
  $("raw").textContent = JSON.stringify(data, null, 2);
  renderTabla(data.resultados || data.procesos || data.tabla || []);
  renderMetricas(data.metricas || data.metrics || {});
  renderGantt(data.gantt || []);
}

function renderTabla(filas) {
  const cont = $("results");
  if (!Array.isArray(filas) || filas.length === 0) {
    cont.innerHTML = "<p>Sin tabla de procesos.</p>";
    return;
  }
  const cols = Object.keys(filas[0]);
  let html = "<table><thead><tr>";
  cols.forEach((c) => (html += `<th>${c}</th>`));
  html += "</tr></thead><tbody>";
  filas.forEach((f) => {
    html += "<tr>";
    cols.forEach((c) => (html += `<td>${fmt(f[c])}</td>`));
    html += "</tr>";
  });
  html += "</tbody></table>";
  cont.innerHTML = html;
}

function renderMetricas(m) {
  const cont = $("metricas");
  const entries = Object.entries(m);
  if (entries.length === 0) { cont.innerHTML = "<p>Sin métricas.</p>"; return; }
  cont.innerHTML = entries
    .map(([k, v]) => `<div class="metric"><div class="k">${k}</div><div class="v">${fmt(v)}</div></div>`)
    .join("");
}

function renderGantt(gantt) {
  const cont = $("gantt");
  if (!Array.isArray(gantt) || gantt.length === 0) { cont.innerHTML = "<p>Sin diagrama.</p>"; return; }
  cont.innerHTML = gantt
    .map((b) => {
      if (typeof b === "string") return `<div class="blk">${b}</div>`;
      const pid = b.pid ?? b.proceso ?? b.id ?? "?";
      const ini = b.inicio ?? b.start ?? "";
      const fin = b.fin ?? b.end ?? "";
      const idle = String(pid).toLowerCase().includes("idle");
      return `<div class="blk${idle ? " idle" : ""}">${pid}<small>${ini}→${fin}</small></div>`;
    })
    .join("");
}

function fmt(v) {
  if (v === null || v === undefined) return "";
  if (typeof v === "number") return Number.isInteger(v) ? v : v.toFixed(2);
  return v;
}

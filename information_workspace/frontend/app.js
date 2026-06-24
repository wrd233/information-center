const state = {
  selectedMaterials: new Set(),
  currentTopicId: null,
  currentEventId: null,
  currentRunId: null,
};

const $ = (id) => document.getElementById(id);

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  const text = await response.text();
  const data = text ? JSON.parse(text) : null;
  if (!response.ok) {
    throw new Error(data?.detail || response.statusText);
  }
  return data;
}

function toast(message) {
  const el = $("toast");
  el.textContent = message;
  el.classList.add("show");
  setTimeout(() => el.classList.remove("show"), 2600);
}

function fmt(value) {
  if (value === null || value === undefined || value === "") return "not set";
  return String(value);
}

function chip(text, type = "") {
  return `<span class="chip ${type}">${escapeHtml(text)}</span>`;
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function renderJson(value) {
  return `<pre>${escapeHtml(JSON.stringify(value, null, 2))}</pre>`;
}

function setView(name) {
  document.querySelectorAll(".view").forEach((el) => el.classList.toggle("active", el.id === name));
  document.querySelectorAll(".nav").forEach((el) => el.classList.toggle("active", el.dataset.view === name));
}

async function loadDashboard() {
  const [health, runs, materials, candidates, events, topics] = await Promise.all([
    api("/api/health"),
    api("/api/runs"),
    api("/api/materials?limit=8&include_noise=true"),
    api("/api/events?status=candidate"),
    api("/api/events?status=official"),
    api("/api/topics"),
  ]);
  $("statusLine").textContent = `${health.status_summary.current_status}; DB ${health.database_path}`;
  $("metrics").innerHTML = [
    ["Runs", health.status_summary.runs],
    ["Materials", health.status_summary.materials],
    ["Candidates", candidates.length],
    ["Topics", topics.length],
  ]
    .map(([label, value]) => `<div class="metric"><strong>${value}</strong><span>${label}</span></div>`)
    .join("");
  $("recentRuns").innerHTML = runs.map(renderRunItem).join("") || "<p>No runs yet.</p>";
  $("recentMaterials").innerHTML = materials.items.map(renderMaterialItem).join("") || "<p>No materials yet.</p>";
}

function renderRunItem(run) {
  return `<article class="item">
    <h4>${escapeHtml(run.id)}</h4>
    <div class="meta">${escapeHtml(run.status)} · ${run.item_count} items · ${escapeHtml(run.created_at)}</div>
    <div class="chips">${chip(run.synthetic ? "synthetic" : "regular")} ${run.error_summary ? chip("error", "danger") : ""}</div>
    <button data-run="${escapeHtml(run.id)}" class="open-run">Open Run</button>
    <button data-run="${escapeHtml(run.id)}" class="process-run">Process</button>
  </article>`;
}

function renderMaterialItem(material) {
  const facets = material.light_understanding?.content_facets || [];
  return `<article class="item">
    <label class="toggle"><input type="checkbox" class="select-material" data-material="${escapeHtml(material.id)}" ${state.selectedMaterials.has(material.id) ? "checked" : ""}/> Select</label>
    <h4>${escapeHtml(material.title)}</h4>
    <div class="meta">${escapeHtml(material.source_name)} · ${escapeHtml(material.source_type)} · ${escapeHtml(material.published_at || material.created_at)}</div>
    <p>${escapeHtml(material.light_understanding?.summary || material.snippet || "")}</p>
    <div class="chips">
      ${facets.map((facet) => chip(facet, facet === "noise" ? "warn" : "")).join("")}
      ${material.ignored ? chip("ignored", "danger") : ""}
      ${material.synthetic ? chip("synthetic") : ""}
      ${material.no_original_link ? chip("no link", "warn") : ""}
    </div>
    <button data-material="${escapeHtml(material.id)}" class="open-material">Open Detail</button>
  </article>`;
}

async function uploadSingle(event) {
  event.preventDefault();
  const payload = {
    title: $("singleTitle").value,
    content_text: $("singleContent").value,
    source_name: $("singleSourceName").value,
    source_type: $("singleSourceType").value,
    url: $("singleUrl").value || null,
    auto_process: $("uploadAutoProcess").checked,
    metadata: { submitted_from_frontend: true },
  };
  const suffix = $("uploadMockLlm").checked ? "?allow_mock_llm=true" : "";
  const result = await api(`/api/materials${suffix}`, { method: "POST", body: JSON.stringify(payload) });
  $("uploadResult").textContent = JSON.stringify(result, null, 2);
  state.currentRunId = result.run_id || result.id;
  toast("Uploaded material");
  await loadRuns();
}

async function uploadBatch(event) {
  event.preventDefault();
  const items = $("batchJsonl").value
    .split(/\n+/)
    .map((line) => line.trim())
    .filter(Boolean)
    .map((line) => JSON.parse(line));
  const payload = { items, auto_process: $("uploadAutoProcess").checked, source: "frontend_jsonl" };
  const suffix = $("uploadMockLlm").checked ? "?allow_mock_llm=true" : "";
  const result = await api(`/api/materials/batch${suffix}`, { method: "POST", body: JSON.stringify(payload) });
  $("uploadResult").textContent = JSON.stringify(result, null, 2);
  state.currentRunId = result.run_id || result.id;
  toast("Uploaded batch");
  await loadRuns();
}

async function searchMaterials() {
  const params = new URLSearchParams();
  if ($("materialQuery").value) params.set("q", $("materialQuery").value);
  if ($("materialSourceType").value) params.set("source_type", $("materialSourceType").value);
  if ($("includeNoise").checked) params.set("include_noise", "true");
  if ($("includeIgnored").checked) params.set("include_ignored", "true");
  if ($("onlySynthetic").checked) params.set("synthetic", "true");
  const data = await api(`/api/materials?${params.toString()}`);
  $("materialResults").innerHTML = data.items.map(renderMaterialItem).join("") || "<p>No materials match.</p>";
  updateSelectedCount();
}

async function openMaterial(materialId) {
  const material = await api(`/api/materials/${materialId}`);
  const facets = material.light_understanding?.content_facets || [];
  $("materialDetail").innerHTML = `<h3>${escapeHtml(material.title)}</h3>
    <div class="meta">${escapeHtml(material.source_name)} · ${escapeHtml(material.source_type)} · ${escapeHtml(material.published_at || material.created_at)}</div>
    <div class="chips">
      ${facets.map((facet) => chip(facet, facet === "noise" ? "warn" : "")).join("")}
      ${material.ignored ? chip("ignored", "danger") : ""}
      ${material.synthetic ? chip("synthetic") : ""}
      ${material.no_original_link ? chip("No original link", "warn") : chip(material.url || "link")}
    </div>
    <div class="toolbar">
      <button data-material="${escapeHtml(material.id)}" class="ignore-material ${material.ignored ? "" : "danger"}">${material.ignored ? "Restore" : "Ignore"}</button>
      <button data-material="${escapeHtml(material.id)}" class="reprocess-material">Reprocess Light</button>
      <button data-material="${escapeHtml(material.id)}" class="event-from-one">Create Event</button>
      <button data-material="${escapeHtml(material.id)}" class="export-one">Export</button>
    </div>
    <h4>Light Understanding</h4>
    ${renderJson(material.light_understanding || {})}
    <h4>Original Text</h4>
    <div class="source-text">${escapeHtml(material.content_text)}</div>
    <h4>References And Trace</h4>
    ${renderJson({ run_id: material.run_id, trace_path: material.llm_trace_path, events: material.events, topics: material.topics, relations: material.relations })}`;
}

async function loadRuns() {
  const runs = await api("/api/runs");
  $("runList").innerHTML = runs.map(renderRunItem).join("") || "<p>No runs yet.</p>";
}

async function openRun(runId) {
  const run = await api(`/api/runs/${runId}`);
  state.currentRunId = runId;
  $("runDetail").innerHTML = `<h3>${escapeHtml(run.id)}</h3>
    <div class="chips">${chip(run.status, run.status === "failed" ? "danger" : "ok")} ${run.synthetic ? chip("synthetic") : ""}</div>
    <div class="toolbar"><button data-run="${escapeHtml(run.id)}" class="process-run">Process</button></div>
    <h4>Steps</h4>
    <div class="stack">${run.steps.map((step) => `<div class="item"><strong>${escapeHtml(step.step_name)}</strong> ${chip(step.status, step.status === "failed" ? "danger" : step.status === "succeeded" ? "ok" : "")}<div class="meta">in ${step.input_count} · out ${step.output_count} · failed ${step.failed_count}</div><p>${escapeHtml(step.message || "")}</p></div>`).join("")}</div>
    <h4>Materials</h4>
    <p>${run.material_ids.map((id) => `<button data-material="${escapeHtml(id)}" class="open-material">${escapeHtml(id)}</button>`).join(" ") || "None"}</p>
    <h4>Logs</h4>
    ${renderJson(run.logs)}`;
}

async function processRun(runId) {
  const allowMock = confirm("Use explicit test mock LLM for this processing call? Cancel uses configured DeepSeek.");
  const suffix = allowMock ? "?allow_mock_llm=true" : "";
  const result = await api(`/api/runs/${runId}/process${suffix}`, { method: "POST" });
  toast(`Run ${result.status}`);
  await openRun(runId);
  await searchMaterials();
  await loadEvents();
}

async function loadEvents() {
  const includeSleeping = $("includeSleepingEvents").checked;
  const [candidates, officials] = await Promise.all([
    api(`/api/events?status=candidate&include_sleeping=${includeSleeping}`),
    api(`/api/events?status=official&include_sleeping=${includeSleeping}`),
  ]);
  $("candidateEvents").innerHTML = candidates.map(renderEventItem).join("") || "<p>No candidates.</p>";
  $("officialEvents").innerHTML = officials.map(renderEventItem).join("") || "<p>No official Events.</p>";
}

function renderEventItem(event) {
  return `<article class="item">
    <h4>${escapeHtml(event.title)}</h4>
    <div class="chips">${chip(event.status, event.status === "candidate" ? "warn" : "ok")}</div>
    <button data-event="${escapeHtml(event.id)}" class="open-event">Open</button>
    ${event.status === "candidate" ? `<button data-event="${escapeHtml(event.id)}" class="promote-event">Promote</button><button data-event="${escapeHtml(event.id)}" class="ignore-candidate danger">Ignore Candidate</button>` : ""}
    ${event.status !== "candidate" ? `<button data-event="${escapeHtml(event.id)}" class="export-event">Export</button>` : ""}
  </article>`;
}

async function openEvent(eventId) {
  const event = await api(`/api/events/${eventId}`);
  state.currentEventId = eventId;
  $("eventDetail").innerHTML = `<h3>${escapeHtml(event.title)}</h3>
    <div class="chips">${chip(event.status)} ${event.user_focus ? chip("user focus") : ""}</div>
    <h4>Center Description</h4>
    ${renderJson(event.center_description)}
    <h4>Materials</h4>
    <div class="stack">${event.materials.map((item) => `<div class="item"><strong>${escapeHtml(item.material.title)}</strong><div class="meta">${escapeHtml(item.role)}</div><button data-material="${escapeHtml(item.material.id)}" class="open-material">Open Material</button></div>`).join("")}</div>
    <h4>Related Topics</h4>
    ${renderJson(event.topics)}`;
}

async function createEventFromSelected() {
  const materialIds = [...state.selectedMaterials];
  if (!materialIds.length) return toast("Select materials first");
  const allowMock = confirm("Use explicit test mock LLM for Event creation? Cancel uses configured DeepSeek.");
  const suffix = allowMock ? "?allow_mock_llm=true" : "";
  const result = await api(`/api/events/from-materials${suffix}`, {
    method: "POST",
    body: JSON.stringify({ material_ids: materialIds, user_focus: "Created from selected materials" }),
  });
  await loadEvents();
  setView("events");
  await openEvent(result.id);
}

async function loadTopics() {
  const topics = await api("/api/topics");
  $("topicList").innerHTML = topics.map(renderTopicItem).join("") || "<p>No Topics yet.</p>";
}

function renderTopicItem(topic) {
  return `<article class="item">
    <h4>${escapeHtml(topic.title)}</h4>
    <p>${escapeHtml(topic.goal)}</p>
    <div class="meta">${escapeHtml(topic.updated_at)}</div>
    <button data-topic="${escapeHtml(topic.id)}" class="open-topic">Open</button>
    <button data-topic="${escapeHtml(topic.id)}" class="refresh-topic">Refresh Structure</button>
    <button data-topic="${escapeHtml(topic.id)}" class="export-topic">Export</button>
  </article>`;
}

async function createTopic(event) {
  event.preventDefault();
  const result = await api("/api/topics", {
    method: "POST",
    body: JSON.stringify({
      title: $("topicTitle").value,
      goal: $("topicGoal").value,
      organization: $("topicOrganization").value,
      material_ids: [...state.selectedMaterials],
    }),
  });
  await loadTopics();
  await openTopic(result.id);
  toast("Topic created");
}

async function createTopicFromSelected() {
  const materialIds = [...state.selectedMaterials];
  if (!materialIds.length) return toast("Select materials first");
  const title = prompt("Topic title");
  if (!title) return;
  const goal = prompt("Topic goal / organization need") || "Organize selected materials";
  const result = await api("/api/topics", {
    method: "POST",
    body: JSON.stringify({ title, goal, organization: "", material_ids: materialIds }),
  });
  await loadTopics();
  setView("topics");
  await openTopic(result.id);
}

async function openTopic(topicId) {
  const topic = await api(`/api/topics/${topicId}`);
  state.currentTopicId = topicId;
  $("topicDetail").innerHTML = `<h3>${escapeHtml(topic.title)}</h3>
    <p>${escapeHtml(topic.goal)}</p>
    <div class="chips">${chip(`${topic.unincorporated_material_count} unincorporated`)}</div>
    <div class="toolbar">
      <button data-topic="${escapeHtml(topic.id)}" class="refresh-topic">Refresh Structure</button>
      <button data-topic="${escapeHtml(topic.id)}" class="confirm-topic">Confirm Candidate</button>
      <button data-topic="${escapeHtml(topic.id)}" class="local-refresh-topic">Local Refresh</button>
      <button data-topic="${escapeHtml(topic.id)}" class="export-topic">Export</button>
    </div>
    <h4>Material Flow</h4>
    <div class="stack">${topic.materials.map((item) => `<div class="item"><strong>${escapeHtml(item.material.title)}</strong><div class="meta">${item.referenced_by_current_structure ? "referenced" : "not referenced"}</div><button data-material="${escapeHtml(item.material.id)}" class="open-material">Open Material</button></div>`).join("") || "No materials."}</div>
    <h4>Current Structure</h4>${renderJson(topic.current_structure)}
    <h4>Candidate Structure</h4>${renderJson(topic.candidate_structure)}
    <h4>Events</h4>${renderJson(topic.events)}`;
}

async function refreshTopic(topicId) {
  const allowMock = confirm("Use explicit test mock LLM for Topic refresh? Cancel uses configured DeepSeek.");
  const result = await api(`/api/topics/${topicId}/refresh-structure`, {
    method: "POST",
    body: JSON.stringify({ include_new_materials: true, allow_mock_llm: allowMock }),
  });
  await openTopic(result.id);
}

async function exportSelectedMaterials() {
  const materialIds = [...state.selectedMaterials];
  if (!materialIds.length) return toast("Select materials first");
  const result = await api("/api/exports/material", { method: "POST", body: JSON.stringify({ material_ids: materialIds }) });
  toast(`Exported ${result.file_path}`);
}

async function refreshReports() {
  const health = await api("/api/health");
  $("reportStatus").textContent = JSON.stringify(health, null, 2);
}

function updateSelectedCount() {
  $("selectedCount").textContent = `${state.selectedMaterials.size} selected`;
}

document.addEventListener("click", async (event) => {
  const target = event.target;
  if (!(target instanceof HTMLElement)) return;
  try {
    if (target.matches(".nav")) setView(target.dataset.view);
    if (target.id === "refreshDashboard") await loadDashboard();
    if (target.id === "searchMaterials") await searchMaterials();
    if (target.id === "refreshRuns") await loadRuns();
    if (target.id === "refreshEvents") await loadEvents();
    if (target.id === "refreshTopics") await loadTopics();
    if (target.id === "refreshReports") await refreshReports();
    if (target.id === "createTopicFromSelected") await createTopicFromSelected();
    if (target.id === "createEventFromSelected") await createEventFromSelected();
    if (target.id === "exportSelectedMaterials") await exportSelectedMaterials();
    if (target.matches(".open-material")) {
      setView("materials");
      await openMaterial(target.dataset.material);
    }
    if (target.matches(".open-run")) {
      setView("runs");
      await openRun(target.dataset.run);
    }
    if (target.matches(".process-run")) await processRun(target.dataset.run);
    if (target.matches(".ignore-material")) {
      const detail = await api(`/api/materials/${target.dataset.material}`);
      await api(`/api/materials/${target.dataset.material}/${detail.ignored ? "restore" : "ignore"}`, { method: "POST" });
      await openMaterial(target.dataset.material);
    }
    if (target.matches(".reprocess-material")) {
      const allowMock = confirm("Use explicit test mock LLM for reprocess? Cancel uses configured DeepSeek.");
      await api(`/api/materials/${target.dataset.material}/reprocess-light${allowMock ? "?allow_mock_llm=true&debug=true" : "?debug=true"}`, { method: "POST" });
      await openMaterial(target.dataset.material);
    }
    if (target.matches(".event-from-one")) {
      state.selectedMaterials = new Set([target.dataset.material]);
      await createEventFromSelected();
    }
    if (target.matches(".export-one")) {
      await api("/api/exports/material", { method: "POST", body: JSON.stringify({ material_ids: [target.dataset.material] }) });
      toast("Material exported");
    }
    if (target.matches(".open-event")) await openEvent(target.dataset.event);
    if (target.matches(".promote-event")) {
      const allowMock = confirm("Use explicit test mock LLM for promotion? Cancel uses configured DeepSeek.");
      await api(`/api/events/${target.dataset.event}/promote${allowMock ? "?allow_mock_llm=true" : ""}`, { method: "POST" });
      await loadEvents();
    }
    if (target.matches(".ignore-candidate")) {
      await api(`/api/events/${target.dataset.event}/ignore-candidate`, { method: "POST" });
      await loadEvents();
    }
    if (target.matches(".export-event")) {
      const result = await api(`/api/exports/event/${target.dataset.event}`, { method: "POST" });
      toast(`Exported ${result.file_path}`);
    }
    if (target.matches(".open-topic")) await openTopic(target.dataset.topic);
    if (target.matches(".refresh-topic")) await refreshTopic(target.dataset.topic);
    if (target.matches(".confirm-topic")) {
      const result = await api(`/api/topics/${target.dataset.topic}/confirm-candidate`, { method: "POST" });
      await openTopic(result.id);
    }
    if (target.matches(".local-refresh-topic")) {
      const nodeId = prompt("Node id to refresh", "node-1");
      const instruction = prompt("Node instruction", "Tighten this node around evidence and mark unsupported claims.");
      if (nodeId && instruction) {
        const allowMock = confirm("Use explicit test mock LLM for local refresh? Cancel uses configured DeepSeek.");
        const result = await api(`/api/topics/${target.dataset.topic}/local-refresh`, {
          method: "POST",
          body: JSON.stringify({ node_id: nodeId, instruction, include_new_materials: true, allow_mock_llm: allowMock }),
        });
        await openTopic(result.id);
      }
    }
    if (target.matches(".export-topic")) {
      const result = await api(`/api/exports/topic/${target.dataset.topic}`, { method: "POST" });
      toast(`Exported ${result.file_path}`);
    }
  } catch (error) {
    toast(error.message);
  }
});

document.addEventListener("change", (event) => {
  const target = event.target;
  if (!(target instanceof HTMLInputElement)) return;
  if (target.matches(".select-material")) {
    if (target.checked) state.selectedMaterials.add(target.dataset.material);
    else state.selectedMaterials.delete(target.dataset.material);
    updateSelectedCount();
  }
});

$("singleUploadForm").addEventListener("submit", (event) => uploadSingle(event).catch((error) => toast(error.message)));
$("batchUploadForm").addEventListener("submit", (event) => uploadBatch(event).catch((error) => toast(error.message)));
$("topicForm").addEventListener("submit", (event) => createTopic(event).catch((error) => toast(error.message)));

Promise.all([loadDashboard(), searchMaterials(), loadRuns(), loadEvents(), loadTopics(), refreshReports()]).catch((error) => toast(error.message));

const seedNotes = [
  { id: 1, title: "Build the smallest useful search", body: "Start with deterministic full-text search before adding embeddings. A predictable baseline makes semantic improvements measurable.", tags: ["product", "search"], archived: false, updatedAt: "2026-10-29T10:00:00Z" },
  { id: 2, title: "Evidence should travel with AI output", body: "Every generated summary needs visible source references. Store the source note IDs and never present generated content as independently verified fact.", tags: ["ai", "trust"], archived: false, updatedAt: "2026-10-30T14:30:00Z" },
  { id: 3, title: "Local-first is a product advantage", body: "Offline access, private data, and portable exports make a knowledge tool useful before accounts and hosted infrastructure exist.", tags: ["principles", "privacy"], archived: false, updatedAt: "2026-10-31T09:15:00Z" },
  { id: 4, title: "Design the graph around questions", body: "A graph is valuable when it helps answer a question. Prefer meaningful links and labels over a dense visual network.", tags: ["product", "graph"], archived: false, updatedAt: "2026-11-01T16:20:00Z" },
  { id: 5, title: "Old launch checklist", body: "Review deployment, backups, observability, and a rollback path before sharing a new release.", tags: ["launch"], archived: true, updatedAt: "2026-10-14T08:00:00Z" }
];
const seedLinks = [{ source: 1, target: 2, label: "supports" }, { source: 1, target: 4, label: "informs" }, { source: 2, target: 3, label: "depends on" }, { source: 3, target: 4, label: "shapes" }];
const state = {
  notes: JSON.parse(localStorage.getItem("second-brain-notes") || "null") || seedNotes,
  links: JSON.parse(localStorage.getItem("second-brain-links") || "null") || seedLinks,
  selected: null, filter: "all", view: "notes", query: "", tag: ""
};
const $ = (selector) => document.querySelector(selector);
const escapeHtml = (value) => String(value).replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;" }[char]));
function persist() { localStorage.setItem("second-brain-notes", JSON.stringify(state.notes)); localStorage.setItem("second-brain-links", JSON.stringify(state.links)); }
function toast(message) { const element = $("#toast"); element.textContent = message; element.classList.add("show"); setTimeout(() => element.classList.remove("show"), 2200); }
function activeNotes() { return state.notes.filter((note) => !note.archived); }
function formatDate(date) { return new Intl.DateTimeFormat(undefined, { month: "short", day: "numeric", year: "numeric" }).format(new Date(date)); }
function allTags() { return [...new Set(state.notes.flatMap((note) => note.tags))].sort(); }
function filteredNotes() {
  let notes = state.view === "archive" ? state.notes.filter((note) => note.archived) : activeNotes();
  const query = state.query.toLowerCase().trim();
  if (query) notes = notes.filter((note) => `${note.title} ${note.body} ${note.tags.join(" ")}`.toLowerCase().includes(query));
  if (state.tag) notes = notes.filter((note) => note.tags.includes(state.tag));
  if (state.filter === "linked") notes = notes.filter((note) => state.links.some((link) => link.source === note.id || link.target === note.id));
  if (state.filter === "recent") notes = [...notes].sort((a, b) => new Date(b.updatedAt) - new Date(a.updatedAt)).slice(0, 5);
  return notes;
}
function renderTags() {
  $("#tag-filter").innerHTML = `<option value="">All tags</option>${allTags().map((tag) => `<option value="${escapeHtml(tag)}">${escapeHtml(tag)}</option>`).join("")}`;
  $("#tag-filter").value = state.tag;
}
function renderList() {
  const notes = filteredNotes();
  $("#note-count").textContent = activeNotes().length;
  $("#note-list").innerHTML = notes.length ? notes.map((note) => `
    <article class="note-card ${state.selected === note.id ? "selected" : ""}" data-note="${note.id}">
      <h3>${escapeHtml(note.title)}</h3><div class="note-preview">${escapeHtml(note.body)}</div>
      <div class="tags">${note.tags.map((tag) => `<span class="tag">${escapeHtml(tag)}</span>`).join("")}</div>
      <div class="note-meta"><span>${formatDate(note.updatedAt)}</span><span>·</span><span>${state.links.filter((link) => link.source === note.id || link.target === note.id).length} connections</span></div>
    </article>`).join("") : `<div class="empty-editor"><div class="empty-icon">⌕</div><h2>No notes found</h2><p>Try a different search or create a new note.</p></div>`;
  document.querySelectorAll("[data-note]").forEach((card) => card.addEventListener("click", () => { state.selected = Number(card.dataset.note); render(); }));
}
function renderEditor() {
  const note = state.notes.find((item) => item.id === state.selected);
  if (!note) { $("#editor-panel").innerHTML = `<div class="empty-editor"><div class="empty-icon">✎</div><h2>Select a note</h2><p>Choose an idea from your library or create a new note to start building your second brain.</p><button class="button-secondary" id="empty-new">Create your first note</button></div>`; $("#empty-new").onclick = newNote; return; }
  const connections = state.links.filter((link) => link.source === note.id || link.target === note.id);
  const options = activeNotes().filter((item) => item.id !== note.id).map((item) => `<option value="${item.id}">${escapeHtml(item.title)}</option>`).join("");
  $("#editor-panel").innerHTML = `<div class="editor-head"><div><p class="kicker">Note editor</p><h2>${escapeHtml(note.title)}</h2><div class="editor-date">Updated ${formatDate(note.updatedAt)}</div></div><div class="editor-actions"><button class="text-button" id="archive-note">${note.archived ? "Restore" : "Archive"}</button><button class="text-button" id="delete-note">Delete</button></div></div>
    <form class="editor-form" id="editor-form"><label class="form-label" for="edit-title">Title</label><input id="edit-title" value="${escapeHtml(note.title)}" maxlength="120" required><label class="form-label" for="edit-body">Your thought</label><textarea id="edit-body" required>${escapeHtml(note.body)}</textarea><label class="form-label" for="edit-tags">Tags <span class="muted">(comma separated)</span></label><input id="edit-tags" value="${escapeHtml(note.tags.join(", "))}"><div class="save-row"><span class="muted">Saved locally in your browser</span><button class="button-primary">Save changes</button></div></form>
    <div class="link-box"><h3>Connected ideas</h3>${connections.length ? connections.map((link) => { const other = state.notes.find((item) => item.id === (link.source === note.id ? link.target : link.source)); return `<div class="connection"><span>↗ ${escapeHtml(other?.title || "Unknown")} <em>· ${escapeHtml(link.label || "linked")}</em></span><button data-unlink="${other?.id}" title="Remove link">×</button></div>`; }).join("") : `<p class="muted">No connections yet.</p>`}<div class="link-row"><select id="link-target"><option value="">Link another note...</option>${options}</select><input id="link-label" placeholder="Relationship" aria-label="Relationship"><button type="button" class="button-secondary" id="add-link">Link</button></div></div>
    <div class="link-box"><h3>Export</h3><div class="actions"><button type="button" class="button-secondary" id="export-json">Download JSON</button><button type="button" class="button-secondary" id="export-markdown">Download Markdown</button></div></div>`;
  $("#editor-form").onsubmit = saveNote; $("#archive-note").onclick = () => { note.archived = !note.archived; note.updatedAt = new Date().toISOString(); persist(); toast(note.archived ? "Note archived" : "Note restored"); render(); };
  $("#delete-note").onclick = () => { if (!confirm("Delete this note?")) return; state.notes = state.notes.filter((item) => item.id !== note.id); state.links = state.links.filter((link) => link.source !== note.id && link.target !== note.id); state.selected = null; persist(); toast("Note deleted"); render(); };
  $("#add-link").onclick = () => { const target = Number($("#link-target").value); if (!target) return; state.links = state.links.filter((link) => !(link.source === note.id && link.target === target)); state.links.push({ source: note.id, target, label: $("#link-label").value.trim() || "related" }); persist(); toast("Connection added"); render(); };
  $("#export-json").onclick = () => download(`${note.title}.json`, JSON.stringify(note, null, 2), "application/json");
  $("#export-markdown").onclick = () => download(`${note.title}.md`, `# ${note.title}\n\n${note.tags.map((tag) => `#${tag}`).join(" ")}\n\n${note.body}\n`, "text/markdown");
  document.querySelectorAll("[data-unlink]").forEach((button) => button.onclick = () => { const target = Number(button.dataset.unlink); state.links = state.links.filter((link) => !((link.source === note.id && link.target === target) || (link.target === note.id && link.source === target))); persist(); render(); });
}
function download(filename, content, type) { const link = document.createElement("a"); link.href = URL.createObjectURL(new Blob([content], { type })); link.download = filename.replace(/[^\w.-]+/g, "-"); link.click(); URL.revokeObjectURL(link.href); }
function saveNote(event) { event.preventDefault(); const note = state.notes.find((item) => item.id === state.selected); note.title = $("#edit-title").value.trim(); note.body = $("#edit-body").value.trim(); note.tags = $("#edit-tags").value.split(",").map((tag) => tag.trim().toLowerCase()).filter(Boolean); note.updatedAt = new Date().toISOString(); persist(); toast("Note saved"); render(); }
function newNote() { const note = { id: Date.now(), title: "Untitled idea", body: "Capture the thought here...", tags: ["inbox"], archived: false, updatedAt: new Date().toISOString() }; state.notes.unshift(note); state.selected = note.id; state.view = "notes"; persist(); render(); setTimeout(() => { $("#edit-title").focus(); $("#edit-title").select(); }, 0); }
function renderGraph() {
  const svg = $("#graph"); const notes = activeNotes(); const width = svg.clientWidth || 700; const height = svg.clientHeight || 500; svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
  const positions = new Map(notes.map((note, index) => { const angle = (index / Math.max(notes.length, 1)) * Math.PI * 2 - Math.PI / 2; const radius = Math.min(width, height) * .31; return [note.id, { x: width / 2 + Math.cos(angle) * radius, y: height / 2 + Math.sin(angle) * radius }]; }));
  const edges = state.links.map((link) => { const a = positions.get(link.source), b = positions.get(link.target); return a && b ? `<line class="graph-edge" x1="${a.x}" y1="${a.y}" x2="${b.x}" y2="${b.y}"></line>` : ""; }).join("");
  const nodes = notes.map((note) => { const point = positions.get(note.id); return `<g class="graph-group" data-graph-note="${note.id}"><circle class="graph-node" cx="${point.x}" cy="${point.y}" r="25"></circle><text class="graph-label" x="${point.x}" y="${point.y + 44}" text-anchor="middle">${escapeHtml(note.title.length > 23 ? `${note.title.slice(0, 22)}…` : note.title)}</text></g>`; }).join("");
  svg.innerHTML = edges + nodes; $("#graph-count").textContent = `${state.links.length} connection${state.links.length === 1 ? "" : "s"}`; document.querySelectorAll("[data-graph-note]").forEach((node) => node.onclick = () => { state.selected = Number(node.dataset.graphNote); state.view = "notes"; render(); });
}
function renderArchive() { $("#archive-list").innerHTML = state.notes.filter((note) => note.archived).map((note) => `<article class="archive-row"><div><h3>${escapeHtml(note.title)}</h3><span class="muted">${escapeHtml(note.body.slice(0, 120))}</span></div><button class="button-secondary" data-restore="${note.id}">Restore</button></article>`).join("") || `<div class="empty-editor"><h2>Nothing archived</h2><p>Archived notes will appear here.</p></div>`; document.querySelectorAll("[data-restore]").forEach((button) => button.onclick = () => { const note = state.notes.find((item) => item.id === Number(button.dataset.restore)); note.archived = false; persist(); render(); }); }
function render() { $("#notes-view").classList.toggle("hidden", state.view !== "notes"); $("#graph-view").classList.toggle("hidden", state.view !== "graph"); $("#archive-view").classList.toggle("hidden", state.view !== "archive"); $("#page-title").textContent = state.view === "graph" ? "Knowledge graph" : state.view === "archive" ? "Archive" : "Notes"; renderTags(); if (state.view === "notes") { renderList(); renderEditor(); } if (state.view === "graph") renderGraph(); if (state.view === "archive") renderArchive(); }
document.querySelectorAll(".nav-item").forEach((button) => button.onclick = () => { state.view = button.dataset.view; document.querySelectorAll(".nav-item").forEach((item) => item.classList.toggle("active", item === button)); render(); });
document.querySelectorAll(".filter").forEach((button) => button.onclick = () => { state.filter = button.dataset.filter; document.querySelectorAll(".filter").forEach((item) => item.classList.toggle("active", item === button)); render(); });
$("#search").oninput = (event) => { state.query = event.target.value; render(); };
$("#tag-filter").onchange = (event) => { state.tag = event.target.value; render(); };
$("#new-note").onclick = newNote; $("#empty-new").onclick = newNote;
$("#reset-demo").onclick = () => { if (!confirm("Reset the workspace to the showcase notes?")) return; localStorage.removeItem("second-brain-notes"); localStorage.removeItem("second-brain-links"); location.reload(); };
document.addEventListener("keydown", (event) => { if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") { event.preventDefault(); $("#search").focus(); } });
render();

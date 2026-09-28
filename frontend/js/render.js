// ==========================================================================
// RENDER — montagem do HTML no DOM (hero, eventos e autoridades)
// ==========================================================================
// Onde estava:  antigo app.js (blocos "Render: hero", "Render: lista de
//               eventos" e "Render: contadores", linhas 106–276).
// Usos:         funções exportadas chamadas por ui.js e main.js.
// --------------------------------------------------------------------------

import { API_BASE_URL, PAGE_SIZE, ROLE_LABELS, state } from "./config.js";
import { apiGet, extractList } from "./api.js";
import {
  formatDateLabel,
  todayISO,
  safeText,
  extractTime,
  extractRole,
  normalizeRoleKey,
} from "./format.js";

// --------------------------------------------------------------------------
// Hero: data de hoje, status da API, contadores e "Hoje na agenda"
// --------------------------------------------------------------------------
export async function loadHero() {
  document.getElementById("hero-date").textContent = formatDateLabel(new Date());
  const statusEl = document.getElementById("api-status");
  const listEl = document.getElementById("today-list");

  try {
    const today = todayISO();
    const payload = await apiGet("/events", { date: today, limit: 50 });
    const { items } = extractList(payload);

    statusEl.textContent = "conectado";
    statusEl.classList.add("is-ok");

    renderStats(items);
    renderTodayList(items, listEl);
  } catch (err) {
    console.error(err);
    statusEl.textContent = "API offline";
    statusEl.classList.add("is-error");
    listEl.innerHTML = `<li class="today-card__empty">
      Não foi possível conectar à API em <code>${API_BASE_URL}</code>.
      Verifique se ela está rodando e se o CORS está liberado.
    </li>`;
  }
}

function renderStats(events) {
  const counts = { president: 0, vice_president: 0, first_lady: 0 };
  events.forEach((event) => {
    const key = normalizeRoleKey(extractRole(event));
    if (counts[key] !== undefined) counts[key] += 1;
  });

  document.querySelectorAll("[data-count]").forEach((el) => {
    const key = el.getAttribute("data-count");
    el.textContent = counts[key] ?? 0;
  });
}

function renderTodayList(events, listEl) {
  if (!events.length) {
    listEl.innerHTML = `<li class="today-card__empty">Nenhum compromisso registrado para hoje ainda.</li>`;
    return;
  }

  listEl.innerHTML = events
    .slice(0, 8)
    .map((event) => {
      const role = normalizeRoleKey(extractRole(event));
      return `
        <li class="today-item">
          <span class="today-item__bar today-item__bar--${role}"></span>
          <span class="today-item__time">${extractTime(event)}</span>
          <span class="today-item__body">
            <span class="today-item__title">${safeText(event.title, "Compromisso oficial")}</span>
            <span class="today-item__loc">${safeText(event.location, "Local não informado")}</span>
          </span>
        </li>`;
    })
    .join("");
}

// --------------------------------------------------------------------------
// Lista de eventos com filtros, ordenação e paginação
// --------------------------------------------------------------------------
export async function loadEvents({ append = false } = {}) {
  if (state.loading) return;
  state.loading = true;

  const listEl = document.getElementById("event-list");
  const countEl = document.getElementById("results-count");
  const loadMoreBtn = document.getElementById("load-more");

  if (!append) {
    listEl.innerHTML = `
      <li class="event-skeleton"></li>
      <li class="event-skeleton"></li>
      <li class="event-skeleton"></li>`;
  }

  try {
    const payload = await apiGet("/events", {
      authority: state.role,
      date: state.date,
      search: state.search,
      location: state.location,
      limit: PAGE_SIZE,
      offset: state.offset,
    });

    const { items, total } = extractList(payload);
    const sorted = sortEvents(items, state.sort);

    if (!append) listEl.innerHTML = "";

    if (!sorted.length && !append) {
      listEl.innerHTML = `<li class="event-list__empty">Nenhum evento encontrado com esses filtros.</li>`;
    } else {
      listEl.insertAdjacentHTML("beforeend", sorted.map(renderEventItem).join(""));
    }

    countEl.textContent = total
      ? `${total} evento${total === 1 ? "" : "s"} encontrado${total === 1 ? "" : "s"}`
      : "Nenhum resultado";

    const loadedSoFar = state.offset + items.length;
    loadMoreBtn.hidden = items.length < PAGE_SIZE || (total && loadedSoFar >= total);
  } catch (err) {
    console.error(err);
    if (!append) {
      listEl.innerHTML = `<li class="event-list__error">
        Erro ao consultar a API em <code>${API_BASE_URL}/events</code>. Confirme se ela está no ar.
      </li>`;
    }
    document.getElementById("load-more").hidden = true;
  } finally {
    state.loading = false;
  }
}

function sortEvents(events, direction) {
  const copy = [...events];
  copy.sort((a, b) => {
    const dateA = new Date(a.datetime || a.start || 0).getTime();
    const dateB = new Date(b.datetime || b.start || 0).getTime();
    return direction === "asc" ? dateA - dateB : dateB - dateA;
  });
  return copy;
}

function renderEventItem(event) {
  const role = normalizeRoleKey(extractRole(event));
  const roleLabel = ROLE_LABELS[role] || "Autoridade";
  const rawDate = event.datetime || event.start || "";
  const dateLabel = rawDate ? String(rawDate).slice(0, 10) : "—";

  return `
    <li class="event-item event-item--${role}">
      <span class="event-item__date">${dateLabel}</span>
      <span class="event-item__time">${extractTime(event)}</span>
      <span>
        <p class="event-item__title">${safeText(event.title, "Compromisso oficial")}</p>
        <p class="event-item__loc">${safeText(event.location, "Local não informado")}</p>
      </span>
      <span class="event-item__role event-item__role--${role}">${roleLabel}</span>
    </li>`;
}

// --------------------------------------------------------------------------
// Contadores por autoridade (seção "Autoridades monitoradas")
// --------------------------------------------------------------------------
export async function loadAuthorityCounts() {
  const roles = ["president", "vice_president", "first_lady"];

  await Promise.all(
    roles.map(async (role) => {
      const el = document.querySelector(`[data-authority-count="${role}"]`);
      if (!el) return;
      try {
        const payload = await apiGet("/events", { authority: role, limit: 1 });
        const { total } = extractList(payload);
        el.textContent = `${total ?? "—"} eventos registrados`;
      } catch {
        el.textContent = "dados indisponíveis";
      }
    })
  );
}
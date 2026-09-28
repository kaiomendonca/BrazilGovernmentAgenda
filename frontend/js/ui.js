// ==========================================================================
// UI — eventos de interface (filtros, ordenação, paginação e "Limpar")
// ==========================================================================
// Onde estava:  antigo app.js (bloco "Eventos de UI", linhas 278–332).
// Usos:         importado por main.js.
// --------------------------------------------------------------------------

import { PAGE_SIZE, state } from "./config.js";
import { loadEvents } from "./render.js";

export function setupFilterUI() {
  const form = document.getElementById("filters");
  const roleButtons = document.querySelectorAll(".role-btn");
  const dateInput = document.getElementById("filter-date");
  const searchInput = document.getElementById("filter-search");
  const locationInput = document.getElementById("filter-location");
  const sortSelect = document.getElementById("sort-select");
  const loadMoreBtn = document.getElementById("load-more");
  const clearBtn = document.getElementById("clear-filters");

  // Filtros rápidos por autoridade (botões "Todas", "Presidente", etc.)
  roleButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      roleButtons.forEach((b) => b.classList.remove("is-active"));
      btn.classList.add("is-active");
      state.role = btn.dataset.role;
      state.offset = 0;
      loadEvents();
    });
  });

  // Submit do formulário: aplica data, busca e local escolhidos
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    state.date = dateInput.value;
    state.search = searchInput.value.trim();
    state.location = locationInput.value.trim();
    state.offset = 0;
    loadEvents();
  });

  // Alteração da ordenação recarrega a lista desde o início
  sortSelect.addEventListener("change", () => {
    state.sort = sortSelect.value;
    state.offset = 0;
    loadEvents();
  });

  // "Carregar mais" avança o offset e reutiliza a mesma consulta
  loadMoreBtn.addEventListener("click", () => {
    state.offset += PAGE_SIZE;
    loadEvents({ append: true });
  });

  // Botão "Limpar" restaura todos os filtros ao estado inicial
  clearBtn.addEventListener("click", () => {
    dateInput.value = "";
    searchInput.value = "";
    locationInput.value = "";
    sortSelect.value = "desc";
    roleButtons.forEach((b) => b.classList.remove("is-active"));
    document.querySelector('.role-btn[data-role=""]').classList.add("is-active");

    Object.assign(state, { role: "", date: "", search: "", location: "", sort: "desc", offset: 0 });
    loadEvents();
  });
}
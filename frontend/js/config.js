// ==========================================================================
// CONFIG — constantes globais e estado da aplicação
// ==========================================================================
// Onde estava:  antigo app.js (bloco "Configuração", linhas 1–24).
// Usos:         importado por api.js, render.js e ui.js.
// --------------------------------------------------------------------------

// Troque pela URL onde a sua API FastAPI está rodando.
// Local: http://localhost:8000  |  Produção: https://sua-api.exemplo.com
export const API_BASE_URL = "http://localhost:8000";

export const ROLE_LABELS = {
  president: "Presidente",
  vice_president: "Vice-Presidente",
  first_lady: "Primeira-Dama",
};

export const PAGE_SIZE = 12;

export const state = {
  role: "",
  date: "",
  search: "",
  location: "",
  sort: "desc",
  offset: 0,
  loading: false,
};
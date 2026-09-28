// ==========================================================================
// FORMAT — funções de formatação e normalização de dados
// ==========================================================================
// Onde estava:  antigo app.js (bloco "Formatação", linhas 57–104).
// Usos:         importado por render.js.
// --------------------------------------------------------------------------

// Ex.: "segunda-feira, 14 de setembro"
export function formatDateLabel(date) {
  return new Intl.DateTimeFormat("pt-BR", {
    weekday: "long",
    day: "2-digit",
    month: "long",
  }).format(date);
}

// Data de hoje no padrão ISO (AAAA-MM-DD), usada nos filtros e na API.
export function todayISO() {
  return new Date().toISOString().slice(0, 10);
}

// Retorna o valor ou um texto substituto quando estiver vazio.
export function safeText(value, fallback = "Sem informação") {
  if (!value) return fallback;
  return String(value);
}

// Tenta extrair um horário legível do campo `start` ou `datetime` do evento.
export function extractTime(event) {
  const raw = event.start || event.datetime || "";
  const match = String(raw).match(/(\d{1,2}:\d{2})/);
  return match ? match[1] : "—";
}

// Identifica o cargo da autoridade dona do evento.
export function extractRole(event) {
  // Alguns endpoints retornam `role` direto; outros trazem `authorities: [...]`
  if (event.role) return event.role;
  if (Array.isArray(event.authorities) && event.authorities[0]?.role) {
    return event.authorities[0].role;
  }
  return null;
}

// Mapeia os formatos de cargo usados pela API para as "keys" do front
// (president, vice_president, first_lady), que também viram classes CSS.
const ROLE_KEY_MAP = {
  "presidente-da-republica": "president",
  "vice-presidente": "vice_president",
  "primeira-dama": "first_lady",
  president: "president",
  vice_president: "vice_president",
  first_lady: "first_lady",
};

export function normalizeRoleKey(role) {
  return ROLE_KEY_MAP[role] || role || "president";
}
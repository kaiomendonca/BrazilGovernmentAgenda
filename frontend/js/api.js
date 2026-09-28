// ==========================================================================
// API — camada de comunicação com o backend (fetch + normalização)
// ==========================================================================
// Onde estava:  antigo app.js (bloco "Helpers de API", linhas 26–55).
// Usos:         importado por render.js.
// --------------------------------------------------------------------------

import { API_BASE_URL } from "./config.js";

// Faz um GET montando a query string apenas com parâmetros preenchidos.
export async function apiGet(path, params = {}) {
  const url = new URL(API_BASE_URL + path);
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "") {
      url.searchParams.set(key, value);
    }
  });

  const response = await fetch(url.toString(), {
    method: "GET",
    headers: { Accept: "application/json" },
  });

  if (!response.ok) {
    throw new Error(`Erro ${response.status} ao consultar ${path}`);
  }
  return response.json();
}

// A API pode devolver a lista direto ou dentro de um envelope { items, total }.
// Isso normaliza os dois formatos sem quebrar o front.
export function extractList(payload) {
  if (Array.isArray(payload)) return { items: payload, total: payload.length };
  if (Array.isArray(payload.items)) return { items: payload.items, total: payload.total ?? payload.items.length };
  if (Array.isArray(payload.results)) return { items: payload.results, total: payload.total ?? payload.results.length };
  return { items: [], total: 0 };
}
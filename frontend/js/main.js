// ==========================================================================
// MAIN — ponto de entrada da aplicação (bootstrap)
// ==========================================================================
// Onde estava:  antigo app.js (bloco "Init", linhas 334–342).
// Usos:         arquivo carregado como <script type="module"> no index.html.
// --------------------------------------------------------------------------

import { setupFilterUI } from "./ui.js";
import { loadHero, loadEvents, loadAuthorityCounts } from "./render.js";

document.addEventListener("DOMContentLoaded", () => {
  // Conecta os listeners do formulário de filtros
  setupFilterUI();

  // Cargas iniciais de dados
  loadHero();           // hero: data, status da API, contadores e "Hoje na agenda"
  loadEvents();         // lista principal de eventos (com filtros padrão)
  loadAuthorityCounts(); // contadores da seção "Autoridades monitoradas"
});
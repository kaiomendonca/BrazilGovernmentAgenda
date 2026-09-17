# BrazilGovernmentAgenda

API Web desenvolvida com FastAPI que coleta, normaliza e disponibiliza dados públicos das agendas oficiais de autoridades do Governo Federal, como Presidente, Vice-Presidente e Primeira-Dama, a partir das APIs públicas de agenda.

Os dados são processados e persistidos em SQLite utilizando SQLAlchemy, permitindo consultas centralizadas e padronizadas por meio de endpoints REST.

O projeto tem como objetivo facilitar o acesso, consulta e análise de informações públicas, oferecendo uma fonte centralizada para cidadãos acompanharem compromissos oficiais e para organizações analisarem a agenda pública das autoridades como insumo para planejamento, acompanhamento institucional e tomada de decisões.

## O que o projeto faz

- Coleta: constrói, para cada dia de um intervalo de datas, a URL pública da
  agenda da autoridade solicitada, faz a requisição HTTP (`requests`) e extrai
  os eventos (compromissos) retornados pela API.
- Normaliza: mapeia cada evento para o modelo de dados `Event` e detecta a
  autoridade/role a partir do `href` do evento.
- Persiste: salva eventos e a relação evento-autoridade no banco SQLite,
  evitando duplicações.
- Expõe: disponibiliza os dados via API REST (FastAPI) com endpoints de leitura
  de eventos e autoridades.

## Fontes de dados

### API do Planalto (fluxo atual)

Base: `https://www.gov.br/planalto/pt-br`

| Autoridade       | Caminho da API (JSON por data)                                        |
|------------------|------------------------------------------------------------------------|
| `president`      | `/acompanhe-o-planalto/agenda-do-presidente-da-republica-lula/agenda-do-presidente-da-republica/json/` |
| `vice_president` | `/vice-presidencia/agenda-vice-presidente-geraldo-alckmin/agenda-do-vice-presidente-geraldo-alckmin/json/` |
| `first_lady`     | `/acompanhe-o-planalto/agenda-da-primeira-dama/agenda-da-primeira-dama/json/` |

Retorno esperado da API: lista de dias, cada dia com o campo `isSelected`; o
evento compromisso fica em `day["items"]`.

### e-Agendas

O e-Agendas unificou as agendas de todas as autoridades em um só lugar — algo que
antes era feito por este projeto, que coletava os dados dessas APIs uma a uma.
Atualmente trabalhamos na ideia de consumir os dados do e-Agendas com o objetivo
de organizá-los de forma mais legível e acessível a qualquer tipo de público.

## Estrutura do projeto

```
BrazilGovernmentAgenda/
├── app/
│   ├── main.py                         # Entrypoint FastAPI (create_app, /health)
│   ├── schemas.py                      # Pydantic models (EventOut, AuthorityOut, responses)
│   ├── core/
│   │   ├── dependencies.py             # contextmanager get_db() (sessão/commit/rollback)
│   │   └── logger.py                   # Logger colorido (dev) ou JSON (prod)
│   ├── database/
│   │   └── connection.py               # engine, SessionLocal, Base, init_db()
│   ├── models/
│   │   └── agenda.py                   # Entidades Event, Authorities e enum PubliclyExposedPersons
│   ├── repositories/
│   │   ├── authority_repository.py     # persiste relação autoridade x evento
│   │   └── event_repository.py         # salva eventos com deduplicação por href e lista
│   ├── router/
│   │   ├── events.py                   # GET /events e GET /events/{event_id}
│   │   └── authorities.py              # GET /authorities
│   ├── services/
│   │   ├── agenda_service.py           # orquestra o fluxo Planalto
│   │   └── request_service.py          # requisição HTTP e extração dos events
│   └── utils/
│       ├── authority_utils.py          # mapeia slug do href -> enum de role
│       ├── date_utils.py               # gera lista de datas entre duas datas
│       └── url_builder.py              # monta URL da API do Planalto
├── Note/                               # anotações de planejamento (Redis, mocks, etc.)
├── tests/                              # testes unitários (pytest)
├── government.db                       # banco SQLite (ignorado pelo git)
├── requirements.txt
└── .env                                # configuração (ver abaixo)
```

## Fluxo de dados (Planalto)

```
process_agenda(official_name, start_date, end_date)
  ├─ init_db()
  ├─ date_list = generate_dates(start, end)          # lista de datas %
  └─ for date in date_list:
        url = build_official_url(name, date)         # URL da API JSON
        events = request_data(url)                   # chamada HTTP + extração
        EventRepository(session).save(events)        # persistência
            └─ AuthorityRepository.save_for_event(event, href)
```

Os dados coletados são então expostos pela API REST (endpoints em `router/`).

Detalhes:

- `generate_dates` — valida formato `%Y-%m-%d`, rejeita datas inválidas ou
  intervalos invertidos (lança erro de validação).
- `request_data` — envia headers de navegador, loga a requisição e retorna os
  eventos do dia com `isSelected == True`. Retorna `None` em erro de rede.
- `EventRepository.save` — cria evento apenas se `href` ainda não existe;
  para evento já existente, apenas garante a associação com a autoridade
  (sem duplicar).
- `AuthorityRepository.save_for_event` — deriva o role pelo slug no `href`
  (`presidente-da-republica`, `vice-presidente`, `primeira-dama`) e insere a
  linha em `authorities` se ainda não existir.

## Modelo de dados

### `Event` (tabela `events`)

| Coluna   | Tipo    | Notas              |
|----------|---------|--------------------|
| `_id`    | Integer | PK, indexado       |
| `datetime` | String | indexado         |
| `href`   | String  | indexado (dedup)  |
| `location` | String | indexado          |
| `start`  | String  | indexado           |
| `title`  | String  | indexado           |

### `Authorities` (tabela `authorities`)

| Coluna     | Tipo   | Notas                              |
|------------|--------|------------------------------------|
| `_id`      | Integer| PK, indexado                       |
| `role`     | Enum   | `presidente-da-republica`, `vice-presidente`, `primeira-dama` |
| `event_id` | Integer| FK -> `events._id`                 |

## Como rodar

```bash
# dependências
pip install -r requirements.txt

# subir a API
python -m app.main
# ou
uvicorn app.main:app --reload
```

A API sobe em `http://localhost:8000` e a documentação interativa (Swagger)
fica em `http://localhost:8000/docs`.

A coleta é executada via código, usando a função `process_agenda`:

```python
from app.services.agenda_service import process_agenda

process_agenda("president", "2026-01-01", "2026-01-05")
```

## Endpoints

| Método | Caminho                 | Descrição                                         |
|--------|-------------------------|---------------------------------------------------|
| GET    | `/health`               | Health check (`{"status": "ok"}`)                |
| GET    | `/events`               | Lista eventos (filtros: `authority`, `date`, `location`, `search`; paginação `limit`/`offset`) |
| GET    | `/events/{event_id}`    | Retorna um evento pelo ID                         |
| GET    | `/authorities`          | Lista autoridades (filtros: `role`, `event_id`; paginação `limit`/`offset`) |

Parâmetros de autoridade/role:

- `president`, `vice_president` ou `first_lady`

## Configuração (.env)

| Variável        | Descrição                                            |
|-----------------|------------------------------------------------------|
| `DATABASE_URL`  | URL de conexão do banco (padrão local: `sqlite:///government.db`) |
| `LOG_LEVEL`     | `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`     |
| `ENVIRONMENT`   | `development` (log colorido) ou `production` (log JSON) |

## Testes

```bash
pytest
```

Testes existentes:

- `tests/utils/test_date_utils.py` — `generate_dates` (datas válidas, dia único, inválidas, intervalo invertido).
- `tests/utils/test_url_builder.py` — `build_official_url` (nomes válidos/inválidos).
- `tests/utils/test_authority_utils.py` — resolução de role pelo `href`.
- `tests/services/test_request_service.py` — `request_data` (extração de eventos e erro de rede) usando mocks.
- `tests/repositories/test_event_repository.py` — salvamento e não-duplicação de eventos, com fixture `db_session` (SQLite em memória).

## Roadmap / notas

- **e-Agendas**: consumir os dados já unificados pelo e-Agendas e organizá-los de
  forma legível e acessível ao público.
- **Consulta**: expandir as funções de leitura além do atual (`list_events`, `get_by_id`, `list_authorities`) e adicionar regras específicas de negócio.
- **Python date/time**: padronizar data e fuso horário em `datetime` (branch `chore/iso-8601-date-standard`).
- **Redis**: cache para datas futuras (TTL) e Postgres como histórico de dados passados (ver `Note/redis.txt`).
- **Ferramentas**: poetry, ruff, pre-commit e pipelines de CI/CD.
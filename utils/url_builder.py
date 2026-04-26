def build_official_url(name, date):
    GOV_AGENDA_BASE_URL = "https://www.gov.br/planalto/pt-br"

    base_urls = {
        "president": (
            GOV_AGENDA_BASE_URL + "/acompanhe-o-planalto"
            "/agenda-do-presidente-da-republica-lula"
            "/agenda-do-presidente-da-republica/json/"
        ),
        "vice_president": (
            GOV_AGENDA_BASE_URL + "/vice-presidencia"
            "/agenda-vice-presidente-geraldo-alckmin"
            "/agenda-do-vice-presidente-geraldo-alckmin/json/"
        ),
        "first_lady": (
            GOV_AGENDA_BASE_URL + "/acompanhe-o-planalto"
            "/agenda-da-primeira-dama/agenda-da-primeira-dama/json/"
        ),
    }

    if name not in base_urls:
        raise ValueError("Invalid official name")

    return f"{base_urls[name]}{date}"
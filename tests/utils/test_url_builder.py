from app.utils.url_builder import build_official_url
import pytest

class TestBuildOfficialUrl:
    
    GOV_AGENDA_BASE_URL = "https://www.gov.br/planalto/pt-br"

    @pytest.mark.parametrize(
        "role, expected_url",
        [
            (
                "president",
                (
                    GOV_AGENDA_BASE_URL
                    + "/acompanhe-o-planalto"
                    "/agenda-do-presidente-da-republica-lula"
                    "/agenda-do-presidente-da-republica/json/"
                ),
            ),
            (
                "vice_president",
                (
                    GOV_AGENDA_BASE_URL
                    + "/vice-presidencia"
                    "/agenda-vice-presidente-geraldo-alckmin"
                    "/agenda-do-vice-presidente-geraldo-alckmin/json/"
                ),
            ),
            (
                "first_lady",
                (
                    GOV_AGENDA_BASE_URL
                    + "/acompanhe-o-planalto"
                    "/agenda-da-primeira-dama"
                    "/agenda-da-primeira-dama/json/"
                ),
            ),
        ],
    )
    def test_valid_names_for_official_build_url(self, role, expected_url):
        assert build_official_url(role, "2026-01-01") == expected_url + "2026-01-01"
        
        
    
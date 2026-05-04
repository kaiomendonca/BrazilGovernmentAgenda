from app.utils.authority_utils import get_authority_from_href, ROLE_MAPPING
import pytest
from app.models.agenda import PubliclyExposedPersons


class TestAuthorityHref:
        
    GOV_AGENDA_BASE_URL = "https://www.gov.br/planalto/pt-br"

    @pytest.mark.parametrize(
        "href, expected_role",
        [
            (
                GOV_AGENDA_BASE_URL
                + "/acompanhe-o-planalto"
                "/agenda-do-presidente-da-republica-lula"
                "/agenda-do-presidente-da-republica/json/",
                PubliclyExposedPersons.PRESIDENT,
            ),
            (
                GOV_AGENDA_BASE_URL
                + "/vice-presidencia"
                "/agenda-vice-presidente-geraldo-alckmin"
                "/agenda-do-vice-presidente-geraldo-alckmin/json/",
                PubliclyExposedPersons.VICE_PRESIDENT,
            ),
            (
                GOV_AGENDA_BASE_URL
                + "/acompanhe-o-planalto"
                "/agenda-da-primeira-dama"
                "/agenda-da-primeira-dama/json/",
                PubliclyExposedPersons.FIRST_LADY,
            ),
        ],
    )
    def test_get_authority_from_href(self, href, expected_role):
        assert get_authority_from_href(href) == expected_role
        
    
    def test_should_return_none_when_slug_found(self):
        assert get_authority_from_href("") == None
        
        
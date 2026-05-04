from app.models.agenda import PubliclyExposedPersons

ROLE_MAPPING = {
    "presidente-da-republica": PubliclyExposedPersons.PRESIDENT,
    "vice-presidente": PubliclyExposedPersons.VICE_PRESIDENT,
    "primeira-dama": PubliclyExposedPersons.FIRST_LADY,
}

def get_authority_from_href(href_string: str) -> PubliclyExposedPersons | None:
    href_lower = href_string.lower()
    
    for slug, role_enum in ROLE_MAPPING.items():
        if slug in href_lower:
            return role_enum
    
    return None
        
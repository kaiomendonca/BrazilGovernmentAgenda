from sqlalchemy.orm import Session

from app.models.agenda import Authorities
from app.utils.authority_utils import get_authority_from_href


class AuthorityRepository:
    def __init__(self, session: Session):
        self.session = session

    def exists(self, event_id: int, role) -> bool:
        return (
            self.session.query(Authorities)
            .filter_by(event_id=event_id, role=role)
            .first()
            is not None
        )

    def save_for_event(self, event, href_string: str):
        role_enum = get_authority_from_href(href_string)
        if role_enum is None:
            return None

        if not self.exists(event._id, role_enum):
            authority = Authorities(role=role_enum, event_id=event._id)
            self.session.add(authority)
            return authority

        return None

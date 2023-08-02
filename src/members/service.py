from datetime import datetime

from starlette import status

from src.database import Session, get_session
from src.models import tables
from uuid import UUID

from fastapi import (
    Depends, HTTPException,
)


class MembersService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def create(
            self,
            user_uuid: UUID,
            event_uuid: UUID,
    ) -> tables.Member:
        member = (
            self.session
                .query(tables.Member)
                .filter(
                    tables.Member.user_uuid == user_uuid,
                    tables.Member.event_uuid == event_uuid
                )
                .first()
        )
        if member:
            raise HTTPException(status.HTTP_409_CONFLICT)

        member = tables.Member(
            user_uuid=user_uuid,
            event_uuid=event_uuid,
            date=datetime.utcnow()
        )
        self.session.add(member)
        self.session.commit()
        return member


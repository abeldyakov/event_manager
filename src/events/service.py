from typing import (
    List,
    Optional,
)
from uuid import UUID

from fastapi import (
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from src.events.schemas import EventList, EventOut, Event, EventCreate, EventUpdate
from src.models import tables
from src.database import get_session


class EventsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_many(self, user_uuid: UUID) -> EventList:
        events = (
            self.session
            .query(tables.Event).join(tables.Member, isouter=True)
            .group_by(tables.Event)
            .order_by(
                tables.Event.date.desc(),
            )
            .all()
        )

        return events

    def get(
        self,
        user_id: int,
        event_uuid: UUID
    ) -> EventOut:

        event = (
            self.session
            .query(tables.Event).join(tables.Member, isouter=True).join(tables.User, isouter=True)
            .filter(
                tables.Event.uuid == event_uuid,
            )
            .group_by(tables.Event)
            .first()
        )
        if not event:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return event

    def create_many(
        self,
        user_id: int,
        events_data: List[EventCreate],
    ) -> List[Event]:
        events = [
            Event(
                **event_data.dict(),
                user_id=user_id,
            )
            for event_data in events_data
        ]
        self.session.add_all(events)
        self.session.commit()
        return events

    def create(
        self,
        user_uuid: UUID,
        event_data: EventCreate,
    ) -> tables.Event:
        event = tables.Event(
            **event_data.dict(),
        )
        self.session.add(event)
        self.session.commit()
        return event

    def update(
        self,
        user_uuid: UUID,
        event_uuid: UUID,
        event_data: EventUpdate,
    ) -> Event:
        event = self._get(user_uuid, event_uuid)
        for field, value in event_data:
            setattr(event, field, value)
        self.session.commit()
        return event

    def delete(
        self,
        user_uuid: UUID,
        event_uuid: UUID,
    ):
        event = self._get(user_uuid, event_uuid)
        self.session.delete(event)
        self.session.commit()

    def _get(self, user_uuid: UUID, event_uuid: UUID) -> Optional[tables.Event]:
        event = (
            self.session
            .query(tables.Event)
            .filter(
                tables.Event.uuid == event_uuid,
            )
            .first()
        )
        if not event:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return event

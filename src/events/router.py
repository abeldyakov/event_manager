from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from .service import EventsService
from .schemas import EventList, EventCreate, Event, EventOut, EventUpdate
from src.auth.service import get_current_user
from src.auth.schemas import User

router = APIRouter(
    prefix='/events',
    tags=['events'],
    responses={404: {"description": "Not found"}},
)


@router.get('/', response_model=List[EventList])
def get_events(
    user: User = Depends(get_current_user),
    events_service: EventsService = Depends(),
):
    return events_service.get_many(user.uuid)


@router.post(
    '/',
    response_model=Event,
    status_code=status.HTTP_201_CREATED,
)
def create_event(
    event_data: EventCreate,
    user: User = Depends(get_current_user),
    events_service: EventsService = Depends(),
):
    return events_service.create(
        user.uuid,
        event_data,
    )


@router.get(
    '/{event_uuid}',
    response_model=EventOut
)
def get_event(
    event_uuid: UUID,
    user: User = Depends(get_current_user),
    events_service: EventsService = Depends(),
):
    return events_service.get(
        user.uuid,
        event_uuid,
    )


@router.put(
    '/{event_uuid}',
    response_model=Event,
)
def update_event(
    event_uuid: UUID,
    event_data: EventUpdate,
    user: User = Depends(get_current_user),
    events_service: EventsService = Depends(),
):
    return events_service.update(
        user.uuid,
        event_uuid,
        event_data,
    )


@router.delete(
    '/{event_uuid}',
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_event(
    event_uuid: UUID,
    user: User = Depends(get_current_user),
    events_service: EventsService = Depends(),
):
    events_service.delete(
        user.uuid,
        event_uuid,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)

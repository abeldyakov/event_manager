from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.auth.service import get_current_user
from src.auth.schemas import User
from .service import MembersService
from .schemas import Member

router = APIRouter(
    prefix='/members',
    tags=['members'],
)


@router.post(
    '/',
    response_model=Member,
    status_code=status.HTTP_201_CREATED,
)
def participate(
    event_uuid: UUID,
    user: User = Depends(get_current_user),
    members_service: MembersService = Depends(),
):
    return members_service.create(
        user_uuid=user.uuid,
        event_uuid=event_uuid,
    )

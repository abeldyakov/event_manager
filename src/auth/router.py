from fastapi import (
    APIRouter,
    Depends,
    status,
)
from fastapi.security import OAuth2PasswordRequestForm


from .schemas import Token, User, UserCreate
from .service import AuthService, get_current_user

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)


@router.post(
    '/sign-up/',
    response_model=Token,
    status_code=status.HTTP_201_CREATED,
)
def sign_up(
    user_data: UserCreate,
    auth_service: AuthService = Depends(),
):
    return auth_service.register_new_user(user_data)


@router.post(
    '/sign-in/',
    response_model=Token,
)
def sign_in(
    auth_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(),
):
    return auth_service.authenticate_user(
        email=auth_data.username,
        password=auth_data.password,
    )


@router.get(
    '/profile/',
    response_model=User,
)
def get_user(user: User = Depends(get_current_user)):
    return user

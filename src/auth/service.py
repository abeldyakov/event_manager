import json
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.hash import bcrypt
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.auth.schemas import User, UserCreate, Token
from src.models import tables
from src.database import get_session
from settings import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/sign-in/')


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    return AuthService.verify_token(token)


class AuthService:
    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    def verify_token(cls, token: str) -> User:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algorithm],
            )
        except JWTError:
            raise exception from None

        user_data = payload.get('user')

        try:
            user = User.model_validate(json.loads(user_data))
        except ValidationError:
            raise exception from None

        return user

    @classmethod
    def create_token(cls, user: tables.User) -> Token:
        user_data = User.model_validate(user)
        now = datetime.utcnow()
        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + timedelta(seconds=settings.jwt_expires_s),
            'sub': str(user_data.uuid),
            'user': user_data.model_dump_json(),
        }
        token = jwt.encode(
            payload,
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm,
        )
        return Token(access_token=token)

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def register_new_user(
        self,
        user_data: UserCreate,
    ) -> Token:

        query = select(tables.User.uuid).where(tables.User.email == user_data.email)
        result = self.session.execute(query).one_or_none()
        if result:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='User already exist',
                headers={'WWW-Authenticate': 'Bearer'},
            )
        user = tables.User(
            email=user_data.email,
            username=user_data.username,
            password_hash=self.hash_password(user_data.password),
        )
        self.session.add(user)
        self.session.commit()
        return self.create_token(user)

    def authenticate_user(
        self,
        email: str,
        password: str,
    ) -> Token:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )

        user = (
            self.session
            .query(tables.User)
            .filter(tables.User.email == email)
            .first()
        )

        if not user:
            raise exception

        if not self.verify_password(password, user.password_hash):
            raise exception

        return self.create_token(user)

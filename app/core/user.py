from typing import Optional, Union

from fastapi import Depends, Request
from fastapi_users import (
    BaseUserManager, FastAPIUsers, IntegerIDMixin, InvalidPasswordException
)
from fastapi_users.authentication import (
    AuthenticationBackend, BearerTransport, JWTStrategy
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.models import User
from app.schemas.user import UserCreate

TOKEN_URL = 'auth/jwt/login'
TOKEN_LIFE_TIME = 3600
AUTH_BACKEND_NAME = 'jwt'
PASSWORD_LEN_VALUE = 3
PASSWORD_LEN_ERROR_MESSAGE = (f'Password should be at least'
                              f' {PASSWORD_LEN_VALUE} characters')
NO_EMAIL_IN_PASSWORD_MESSAGE = 'Пароль не должен содержать e-mail'


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


bearer_transport = BearerTransport(tokenUrl=TOKEN_URL)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.secret,
        lifetime_seconds=TOKEN_LIFE_TIME
    )


auth_backend = AuthenticationBackend(
    name=AUTH_BACKEND_NAME,
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    async def validate_password(
            self,
            password: str,
            user: Union[UserCreate, User]
    ) -> None:
        if len(password) < PASSWORD_LEN_VALUE:
            raise InvalidPasswordException(
                reason=PASSWORD_LEN_ERROR_MESSAGE
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason=NO_EMAIL_IN_PASSWORD_MESSAGE
            )

    async def on_after_register(
            self,
            user: User,
            request: Optional[Request] = None
    ) -> None:
        print(f'Пользователь {user.email} зарегистрирован.')


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)
current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)

from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from app.core.user import auth_backend, fastapi_users
from app.schemas.user import UserCreate, UserRead, UserUpdate

AUTH_NAME = 'auth'
USERS_NAME = 'users'
AUTH_TAGS = [AUTH_NAME]
USERS_TAGS = [USERS_NAME]
AUTH_PREFIX = '/' + AUTH_NAME
AUTH_JWT_PREFIX = AUTH_PREFIX + '/jwt'
USERS_PREFIX = '/' + USERS_NAME
USERS_DELETE_PATH = USERS_PREFIX + '/{id}'
DELETE_USERS_ERROR_MESSAGE = 'Удаление пользователей запрещено!'

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix=AUTH_JWT_PREFIX,
    tags=AUTH_TAGS,
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix=AUTH_PREFIX,
    tags=AUTH_TAGS,
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix=USERS_PREFIX,
    tags=USERS_TAGS
)


@router.delete(
    USERS_DELETE_PATH,
    tags=USERS_TAGS,
    deprecated=True
)
def delete_user(id: str):
    """Не используйте удаление, деактивируйте пользователей."""
    raise HTTPException(
        status_code=HTTPStatus.METHOD_NOT_ALLOWED,
        detail=DELETE_USERS_ERROR_MESSAGE
    )

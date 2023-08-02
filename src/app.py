import os
import sys

from fastapi import FastAPI

sys.path.append(os.path.join(sys.path[0], 'src'))

from auth.router import router as auth_router
from events.router import router as events_router
from members.router import router as members_router


tags_metadata = [
    {
        'name': 'auth',
        'description': 'Авторизация и регистрация',
    },
    {
        'name': 'events',
        'description': 'Создание, редактирование, удаление и просмотр мероприятий',
    },
    {
        'name': 'members',
        'description': 'Регистрация участия в событии',
    },
]

app = FastAPI(
    title='EventManager',
    description='Event management service',
    version='1.0.0',
    openapi_tags=tags_metadata,
)


app.include_router(auth_router)
app.include_router(events_router)
app.include_router(members_router)

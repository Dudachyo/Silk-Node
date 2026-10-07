from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
#
from app.api.v1.auth import router as auth_router
from app.api.v1.user import router as users_router
from app.api.v1.person import router as person_router
from app.api.v1.connection import router as connections_router




app = FastAPI(
    title="Silk Node"
)

origins = [
    "http://localhost:5173",  # адрес вашего React-приложения во время разработки
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # разрешить запросы с этих адресов
    allow_credentials=True,      # разрешить передачу кук и заголовков авторизации
    allow_methods=["*"],         # разрешить все методы (GET, POST и т.д.)
    allow_headers=["*"],         # разрешить все заголовки
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(person_router)
app.include_router(connections_router)

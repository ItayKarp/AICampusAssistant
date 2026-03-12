from fastapi import FastAPI
from api import users_router,announcements_router,load_router,faq_router,notification_router
from fastapi.middleware.cors import CORSMiddleware

from api.routes.management import management_router

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://www.itaykarpov.com",
    "https://itaykarpov.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)

app.include_router(announcements_router)
app.include_router(load_router)
app.include_router(faq_router)
app.include_router(notification_router)
app.include_router(management_router)

from fastapi import FastAPI
from api import users_router,announcements_router,load_router,faq_router,authentication_router
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
origins = [
    "https://www.itaykarpov.com",
    "https://itaykarpov.com"
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
app.include_router(authentication_router)
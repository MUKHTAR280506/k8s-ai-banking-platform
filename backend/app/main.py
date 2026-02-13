from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.init_db import init_db

from app.routes import chat, admin, beneficiary, validation

app = FastAPI()
@app.on_event("startup")
def on_startup():
    init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(admin.router)
app.include_router(beneficiary.router)
app.include_router(validation.router)
print(validation.router.routes)


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.v1.router import router as v1_router

from app.core.db import connect_and_init_db, close_db_connection

APP_TITLE = "Monty - Online Marketplace Platform"

# FastAPI Apps
app = FastAPI(title=APP_TITLE)
admin_app = FastAPI(title=f"{APP_TITLE} - Admin")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Connection
app.add_event_handler("startup", connect_and_init_db)
app.add_event_handler("shutdown", close_db_connection)

# User Routes
app.include_router(v1_router)

# Admin Routes
# admin_app.include_router(admin_api_router)
# app.mount("/admin", admin_app, name="admin")

# Static Files
app.mount("/uploads", StaticFiles(directory="static/uploads"), name="uploads")

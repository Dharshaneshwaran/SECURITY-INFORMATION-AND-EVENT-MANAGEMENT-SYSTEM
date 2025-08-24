from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from supabase import create_client, Client
from fastapi.middleware.cors import CORSMiddleware

# FastAPI app
app = FastAPI()

# ✅ CORS middleware must be before routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow POST, GET, OPTIONS
    allow_headers=["*"],  # Allow all headers
)

# Supabase setup
SUPABASE_URL = "https://mcevxrnarduqnkwdhchk.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1jZXZ4cm5hcmR1cW5rd2RoY2hrIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NjAyNjczNiwiZXhwIjoyMDcxNjAyNzM2fQ.eOwGlegEMJdiHOtH1ACVKGLbW5dZKGSdE3PV1QAUD7k"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# Pydantic models
class UserRegister(BaseModel):
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


@app.post("/register")
async def register(user: UserRegister):
    response = supabase.auth.admin.create_user(
        {
            "email": user.email,
            "password": user.password,
            "email_confirm": True,
        }
    )

    if response.user is None:
        raise HTTPException(status_code=400, detail=response)
    return {"user": response.user}


@app.post("/login")
async def login(user: UserLogin, request: Request):
    response = supabase.auth.sign_in_with_password(
        {"email": user.email, "password": user.password}
    )

    if response.user is None:
        raise HTTPException(status_code=400, detail=response)

    # ✅ Extract real client IP
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        ip_address = forwarded_for.split(",")[0].strip()
    else:
        ip_address = request.client.host

    # ✅ If still localhost, check "x-real-ip"
    if ip_address in ("127.0.0.1", "::1"):
        ip_address = request.headers.get("x-real-ip", ip_address)

    # ✅ Insert login log into Supabase
    supabase.table("logs").insert(
        {"user_id": response.user.id, "ip_address": ip_address}
    ).execute()

    return {"session": response.session, "user": response.user, "ip": ip_address}


@app.get("/")
async def root():
    return {"message": "FastAPI + Supabase backend running 🚀"}

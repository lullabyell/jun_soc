import jwt
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.auth import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_current_user,
    verify_password,
)
from app.models import LoginRequest, TokenResponse, RefreshRequest
from app.users import get_user


app = FastAPI(title="Junior SOC API")
security = HTTPBearer()

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/login", response_model=TokenResponse)
def login(credentials: LoginRequest):
    user = get_user(credentials.username)

    if not user or not verify_password(
        credentials.password,
        user["hashed_password"],
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    access_token = create_access_token(user["username"])
    refresh_token = create_refresh_token(user["username"])

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }

@app.get("/profile")
def profile(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    username = get_current_user(credentials.credentials)

    user = get_user(username)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return {
        "username": user["username"],
        "email": user["email"],
        "full_name": user["full_name"],
    }
    
@app.post("/refresh", response_model=TokenResponse)
def refresh_token(request: RefreshRequest):
    try:
        payload = decode_token(request.refresh_token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Refresh token has expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token",
        )

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=401,
            detail="Invalid token type",
        )

    username = payload.get("sub")

    if not username:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token",
        )

    user = get_user(username)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found",
        )

    new_access_token = create_access_token(username)

    return {
        "access_token": new_access_token,
        "refresh_token": request.refresh_token,
        "token_type": "bearer",
    }
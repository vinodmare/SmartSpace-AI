from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.auth import (
    ForgotPasswordRequest,
    LoginRequest,
    RefreshTokenRequest,
    RegisterRequest,
    ResetPasswordRequest,
    TokenResponse,
)
from app.schemas.common import MessageResponse
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/register", response_model=TokenResponse)
async def register(payload: RegisterRequest, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    return await AuthService(db).register(payload)


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    return await AuthService(db).login(payload)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(payload: RefreshTokenRequest, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    return await AuthService(db).refresh(payload.refresh_token)


@router.post("/forgot-password", response_model=MessageResponse)
async def forgot_password(payload: ForgotPasswordRequest, db: AsyncSession = Depends(get_db)) -> MessageResponse:
    await AuthService(db).forgot_password(payload.email)
    return MessageResponse(message="If the account exists, a reset email will be sent")


@router.post("/reset-password", response_model=MessageResponse)
async def reset_password(payload: ResetPasswordRequest, db: AsyncSession = Depends(get_db)) -> MessageResponse:
    await AuthService(db).reset_password(payload.token, payload.new_password)
    return MessageResponse(message="Password reset successfully")


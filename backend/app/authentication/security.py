from datetime import UTC, datetime, timedelta
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config.settings import settings
from app.exceptions import UnauthorizedError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, password_hash: str) -> bool:
    return pwd_context.verify(plain_password, password_hash)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def _create_token(subject: str, expires_delta: timedelta, secret: str, extra: dict[str, Any] | None = None) -> str:
    now = datetime.now(UTC)
    payload: dict[str, Any] = {"sub": subject, "iat": now, "exp": now + expires_delta}
    if extra:
        payload.update(extra)
    return jwt.encode(payload, secret, algorithm=settings.jwt_algorithm)


def create_access_token(subject: str, roles: list[str]) -> str:
    return _create_token(
        subject,
        timedelta(minutes=settings.access_token_expire_minutes),
        settings.jwt_secret_key,
        {"type": "access", "roles": roles},
    )


def create_refresh_token(subject: str) -> str:
    return _create_token(
        subject,
        timedelta(days=settings.refresh_token_expire_days),
        settings.jwt_refresh_secret_key,
        {"type": "refresh"},
    )


def decode_token(token: str, refresh: bool = False) -> dict[str, Any]:
    secret = settings.jwt_refresh_secret_key if refresh else settings.jwt_secret_key
    try:
        return jwt.decode(token, secret, algorithms=[settings.jwt_algorithm])
    except JWTError as exc:
        raise UnauthorizedError("Invalid or expired token") from exc


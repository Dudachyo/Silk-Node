from fastapi import HTTPException, status, Response, Request
from passlib.context import CryptContext
from datetime import datetime, timedelta , UTC
from jose import jwt  ,JWTError, ExpiredSignatureError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.repositories.user import UserRepository
from app.models.user import User


class Security:
    JWT_ACCESS_SECRET_KEY = settings.JWT_ACCESS_SECRET_KEY
    JWT_REFRESH_SECRET_KEY = settings.JWT_REFRESH_SECRET_KEY
    JWT_ALGORITHM = settings.JWT_ALGORITHM
    ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    REFRESH_TOKEN_EXPIRE_DAY = settings.REFRESH_TOKEN_EXPIRE_DAY

    pwd_context = CryptContext(
        schemes=["argon2"],
        deprecated="auto"
    )

    @classmethod
    def hash_password(cls, password: str) -> str:
        return cls.pwd_context.hash(password)

    @classmethod
    def verify_password(cls, password: str, hashed: str) -> bool:
        return cls.pwd_context.verify(password, hashed)

    @classmethod
    def create_access_token(cls, data: dict, expires_minutes: int | None = None) -> str:
        if expires_minutes is None:
            expires_minutes = cls.ACCESS_TOKEN_EXPIRE_MINUTES

        to_encode = data.copy()
        expire = datetime.now(UTC) + timedelta(minutes=expires_minutes)
        to_encode["exp"] = expire

        return jwt.encode(
            to_encode,
            cls.JWT_ACCESS_SECRET_KEY,
            algorithm=cls.JWT_ALGORITHM,
        )

    @classmethod
    def create_refresh_token(cls, data: dict, expires_day: int | None = None) -> str:
        if expires_day is None:
            expires_day = cls.REFRESH_TOKEN_EXPIRE_DAY

        to_encode = data.copy()
        expire = datetime.now(UTC) + timedelta(days=expires_day)
        to_encode["exp"] = expire

        return jwt.encode(
            to_encode,
            cls.JWT_REFRESH_SECRET_KEY,
            algorithm=cls.JWT_ALGORITHM,
        )

    @classmethod
    def decode_token(cls, token: str , token_name: str = 'access') -> dict:
        if token_name == 'access':
            secret_key = cls.JWT_ACCESS_SECRET_KEY
        elif token_name == 'refresh':
            secret_key = cls.JWT_REFRESH_SECRET_KEY
        else:
            raise HTTPException(status_code=401, detail="Token not found")

        try:
            payload = jwt.decode(
                token,
                secret_key,
                algorithms=[cls.JWT_ALGORITHM],
            )
            return payload
        except ExpiredSignatureError:
            raise HTTPException(401, "Token expired")
        except JWTError:
            raise HTTPException(401, "Invalid token")


    @classmethod
    async def refresh_access_token(cls, refresh_token: str, response: Response):
        try:
            payload = Security.decode_token(refresh_token, token_name='refresh')
            user_id = payload.get("sub")
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="refresh token is invalid"
            )
        access_token = Security.create_access_token({
            "sub": user_id,
        })
        response.set_cookie(
            key="access_token",
            value=access_token,
            samesite="lax",
            max_age=60 * Security.ACCESS_TOKEN_EXPIRE_MINUTES,
        )
        return access_token


    @classmethod
    async def get_user_object(cls,session: AsyncSession, response: Response , request:Request) -> User | HTTPException:
        repo = UserRepository(session)
        payload = await cls.get_payload_from_token(request=request, response=response)
        user_id = payload.get("sub")

        obj = await repo.get_one(id=int(user_id))
        if obj is None:
            raise HTTPException(status_code=404, detail="User not found")
        return obj

    @classmethod
    async def get_payload_from_token(cls, request: Request, response: Response) -> dict:
        access_token = request.cookies.get("access_token")
        refresh_token = request.cookies.get("refresh_token")

        if access_token is not None:
            try:
                return cls.decode_token(access_token)
            except HTTPException as exc:
                if exc.detail != "Token expired":
                    raise

        if refresh_token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
            )

        refresh_payload = cls.decode_token(refresh_token, token_name="refresh")
        user_id = refresh_payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        new_access_token = cls.create_access_token({"sub": user_id})

        response.set_cookie(
            key="access_token",
            value=new_access_token,
            httponly=True,
            samesite="lax",
            max_age=60 * cls.ACCESS_TOKEN_EXPIRE_MINUTES,
        )

        return cls.decode_token(new_access_token)


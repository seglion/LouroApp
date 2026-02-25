import os
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt
from src.domain.user_repository_interface import UserRepository
from src.infrastructure.security.hashing import verify_password

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-super-secret-key-for-development-only")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "1440")) # 24 horas

class LoginUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self, email: str, password: str) -> Optional[str]:
        user = self.repository.get_by_email(email)
        if not user:
            return None
            
        if not verify_password(password, user.hashed_password):
            return None
        
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {
            "sub": str(user.id),
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role.value,
            "exp": expire
        }
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        
        return encoded_jwt

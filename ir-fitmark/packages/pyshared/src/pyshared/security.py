"""Security utilities for IR FitMark."""

import secrets
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Union
from uuid import UUID

from jose import JWTError, jwt
from passlib.context import CryptContext

from .config import settings
from .models import TokenData, UserRole

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def generate_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None,
    token_type: str = "access"
) -> str:
    """Generate a JWT token."""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Default expiration times
        if token_type == "access":
            expire = datetime.utcnow() + timedelta(
                minutes=settings.auth.access_token_expire_minutes
            )
        else:  # refresh token
            expire = datetime.utcnow() + timedelta(
                days=settings.auth.refresh_token_expire_days
            )
    
    to_encode.update({"exp": expire, "type": token_type})
    
    return jwt.encode(
        to_encode,
        settings.auth.secret_key,
        algorithm=settings.auth.algorithm
    )


def verify_token(token: str, token_type: str = "access") -> Optional[TokenData]:
    """Verify and decode a JWT token."""
    try:
        payload = jwt.decode(
            token,
            settings.auth.secret_key,
            algorithms=[settings.auth.algorithm]
        )
        
        # Check token type
        if payload.get("type") != token_type:
            return None
        
        # Extract user data
        user_id: Optional[str] = payload.get("sub")
        email: Optional[str] = payload.get("email")
        role: Optional[str] = payload.get("role")
        
        if user_id is None:
            return None
        
        return TokenData(
            user_id=UUID(user_id) if user_id else None,
            email=email,
            role=UserRole(role) if role else None
        )
    
    except (JWTError, ValueError):
        return None


def create_access_token(
    user_id: Union[str, UUID],
    email: str,
    role: UserRole,
    expires_delta: Optional[timedelta] = None
) -> str:
    """Create an access token for a user."""
    data = {
        "sub": str(user_id),
        "email": email,
        "role": role.value,
    }
    return generate_token(data, expires_delta, "access")


def create_refresh_token(
    user_id: Union[str, UUID],
    expires_delta: Optional[timedelta] = None
) -> str:
    """Create a refresh token for a user."""
    data = {"sub": str(user_id)}
    return generate_token(data, expires_delta, "refresh")


def generate_qr_code() -> str:
    """Generate a secure QR code string."""
    return secrets.token_urlsafe(32)


def generate_secure_filename(original_filename: str) -> str:
    """Generate a secure filename with random prefix."""
    import os
    name, ext = os.path.splitext(original_filename)
    secure_name = secrets.token_urlsafe(16)
    return f"{secure_name}{ext}"


def validate_file_type(filename: str, allowed_types: list[str]) -> bool:
    """Validate file type based on extension."""
    import mimetypes
    
    mime_type, _ = mimetypes.guess_type(filename)
    return mime_type in allowed_types if mime_type else False


class RoleChecker:
    """Role-based access control checker."""
    
    def __init__(self, allowed_roles: list[UserRole]):
        self.allowed_roles = allowed_roles
    
    def __call__(self, user_role: UserRole) -> bool:
        """Check if user role is allowed."""
        return user_role in self.allowed_roles


# Common role checkers
require_admin = RoleChecker([UserRole.ADMIN])
require_instructor_or_admin = RoleChecker([UserRole.INSTRUCTOR, UserRole.ADMIN])
require_any_role = RoleChecker([UserRole.STUDENT, UserRole.INSTRUCTOR, UserRole.ADMIN])


def check_permission(user_role: UserRole, required_roles: list[UserRole]) -> bool:
    """Check if user has required permissions."""
    return user_role in required_roles


def is_admin(user_role: UserRole) -> bool:
    """Check if user is admin."""
    return user_role == UserRole.ADMIN


def is_instructor_or_admin(user_role: UserRole) -> bool:
    """Check if user is instructor or admin."""
    return user_role in [UserRole.INSTRUCTOR, UserRole.ADMIN]


# Rate limiting utilities
class RateLimiter:
    """Simple in-memory rate limiter."""
    
    def __init__(self):
        self._requests: Dict[str, list[datetime]] = {}
    
    def is_allowed(
        self,
        key: str,
        max_requests: int,
        window_seconds: int
    ) -> bool:
        """Check if request is allowed based on rate limit."""
        now = datetime.utcnow()
        cutoff = now - timedelta(seconds=window_seconds)
        
        # Initialize or clean old requests
        if key not in self._requests:
            self._requests[key] = []
        
        self._requests[key] = [
            req_time for req_time in self._requests[key]
            if req_time > cutoff
        ]
        
        # Check rate limit
        if len(self._requests[key]) >= max_requests:
            return False
        
        # Add current request
        self._requests[key].append(now)
        return True
    
    def reset(self, key: str) -> None:
        """Reset rate limit for a key."""
        if key in self._requests:
            del self._requests[key]


# Global rate limiter instance
rate_limiter = RateLimiter()
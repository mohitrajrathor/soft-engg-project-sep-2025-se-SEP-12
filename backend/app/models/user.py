from sqlalchemy import Column, Integer, String, DateTime, func
from app.core.db import Base
from passlib.context import CryptContext

# Use Argon2 via passlib to avoid bcrypt backend issues and the 72-byte limit.
# Argon2 is modern and secure; install with: pip install argon2-cffi
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(120), unique=True, index=True, nullable=False)
    # Keep column wide enough for hashed passwords
    password = Column(String(192), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def set_password(self, password: str):
        """
        Hash and set the user's password
        """
        self.password = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        """
        Verify the user's password
        """
        return pwd_context.verify(password, self.password)

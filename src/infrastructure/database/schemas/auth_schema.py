import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from . import Base


class AuthSchema(Base):
    __tablename__ = "auth"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String(30), unique=True, nullable=False, index=True)
    email = Column(String, unique=True)
    user_type = Column(String(30), nullable=False)
    password = Column(String)
    refresh_token = Column(String, nullable=True)
    last_login = Column(DateTime, nullable=True)
    foreign_id = Column(UUID, nullable=True)

    def __repr__(self) -> str:
        return (
            '{"id": "'
            + str(self.id)
            + '", "username": "'
            + str(self.username)
            + '", '
            + '"email": "'
            + str(self.email)
            + '", "user_type": "'
            + str(self.user_type)
            + '", "last_login: "'
            + str(self.last_login)
            + '", "foreign_id": "'
            + str(self.foreign_id)
            + '"}'
        )

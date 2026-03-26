from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from sqlalchemy.dialects.postgresql import JSONB


class Outbox(Base):
    __tablename__ = "outbox"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    payload: Mapped[dict] = mapped_column(JSONB, nullable=False)
    sent: Mapped[bool] = mapped_column(default=False)
    retry_count: Mapped[int] = mapped_column(default=0)

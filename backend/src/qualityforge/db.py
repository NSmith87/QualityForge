from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, String, Text, create_engine, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from qualityforge.settings import Settings


class Base(DeclarativeBase):
    pass


class AgentRunRecord(Base):
    __tablename__ = "agent_runs"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    requirement_id: Mapped[str] = mapped_column(String(128), index=True)
    jira_key: Mapped[str | None] = mapped_column(String(32), nullable=True)
    payload: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


def make_engine(settings: Settings):
    return create_engine(settings.database_url, future=True)


def make_session_factory(settings: Settings):
    engine = make_engine(settings)
    return sessionmaker(engine, expire_on_commit=False)


def init_db(settings: Settings) -> None:
    engine = make_engine(settings)
    Base.metadata.create_all(engine)

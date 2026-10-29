from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    recipes: Mapped[list["Recipe"]] = relationship(back_populates="user")
    sessions: Mapped[list["BrewSession"]] = relationship(back_populates="user")
    inventory: Mapped[list["Inventory"]] = relationship(back_populates="user")


class TeaType(Base):
    __tablename__ = "tea_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    category: Mapped[str] = mapped_column(String(80), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False, default="")
    default_temp: Mapped[int] = mapped_column(Integer, nullable=False)
    default_time: Mapped[int] = mapped_column(Integer, nullable=False)

    recipes: Mapped[list["Recipe"]] = relationship(back_populates="tea_type")
    inventory: Mapped[list["Inventory"]] = relationship(back_populates="tea_type")


class Recipe(Base):
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    tea_type_id: Mapped[int] = mapped_column(ForeignKey("tea_types.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    temperature: Mapped[int] = mapped_column(Integer, nullable=False)
    notes: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    is_private: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    user: Mapped["User"] = relationship(back_populates="recipes")
    tea_type: Mapped["TeaType"] = relationship(back_populates="recipes")
    infusions: Mapped[list["Infusion"]] = relationship(back_populates="recipe")
    sessions: Mapped[list["BrewSession"]] = relationship(back_populates="recipe")


class Infusion(Base):
    __tablename__ = "infusions"

    id: Mapped[int] = mapped_column(primary_key=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id"), nullable=False)
    number: Mapped[int] = mapped_column(Integer, nullable=False)
    brew_time_sec: Mapped[int] = mapped_column(Integer, nullable=False)

    recipe: Mapped["Recipe"] = relationship(back_populates="infusions")
    session_logs: Mapped[list["SessionLog"]] = relationship(back_populates="infusion")


class BrewSession(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id"), nullable=False)
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    total_rating: Mapped[int | None] = mapped_column(Integer, nullable=True)
    notes: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    user: Mapped["User"] = relationship(back_populates="sessions")
    recipe: Mapped["Recipe"] = relationship(back_populates="sessions")
    session_logs: Mapped[list["SessionLog"]] = relationship(back_populates="session")


class SessionLog(Base):
    __tablename__ = "session_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"), nullable=False)
    infusion_id: Mapped[int] = mapped_column(ForeignKey("infusions.id"), nullable=False)
    actual_time_sec: Mapped[int] = mapped_column(Integer, nullable=False)

    session: Mapped["BrewSession"] = relationship(back_populates="session_logs")
    infusion: Mapped["Infusion"] = relationship(back_populates="session_logs")


class Inventory(Base):
    __tablename__ = "inventory"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    tea_type_id: Mapped[int] = mapped_column(ForeignKey("tea_types.id"), nullable=False)
    weight_g: Mapped[float] = mapped_column(Float, nullable=False)

    user: Mapped["User"] = relationship(back_populates="inventory")
    tea_type: Mapped["TeaType"] = relationship(back_populates="inventory")

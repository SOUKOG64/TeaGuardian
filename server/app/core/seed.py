from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import TeaType


STARTER_TEA_TYPES = (
    {
        "name": "Да Хун Пао (武夷岩茶)",
        "category": "Улун",
        "description": "Утёсный улун из Уишань.",
        "default_temp": 93,
        "default_time": 6,
    },
    {
        "name": "Те Гуаньинь (铁观音)",
        "category": "Улун",
        "description": "Китайский улун Те Гуаньинь.",
        "default_temp": 80,
        "default_time": 6,
    },
    {
        "name": "Шен Пуэр (生普洱)",
        "category": "Пуэр",
        "description": "Шэн пуэр, выдержанный или молодой.",
        "default_temp": 80,
        "default_time": 9,
    },
    {
        "name": "Шу Пуэр (熟普洱)",
        "category": "Пуэр",
        "description": "Пуэр, прошедший ускоренную ферментацию.",
        "default_temp": 93,
        "default_time": 9,
    },
    {
        "name": "Жёлтый чай (君山银针)",
        "category": "Жёлтый чай",
        "description": "Жёлтый чай, включая сорт Цзюньшань Иньчжэнь.",
        "default_temp": 73,
        "default_time": 4,
    },
)


def seed_tea_types(db: Session) -> None:
    existing_names = set(db.scalars(select(TeaType.name)).all())
    try:
        for tea_type in STARTER_TEA_TYPES:
            if tea_type["name"] not in existing_names:
                db.add(TeaType(**tea_type))
        db.commit()
    except Exception:
        db.rollback()
        raise

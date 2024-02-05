from sqlalchemy import BigInteger, VARCHAR, DATETIME, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, declared_attr
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from config_data.config import SQL_ALCHEMY_URL


DATABASE_URL = SQL_ALCHEMY_URL

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine)


class AbstractBase(DeclarativeBase):
    """Абстрактный базовый класс для классов таблиц"""
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)

    @classmethod
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class Users(AbstractBase):
    """Класс для создания таблицы пользователей бота"""
    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    user_name: Mapped[str] = mapped_column(VARCHAR(30))
    full_name: Mapped[str] = mapped_column(VARCHAR(30))
    phone: Mapped[int] = mapped_column(Integer)


class SearchSetting(AbstractBase):
    """Класс для создания таблицы хранения поисковых настроек каждого пользователя"""
    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.telegram_id', ondelete='CASCADE'), unique=True)
    district: Mapped[str] = mapped_column(VARCHAR(30))
    rooms: Mapped[str] = mapped_column(VARCHAR(30))
    low_price: Mapped[int] = mapped_column(Integer)
    high_price: Mapped[int] = mapped_column(Integer)


class ViewedAdv(AbstractBase):
    """Класс для создания таблицы просмотренных объявлений"""
    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.telegram_id', ondelete='CASCADE'))
    adv_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('advertisements.advertisements_id',
                                                               ondelete='CASCADE', comment='id объявления'))
    date_adv: Mapped[str] = mapped_column(DATETIME)
    UniqueConstraint(telegram_id, adv_id, name='viewed_tg_adv_key')


class Advertisements(AbstractBase):
    """Класс для создания таблицы с объявлениями об аренде квартир"""
    id: Mapped[int] = mapped_column(primary_key=True)
    advertisements_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    date_adv: Mapped[str] = mapped_column(DATETIME)
    district: Mapped[str] = mapped_column(VARCHAR(30))
    rooms: Mapped[str] = mapped_column(VARCHAR(30))
    floor: Mapped[str] = mapped_column(VARCHAR(30))
    price: Mapped[int] = mapped_column(Integer)
    square: Mapped[str] = mapped_column(VARCHAR(30))
    repair: Mapped[str] = mapped_column(VARCHAR(240))
    furniture: Mapped[str] = mapped_column(VARCHAR(240))
    description: Mapped[str] = mapped_column(VARCHAR(240))
    address: Mapped[str] = mapped_column(VARCHAR(240))
    phone: Mapped[str] = mapped_column(VARCHAR(30))
    images: Mapped[str] = mapped_column(VARCHAR(2000))
    url: Mapped[str] = mapped_column(VARCHAR(50))


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(AbstractBase.metadata.create_all)


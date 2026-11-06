"""SQLite storage and automatic catalog seeding."""
from pathlib import Path
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy.types import JSON

BASE_DIR = Path(__file__).resolve().parent
DATABASE_URL = f"sqlite:///{(BASE_DIR / 'devtool_finder.db').as_posix()}"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

class Tool(Base):
    __tablename__ = "tools"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[str]
    category: Mapped[str] = mapped_column(index=True)
    languages: Mapped[list] = mapped_column(JSON, default=list)
    domains: Mapped[list] = mapped_column(JSON, default=list)
    experience_level: Mapped[list] = mapped_column(JSON, default=list)
    features: Mapped[list] = mapped_column(JSON, default=list)
    project_types: Mapped[list] = mapped_column(JSON, default=list)
    databases: Mapped[list] = mapped_column(JSON, default=list)
    pricing_type: Mapped[str]
    license_type: Mapped[str]
    website: Mapped[str]
    strengths: Mapped[list] = mapped_column(JSON, default=list)
    limitations: Mapped[list] = mapped_column(JSON, default=list)
    popularity: Mapped[str] = mapped_column(default="Popular")

def init_db():
    Base.metadata.create_all(bind=engine)
    from .seed import seed_tools
    with SessionLocal() as db:
        existing = set(db.scalars(select(Tool.name)).all())
        missing = [row for row in seed_tools() if row["name"] not in existing]
        if missing:
            db.add_all(Tool(**row) for row in missing)
            db.commit()

def get_db():
    with SessionLocal() as db:
        yield db

from app.db.session import engine
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'bb' AND table_name != 'alembic_version';"))
    tables = [row[0] for row in result]
    print("Tables in 'bb' schema (excluding alembic_version):", tables)
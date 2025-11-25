"""Script to reset database with new schema including user_id."""

from app.database import engine, Base
from app.models import Goal, Task

print("Dropping all tables...")
Base.metadata.drop_all(bind=engine)

print("Creating all tables with new schema...")
Base.metadata.create_all(bind=engine)

print("Database reset complete! All tables now include user_id field.")

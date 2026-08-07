from collections.abc import Generator
from sqlalchemy.orm import Session
from app.db.database import session_local

def get_db() -> Generator[Session, None, None]:  
    db = session_local()
    try:
        yield db
    finally:
        db.close()
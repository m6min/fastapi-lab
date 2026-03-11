from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from database import Base


class Link(Base):
    ''' Database / Sqlalchemy class '''
    __tablename__ = 'shortened_links'
    id: int = Column(Integer, primary_key=True)
    long_url: str = Column(String, index=True)
    slug: str = Column(String, unique=True)
    # Get date
    created_at = Column(DateTime, default=datetime.now)

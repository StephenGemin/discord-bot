import logging
from importlib import resources

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from . import constants

logger = logging.getLogger(__name__)
Base = declarative_base()


class SadTrigger(Base):
    __tablename__ = "sad_message_trigger_words"
    id = Column(Integer, primary_key=True)
    word = Column(String)


class SadResponse(Base):
    __tablename__ = "sad_message_response"
    id = Column(Integer, primary_key=True)
    response = Column(String)


def load_db():
    logging.info(f"{constants.APP_NAME}")
    with resources.path(f"{constants.APP_NAME}.data", constants.DB_NAME) as db_file:
        engine = create_engine(f"sqlite:///{db_file}")
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    return session

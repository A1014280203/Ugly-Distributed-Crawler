from config import d_server
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class Post(Base):
    __tablename__ = 'posts'
    num = Column(Integer, primary_key=True, autoincrement=True)
    post = Column(Text)


def make_db_session():
    param = 'mysql+pymysql://{user}:{pw}@{addr}/kybsrc?charset=utf8'.format(user=d_server['user'],
                                                                            pw=d_server['passwd'],
                                                                            addr=d_server['addr'])
    engine = create_engine(param)
    db_session = sessionmaker(bind=engine)
    session = db_session()
    return session


def db_add(text):
    db = make_db_session()
    db.add(Post(post=text))
    db.commit()
    db.close()

if __name__ == '__main__':
    t = 'content of post'
    db_add(t)

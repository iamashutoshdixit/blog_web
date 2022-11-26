from sqlalchemy import Column, VARCHAR, Integer,DateTime, ForeignKey,create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker




eng = create_engine("sqlite:///blogmanager.db", echo=True)

Base= declarative_base()

class User(Base):
    __tablename__= "user"
    user_id = Column(Integer, primary_key = True, index = True)
    user_name = Column(VARCHAR)
    email = Column(VARCHAR)
    password = Column(VARCHAR)
    created_at = Column(DateTime)

    task_user = relationship("Task", back_populates = "user_task")


class Blog(Base):
    __tablename__="blog"
    blog_id=Column(Integer,primary_key = True, index  = True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    blog = Column(VARCHAR, Integer)
    created_at = Column(DateTime)
    deleted_at = Column(DateTime)
    updated_at = Column(DateTime)
    vote_count = Column(Integer)


class Vote(Base):
    __tablename__ = "vote"
    vote_id = Column(Integer, primary_key = True, index = True)
    blog_id = Column(Integer, ForeignKey("blog.blog_id")) 
    user_id = Column(Integer, ForeignKey("user.user_id"))


session = sessionmaker(bind=eng)

Base.metadata.create_all(eng)    



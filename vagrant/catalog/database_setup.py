# CONFIG1
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


# let sqlalchemy know that our classes correspond to db tables
Base = declarative_base()

# CLASSES
class User(Base):
    # table representation
    __tablename__ = 'user'
    # columns
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    email = Column(String(250))
    picture = Column(String(250))

    # for JSON
    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
            'email': self.email,
            'picture': self.picture,
        }

class Category(Base):
    # table representation
    __tablename__ = 'category'
    # columns
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)


    # for JSON
    @property
    def serialize(self):
        #return dict(name=self.name, id=self.id, items=[])
        return {
            'name': self.name,
            'id': self.id,
            'items': [],
        }

class Item(Base):
    # table representation
    __tablename__ = 'item'
    # columns
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    created_at = Column(DateTime)

    # for JSON
    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'created_at': self.created_at,
        }




# CONFIG2
# create database
engine = create_engine('sqlite:///itemcatalog.db')
# add classes/tables to database
Base.metadata.create_all(engine)

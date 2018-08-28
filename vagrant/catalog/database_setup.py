# CONFIG1
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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

    # for JSON
    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
            'email': self.email,
        }


class Category(Base):
    # table representation
    __tablename__ = 'category'
    # columns
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)

    # for JSON
    @property
    def serialize(self):
        # return dict(name=self.name, id=self.id, items=[])
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
if __name__ == '__main__':
    # create database
    engine = create_engine('sqlite:///itemcatalog.db')
    # add classes/tables to database
    Base.metadata.create_all(engine)

    # CREATE CATEGORIES
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    newCategory = Category(name="Baseball")
    session.add(newCategory)
    session.commit()

    newCategory = Category(name="Football")
    session.add(newCategory)
    session.commit()

    newCategory = Category(name="Badminton")
    session.add(newCategory)
    session.commit()

    newCategory = Category(name="Basketball")
    session.add(newCategory)
    session.commit()

    newCategory = Category(name="Tennis")
    session.add(newCategory)
    session.commit()

    newCategory = Category(name="Running")
    session.add(newCategory)
    session.commit()

    newCategory = Category(name="Swimming")
    session.add(newCategory)
    session.commit()

    newCategory = Category(name="Cycling")
    session.add(newCategory)
    session.commit()

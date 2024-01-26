#!/usr/bin/python3
from re import U
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.city import City
from models.state import State
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from os import getenv


class DBStorage:
    """ this for database storage"""
    __engine = None
    __session = None

    def __init__(self):
        """ initialized insttance attribute"""
        user = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db_name = getenv("HBNB_MYSQL_DB")
        data_URL = f"mysql+mysqldb://{user}:{password}@{host}:3306/{db_name}"

        self.__engine = create_engine(data_URL, pool_pre_ping=True)
        is_equal = (getenv("HBNB_ENV") == "test")
        if is_equal:
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Quary all classes or """
        classes = [User, State, City, Amenity, Place, Review]
        ALL = {}
        if cls:
            if cls in classes:
                for obj in self.__session.query(cls).all():
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    ALL[key] = obj
        else:
            for CLS in classes:
                for obj in self.__session.query(CLS).all():
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    ALL[key] = obj
        return ALL

    def new(self, obj):
        """add object"""
        if obj:
            self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj"""
        if obj:
            self.__session.delele(obj)

    def reload(self):
        """create all tables in the database"""
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(
            bind=self.__engine, expire_on_commit=False))
        self.__session = Session()
    
    def close(self):
        """close session"""
        self.__session.remove()

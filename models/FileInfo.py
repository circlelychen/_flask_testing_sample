import datetime

from sqlalchemy import String 
from sqlalchemy import Integer 
from sqlalchemy import DateTime 
from models import db

class FileInfo(db.Model):
    __tablename__ = 'FileInfo'

    id = db.Column('id', Integer, primary_key=True)
    file_name = db.Column('file_name', String(64), index=True, unique=True)
    storage_key = db.Column('storage_key', String(64), unique=True)
    create_datetime = db.Column('create_datetime', DateTime, default=datetime.datetime.utcnow, nullable=False)

    def __repr__(self):
        return u"FileInfo<(id:{0}, file_name: {1}, storage_key: {2})>".format(self.id, self.file_name, self.storage_key)

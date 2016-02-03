import datetime
import uuid
import pytz

import factory
import factory.fuzzy
from factory.alchemy import SQLAlchemyModelFactory

def init_db(app):
    from models import db
    db.init_app(app)
    db.create_all()
    return db

from models import FileInfo
class FileInfoFactory(SQLAlchemyModelFactory):
    class Meta:
        model = FileInfo.FileInfo
        sqlalchemy_session = FileInfo.db.session   # the SQLAlchemy session object

    id = factory.Sequence(lambda n: n)
    file_name = factory.LazyAttribute(lambda obj: "file_name-{0}.txt".format(obj.id))
    storage_key = factory.LazyAttribute(lambda obj: "storage_key-{0}".format(uuid.uuid4().hex))
    create_datetime = factory.fuzzy.FuzzyDateTime(datetime.datetime.utcnow().replace(tzinfo=pytz.utc) - datetime.timedelta(days=5))

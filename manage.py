from flask.ext.script import Manager

from application import create_app
from application import init_app

app = create_app("app", "config.DevelopmentConfig")
app = init_app(app)
manager = Manager(app)

@manager.command
def init_db():
    from models import db
    db.init_app(app)
    db.create_all()

if __name__ == "__main__":
    manager.run()

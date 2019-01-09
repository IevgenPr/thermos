#! /usr/bin/env python

from thermos import app, db
from thermos.models import User, Bookmark, Tag
from flask_script import Manager, prompt_bool
from flask_migrate import Migrate, MigrateCommand

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def insert_data():
    user = User(username='ipr', email="ipr@example.com", password="test")
    db.session.add(user)

    def add_bookmark(url, description, tags):
        db.session.add(Bookmark(url=url, description=description,
                                user=user, tags=tags))

    for name in ["python", "flask", "webdev", "programming", "training", "orm",
                 "databases", "news"]:
        db.session.add(Tag(name=name))
    db.session.commit()

    add_bookmark("http://www.pluralsight.com", "Pluralsite. Hard","training")
    add_bookmark("http://www.python.org", "Python - my favorite...", "python")
    add_bookmark("http://flask.pocoo.org", "Flask: web development", "flask")
    add_bookmark("http://www.reddit.com", "Reddit: frontpage", "")
    add_bookmark("http://www.sqlalchemy.org", "nice orm framework", "python,orm,databases")
    add_bookmark("http://werkzeug.pocoo.org/docs/", "Werkzeug", "")
    add_bookmark("http://jinja.pocoo.org", "Jinja templates", "programming,flask,webdev")
    add_bookmark("http://pythonhosted.org/Flask-SQLAlchemy", "", "orm")
    add_bookmark("http://www.initializr.com", " get up and running with HTML5", "webdev")
    add_bookmark("http://emacswiki.org", "all about emacs", "")
    add_bookmark("http://vimwiki.org", "", "vim")
    add_bookmark("http://orgmode.org", "productivity in text mode", "gtd")
    add_bookmark("http://ipython.org", "iipython. interactive compution", "python")
    add_bookmark("http://djangoproject.org", "django - another web framework", "")
    add_bookmark("http://", "", "")
    add_bookmark("http://stackoverflow.com", "", "")

    another_user = User(username="pri", email="pri@examle.com", password="test")
    db.session.add(another_user)
    db.session.commit()

@manager.command
def initdb():
    db.create_all()
    db.session.add(User(username="ipr", email="ipr@example.com", password="test"))
    db.session.add(User(username="rpi", email="rpi@example.com", password="test"))
    db.session.commit()
    print("Initialized database")


@manager.command
def dropdb():
    if prompt_bool("Are you sure you want to drop database? "):
        db.drop_all()
        print("Dropped database")


if __name__ == "__main__":
    manager.run()

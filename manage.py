import os
from flask.ext.script import Manager, Server, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from webapp import app
from webapp1.models import db, User


# default to dev config
env = os.environ.get('WEBAPP_ENV', 'dev')

migrate = Migrate(app, db)
manager = Manager(self.app)
manager.add_command("server", Server())
manager.add_command('db', MigrateCommand)
manager.add_command("shell", Shell(make_context=_make_context))

#Test SFTP
@manager.command
def make_shell_context():
    return dict(
        app=app,
        db=db,
        User=User
    )



if __name__ == "__main__":
    manager.run()
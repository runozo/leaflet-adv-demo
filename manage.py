#! python3
# -*- coding: utf-8 -*-
from flask.ext.script import Manager

from demo import app

manager = Manager(app)


@manager.command
@manager.option('-c', '--config', required=False, help='config file')
def runserver(config=None):
    app.run()


if __name__ == "__main__":
    manager.run()

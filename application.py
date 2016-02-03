import os
import sys
import logging

from flask import Flask

from logger import init_logger

def create_app(app_name, config_setting):
    if not os.getcwd in sys.path:
        sys.path.append(os.getcwd())

    app = Flask(app_name)
    init_logger(app_name, logging.DEBUG, logging.StreamHandler())

    # 1. load config setting, DEBUG flag is set here
    try:
        app.config.from_object(config_setting)
    except ImportError:
        pass
    app_context = app.app_context()
    app_context.push()
    return app


def init_app(app):
    def register_blueprint(app, bp_instance, web_server_prefix='', url_prefix=''):
        if not app.config['DEBUG']:
            # This is for runapp
            app.register_blueprint(bp_instance, url_prefix=web_server_prefix + url_prefix)
        elif not app.config['TESTING']:
            # This is for livereload
            app.register_blueprint(bp_instance, url_prefix= web_server_prefix + url_prefix)
        else:
            # This is testing
            app.register_blueprint(bp_instance, url_prefix=url_prefix)
    # bind restful api
    from api import restful
    register_blueprint(app, restful, web_server_prefix="", url_prefix='')
    return app


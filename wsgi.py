
from application import create_app
from application import init_app

if __name__ == "__main__":
    app = create_app("app", "config.DevelopmentConfig")
    app = init_app(app)
    app.run(host='0.0.0.0', debug=True)

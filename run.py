import os

from app import create_app

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

if __name__ == '__main__':
    app.run()
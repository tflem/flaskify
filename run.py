import os
import psycopg2
import urlparse

from app import create_app

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

if __name__ == '__main__':
    app.run()
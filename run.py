import os

is_prod = os.environ.get('IS_HEROKU', None)

if is_prod:
	urlparse.uses_netloc.append("postgres")
	url = urlparse.urlparse(os.environ["DATABASE_URL"])

	conn = psycopg2.connect(
	    database=url.path[1:],
	    user=url.username,
	    password=url.password,
	    host=url.hostname,
	    port=url.port
)

from app import create_app

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)



if __name__ == '__main__':
    app.run()
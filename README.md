# CiHui - Chinese word lists

## Run web server

Setup virtual env:

    pip install virtualenv  # if not already installed
    source bin/activate

Install dependencies:

    pip install -r requirements.txt

Run using foreman:

    foreman run web

Or:

    foreman run debug

Open a browser to http://localhost:5000/

## Run tests

    py.test --cov cihui --cov-report term-missing -f test/

or

    foreman run cov

## Configuration

Cihui uses environment variables for most configuration.

* API_USER -- username for API access (currently limited)
* API_PASS -- password for API access (currently limited)
* COOKIE_SECRET -- cookie secret for secure cookies.
* DATABASE_URL -- connection string for Postgres
  (eg. postgresql://localhost:5432/cihui).
* PORT -- port to run the web server on (eg. 5000).
* SKRITTER_OAUTH_CLIENT_ID -- client id for Skritter OAuth (see [Skritter API](http://www.skritter.com/api/v0/docs/authentication))
* SKRITTER_OAUTH_CLIENT_SECRET -- client secret for Skritter OAuth
* SKRITTER_REDIRECT_URI -- redirect uri for receiving Skritter OAuth
  token. (eg. http://example.com/skritter/auth)


## Add a database migration

    alembic revision -m "Add a column"
    ...
    alembic upgrade head

See the
[alembic docs](https://alembic.readthedocs.org/en/latest/tutorial.html#running-our-second-migration)
for more details on migrations, and the
[SQLAlchemy](http://docs.sqlalchemy.org/en/rel_0_8/core/schema.html) docs for
details on schema.

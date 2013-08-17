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

    source bin/activate
    py.test --cov cihui -f test/

## Add a database migration

    alembic revision -m "Add a column"
    ...
    alembic upgrade head

See the
[alembic docs](https://alembic.readthedocs.org/en/latest/tutorial.html#running-our-second-migration)
for more details on migrations, and the
[SQLAlchemy](http://docs.sqlalchemy.org/en/rel_0_8/core/schema.html) docs for
details on schema.

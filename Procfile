web:      python app/app.py
debug:    python app/app.py --debug

downgrade: alembic downgrade -1
migrate: alembic upgrade head
stats: radon cc --min B -s cihui test

pep8: find app cihui test -name '*.py' | xargs pep8

test: py.test test
cov: py.test --cov cihui --cov-report term-missing

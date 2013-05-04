web:      gunicorn -k tornado -b 0.0.0.0:$PORT -w 4 main
tornado:  python main.py
debug:    python main.py --debug

downgrade: alembic downgrade -1
migrate: alembic upgrade head
stats: radon cc --min B -s cihui test

pep8: find main.py cihui test -name '*.py' | xargs pep8

test: py.test test
int: py.test scripts/test_*
cov: py.test --cov cihui --cov-report term-missing test

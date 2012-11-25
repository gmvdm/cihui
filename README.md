# CiHui - Chinese word lists

## Run web server

Setup virtual env:

    pip install virtualenv  # if not already installed
    source bin/activate

Install dependencies:

    pip install -r requirements.txt

Run using foreman:

    foreman run web

Run directly:

    python app/app.py 0.0.0.0:5000

Open a browser to http://localhost:5000/

## Run tests

    source bin/activate
    py.test -f test/




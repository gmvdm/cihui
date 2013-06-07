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

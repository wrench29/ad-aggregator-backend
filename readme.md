# Ad Aggregator backend

Simple application written in Python, using FastAPI and SQLAlchemy.

### How to configure

It is recommended to use Python 3.10+

#### Create virtual environment

`$ python -m venv .venv`

#### Enable venv
For Linux/MacOS:

`$ .venv/bin/activate`

For Windows:

`$ .venv/Scripts/Activate.ps1`

May require to enable remote script execution.

#### Install dependencies

`(.venv) $ pip install -r requirements.txt`

#### Create and migrate database

`(.venv) $ alembic upgrade head`

#### Run application (Development mode)

`(.venv) $ fastapi dev app/main.py`


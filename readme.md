# Ad Aggregator backend

Simple application written in Python, using FastAPI and SQLAlchemy.

### How to configure

It is recommended to use Python 3.10+


#### Set up secrets

Create `.env` file and put next values in it:

`AUTORIA_TOKEN="<YOUR_AUTORIA_API_TOKEN>"`

`SECRET_KEY="<YOUR_JWT_SECRET_64_CHARACTERS_LONG>"`

Example value for JWT secret:

`14d25e094faa6123456c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d30k`

#### Create virtual environment

`$ python -m venv .venv`

#### Enable venv
For Linux/MacOS:

`$ . .venv/bin/activate`

For Windows:

`$ .venv/Scripts/Activate.ps1`

May require to enable remote script execution.

#### Install dependencies

`(.venv) $ pip install -r requirements.txt`

#### Create and migrate database

`(.venv) $ alembic upgrade head`

#### Run application (Development mode)

`(.venv) $ fastapi dev app/main.py`

#### View docs

http://localhost:8000/docs

http://localhost:8000/redoc

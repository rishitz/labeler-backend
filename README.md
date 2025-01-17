# Labeler Backend

This is the backend for the Labeler. It is built using Django and PostgreSQL, and can be run either natively on your local machine or using Docker.

## Prerequisites

Before starting, ensure you have the following installed:

- [Python 3.10+](https://www.python.org/)
- [PostgreSQL](https://www.postgresql.org/download/)
- [Docker](https://www.docker.com/get-started) (optional if using Docker)
- [Docker Compose](https://docs.docker.com/compose/install/) (optional if using Docker)

Additionally, set up an `.env` file in the root of the project with the following environment variables. Replace the values with your own credentials:

```env
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=<your-database-name>
DB_USER=<your-database-user>
DB_PASS=<your-database-password>
DB_HOST=<your-database-host>
DB_PORT=<your-database-port>
```


## Setup the project natively

**1. Clone the repository**
```
git clone <your-repository-url>
cd <your-project-directory>
```
**2. Create virtual environment**
```
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
**3. Install dependencies**
```
pip install -r requirements.txt
```
**4. Setup the database:** - Ensure PostgreSQL is running and create a database matching the credentials in your .env file.

## Setup database locally for testing

**1. Install postgres locally**
```
apt install postgresql postgresql-contrib
sudo service postgresql start
```

**2. Update password**
```
sudo -i -u postgres
psql
ALTER USER postgres PASSWORD 'whatever_password_youwant';
```

**3. Migrate structure**

Make sure you are in (venv)
```
python manage.py migrate
```

**4. Create Django User**

Make sure you are in (venv)
```
python manage.py createsuperuser
```
Input email and password


## Setup the project with Docker

**1. Clone the repository**
```
git clone <your-repository-url>
cd <your-project-directory>
```
**2. Bound postgres container to local directory**
```
mkdir postgres_data
chmod 777 -R postgres_data
```
**3. Build Docker image**
```
docker-compose build
```
**4. Run Docker container**
```
docker-compose up
```

## Run migrations
```
python manage.py migrate
```

## Run the development server:
```
python manage.py runserver
```

## Pre-commit Hook Installation
This project uses pre-commit to enforce code quality checks. Install the hooks with the following command:
```
pre-commit install
```
## Development Guidelines

### Branch Naming Convention

Branches should be named as follows:
```
{initials}/{ticket-number}/{task-description}
```

### Conventional Commits
All commits must follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) standard.


### Testing Convention
When writing tests, follow this naming convention for test methods:
```
def test_<methodUnderTest>_<expectedResult>_when<underCertainConditions>
```


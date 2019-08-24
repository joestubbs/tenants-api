# tapiscore (tapycore?)

Core Python library for building Tapis v3 APIs. This library provides Python modules, Dockerfiles and build scripts to
standardize and streamline the development process.

## Getting Started

1. Create a git repository with the following:

```
  + service: directory for API source code.
  + db-data: directory to hold data volume for local db.
  + migrations: directory for migration scripts.
  - config.json: API config values for local development
  - configschema.json: jsonschema definition of the API config.
  - Dockerfile: Build recipe for the API service Docker image.
  - Dockerfile-migrations: Build recipe for the API service migrations Docker image.
  - requirements.txt: Packages required for the API service or migrations scripts.
  - docker-compose.yml:
  - CHANGELOG.md: Tracks releases for the service.
  - README.md: High level description of the service.
  - service.log: Mount into the API container to capture service logs during local development.
```

2. Edit the Dockerfile:
  FROM: tapis/pybase
  ENV TAPIS_API <api_name>
  COPY requirements.txt /home/tapis/requirements.txt
  RUN pip install -r /home/tapis/requirements.txt
  COPY service /home/tapis/service

3. Create migration skeleton.
  Migrations are based on the `alembic` package and must be initialized.

```
  $ docker run -it --entrypoint=bash -v $(pwd):/home/tapis/mig tapis/tenants-api
  # inside the container:
  $ cd mig; alembic init migrations
  $ exit
```

4. Modify the migrations skeleton:
  - Move the `alembic.ini` file into the migrations folder: `mv alembic.ini migrations/`
  - Update the `sqlalchemy.url` within the `alembic.ini` file to use the


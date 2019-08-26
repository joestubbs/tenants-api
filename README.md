# Tapis Tenants API

REST API for managing tenants associated with a Tapis instance.

## Usage
This repository includes build files and other assets needed to start the service locally. Clone this
repository and follow the steps in the subsequent section.

### Start the API Locally
We are automating the management of the lifecycle workflow with `make`. You will need to install `make` it in order
to use the steps bellow.

The make system is generic and used by multiple Tapis services. Before following any of the sections below,
be sure to

```
$ export API_NAME=tenants
```

The `API_NAME` variable is used to let the `make` system know which Tapis service to work with.


#### First Time Setup
Starting the API the first time requires some initial setup. Do the following steps once per machine:

1. `make init_dbs` - creates a new docker volume, `tenant-api_pgdata`, creates a new Postrgres
Docker container with the volume created, and creates the initial (empty) database and database user.
2. `make migrate.upgrade` - runs the migrations contained within the `migrations/versions` directory.
3. `docker-compose up -d tenants` - starts the Tenats API.

#### Updating the API After the First Setup
Once the First Time Setup has been done a machine, updates can be fetched applied as follows:

1. `git pull` - Download the latest updates locally.
2. `make build.api` - Build a new version of the API container image.
3. `make migrate.upgade` - Run any new migrations (this step is only needed if new files appear in the `versions`
directory).migrations
4. `docker-compose up -d tenants` - start a new version of the Tenats API.

### Example Requests
Use any HTTP client to interact with the running API. The following examples use `curl`.

#### List all LDAP objects

```
$ curl localhost:5000/ldaps | jq
{
  "message": "LDAPs retrieved successfully.",
  "result": [
    {
      "account_type": "LDAPAccountTypes.service",
      "bind_credential": "tapis://ldapbind/foo",
      "bind_dn": "admin",
      "id": 4,
      "name": "foo_ldap",
      "url": "ldaps://ldap.tacc.utexas.edu"
    }
  ],
  "status": "success",
  "version": "dev"
}
```

#### Create an LDAP object

```
$ curl localhost:5000/ldaps -H "content-type: application/json" -d '{"url":"ldaps://ldap.tacc.utexas.edu", "user_dn": "ou=users,dc=tapisldap", "bind_dn": "admin", "bind_credential": "tapis://ldapbind/foo", "account_type": "user", "name": "ldap2"}'
{
	"message": "LDAP object created successfully.",
	"result": {
		"account_type": "LDAPAccountTypes.user",
		"bind_credential": "tapis://ldapbind/foo",
		"bind_dn": "admin",
		"id": 5,
		"name": "ldap2",
		"url": "ldaps://ldap.tacc.utexas.edu"
	}
}
```

A complete OpenAPI v3 spec file is included in the `service/resources` directory within this repository.
# python-web-app

A sample python web app built using Flask. It is based off the python-web-app from the [vmware-tanzu/application-accelerator-samples](https://github.com/vmware-tanzu/application-accelerator-samples), but has been modified to make use of a postgresql database by following the tutorial [How to Use Flask-SQLAlchemy to Interact with Databases in a Flask Application](https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application). It also uses the [pyservicebinding](https://github.com/baijum/pyservicebinding) library to pragmatically handle obtaining credentials for the database. The application is intended to run on Tanzu Application Platform.

## Deploying to TAP (using out of the box Bitnami PostgreSQL)

_note:_ Assumes TAP version >= 1.5

```
$ tanzu service class-claim create bitnami-psql-1 --class postgresql-unmanaged
$ tanzu service class-claim get bitnami-psql-1 # copy the Claim Reference from the output
$ tanzu apps workload create python-web-app-bitnami-psql \
  --local-path . \
  --source-image <your image repo> \
  -l app.kubernetes.io/part-of=python-web-app-bitnami-psql \
  --service-ref db=<the Claim Reference copied from the output above>
```

## Deploying to TAP (using AWS RDS)

_note:_ Assumes TAP version >= 1.6

* Follow the steps [here](https://github.com/teddyking/the-dripping-tap/#aws-integration) to create the "rds-postgresql-default-vpc" offering, then:

```
$ tanzu service class-claim create rds-psql-1 --class rds-postgresql-default-vpc
$ tanzu service class-claim get rds-psql-1 # copy the Claim Reference from the output
$ tanzu apps workload create python-web-app-aws-rds-psql \
  --local-path . \
  --source-image <your image repo> \
  -l app.kubernetes.io/part-of=python-web-app-aws-rds-psql \
  --service-ref db=<the Claim Reference copied from the output above>
```

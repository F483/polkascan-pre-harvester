# Polkascan PRE Harvester
Polkascan PRE Harvester Python Application

## Description
The Polkascan PRE Harvester Application transforms a Substrate node's raw data into relational data for various classes of objects, such as: blocks, runtime metadata entities, extrinsics, events and various runtime data entities, such as: timestamps, accounts and balances.

## License
https://github.com/polkascan/polkascan-pre-harvester/blob/master/LICENSE

## Notes for Joystream development

## Tests

We are using the python unittest framework.

This required us to provide means for working with different
databases for development and unit testing.

Since harvester uses alembic and sqlalchemy, we have added a script in
the root folder that can be used for migrating the different
databases.

## Migrations

The `run_migrations.sh` script takes the first parameter as the name
of the environment to run alembic for. The rest of the arguments are
directly passed to alembic.

The requirement is that we have the various ^DB_*$ and ^DB_.*_TEST$
environment variables set as specified in `app/settings.py`

Once the evironment variables are in place, we can run migrations as:

`./run_migrations.sh development current`
`./run_migrations.sh development revision --autogenerate -m "Add a new model"`
`./run_migrations.sh development upgrade head`
`./run_migrations.sh development upgrade +1`
`./run_migrations.sh development downgrade -1`

Similarly for test environment, the same commands be run as:

`./run_migrations.sh test current`
`./run_migrations.sh test revision --autogenerate -m "Add a new model"`
`./run_migrations.sh test upgrade head`
`./run_migrations.sh test upgrade +1`
`./run_migrations.sh test downgrade -1`

## Running tests

Since we are using python unittest. You an run all tests as:

`python -m unittest`

Or run single test as

`python -m unittest tests/test_joystream_extrinsic.py`

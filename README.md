# Furtag

A reimplementation of @GeoCyberwolf's Furtag PHP app.

Original code: https://bitbucket.org/GeoCyberwolf/furtag

To use this:

- Set up a virtualenv: `python3 -m venv venv; . venv/bin/activate; pip install -r requirements.txt`
- Set `FLASK_APP`: `export FLASK_APP=myapp.app`
- Configure the database by editing myapp/myapp.cfg (use myapp.cfg.example as an example)
- Apply the migration to the database: `flask db upgrade`

For more information on flask-migrate, see https://flask-migrate.readthedocs.io/en/latest/ .


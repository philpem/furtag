# Developer notes

## Running in development mode:

```
python -m venv venv
. venv/bin/activate
pip3 install -r requirements.txt
cp regsys/regsys.cfg.example regsys/regsys.cfg

# edit regsys.cfg -- specifically change the secret key and enable a
# database backend.
#
# to generate a secret key:
#   dd if=/dev/urandom count=32k status=none | sha256sum | awk '{ print $1 }'

# initialise the database
python3 install.py

export FLASK_ENV=development
export FLASK_APP=regsys
flask run
```


## Database profiling and debugging

Database profiling requires the `sqltap` library.

It can be enabled in the config file (see `DEBUG_DB_PROFILING`).

To log all queries which are sent to the database, enable `DEBUG_DB_LOG`.


## Running under Gunicorn

`gunicorn -b 0.0.0.0:5000 regsys.app`


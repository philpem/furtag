Installing Regsys
=================

  - Check out the code using Mercurial.
  - Set up a virtualenv: ``python3 -m venv venv`` (creates a directory called
    ``venv``)
  - Activate the virtualenv: ``. venv/bin/activate``
  - Install the dependencies: ``pip install -r requirements.txt``
  - Install the database driver:
    - MySQL: ``pip install pymysql``
    - SQLite: This is included in the Python 3 distribution as ``sqlite3``.
    - PostgreSQL: ``pip install psycopg2``
  - Configure:
    - ``cp htaccess_venv.example .htaccess``
    - ``cp regsys/regsys.cfg.example regsys/regsys.cfg``
    - Edit ``regsys/regsys.cfg``:
      - Generate a secure secret key (``python -c 'import os; print(repr(os.urandom(30)))'``)
      - Copy the generated secret key into the ``SECRET_KEY`` field
      - Set the database connection string as appropriate
  - Create the database:
    - ``python3 install.py``

Note that the installation script will complain loudly if you haven't set the
``SECRET_KEY``.

The default administrator account credentials are:
  * Username: ``admin``
  * Password: ``password``

You must change the admin password as soon as you log in.


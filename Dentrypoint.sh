#!/bin/sh -e

# TODO find a better way to do this
if [ ! -f /var/lib/myapp/database_initialised ]; then
	echo "--- Database not present, creating... ---"
	python3 install.py
	touch /var/lib/myapp/database_initialised
fi

echo "Starting and daemonising Gunicorn..."
gunicorn -b 0.0.0.0:8000 myapp.app


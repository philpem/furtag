# This allows us to run in a Flask test environment without Apache, e.g.:
#   $ python -m myapp
#
from __future__ import absolute_import

from .app import app

app.run(debug=app.config.get('DEBUG', False))

# vim: ts=4 sw=4 noet

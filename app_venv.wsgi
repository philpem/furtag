#
# Example WSGI boot script
#
# Based on:
#   http://flask.pocoo.org/docs/0.10/deploying/mod_wsgi/#creating-a-wsgi-file
#   http://www.enigmeta.com/2012/08/16/starting-flask/
# Python3 fixes:
#   http://askubuntu.com/questions/488529/pyvenv-3-4-error-returned-non-zero-exit-status-1
#
import os, sys
import site

def _activate_env_from_path(env_path):
    """ Fix when `activate_this.py` does not exist.

        For Python 3.3 and newer, a new command-line tool `pyvenv` create venv
        will not provide 'activate_this.py'.
    """
    prev_sys_path = list(sys.path)

    if sys.platform == 'win32':
        site_packages_paths = [os.path.join(env_path, 'Lib', 'site-packages')]
    else:
        lib_path = os.path.join(env_path, 'lib')
        site_packages_paths = [os.path.join(lib_path, lib, 'site-packages')
                               for lib in os.listdir(lib_path)]
    for site_packages_path in site_packages_paths:
        site.addsitedir(site_packages_path)

    sys.real_prefix = sys.prefix
    sys.prefix = env_path
    sys.exec_prefix = env_path

    # Move the added items to the front of the path:
    new_sys_path = []
    for item in list(sys.path):
        if item not in prev_sys_path:
            new_sys_path.append(item)
            sys.path.remove(item)
    sys.path[:0] = new_sys_path


# figure out where we are
basepath = os.path.abspath(os.path.dirname(__file__))

# set up the local VEnv environment (we need this for SQLAlchemy and Flask)
activate_this = os.path.abspath(os.path.join(basepath, 'venv/bin/activate_this.py'))
try:
    with open(activate_this) as f:
    	code = compile(f.read(), activate_this, 'exec')
    	exec(code, dict(__file__=activate_this))
except IOError:
    _activate_env_from_path(os.path.abspath(os.path.join(basepath, 'venv')))


# plop the application onto the search path
sys.path.insert(0, basepath)

# now bring up the application!
from myapp.app import app as application


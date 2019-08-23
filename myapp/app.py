from __future__ import absolute_import, unicode_literals

from flask import Flask, render_template, redirect, request, url_for, flash, g
from flask_login import (LoginManager, current_user, login_required,
		login_user, logout_user, confirm_login, fresh_login_required)
from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, TextField
from wtforms.validators import Required
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
import os

# Subclass the application so we can add the menu management functions
class AppClass(Flask):
	def __init__(self, *args, **kwargs):
		# Let Flask initialise itself
		super(AppClass, self).__init__(*args, **kwargs)
		# Now create an empty menu object and set up the context processor
		self._myapp_menudata = None

	def add_menu_item(self, label, endpoint, sortorder=0):
		if self._myapp_menudata is None:
			self._myapp_menudata = list()
		self._myapp_menudata.append(dict(label=label, endpoint=endpoint, sortorder=sortorder))

# create and configure the application
app = AppClass(__name__)
app.config.from_pyfile('myapp.cfg')

# provide a link to the application for gunicorn
application = app

# tell jinja to remove extraneous whitespace
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

# enable database logging (if enabled)
if app.config.get('DEBUG_DB_LOG', False):
	from flask.logging import default_handler
	import logging
	app.logger.warning('Warning - database logging enabled. This will spam the logs!')
	logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
	logging.getLogger('sqlalchemy.engine').addHandler(default_handler)

# start database profiling (if enabled)
if app.config.get('DEBUG_DB_PROFILING', False):
	app.logger.warning('Warning - database profiling enabled. Do not use this in production!')
	try:
		import sqltap
	except:
		app.logger.error('Cannot import sqltap. Install it with pip to use profiling!')
		raise

	def context_fn(*args):
		import uuid
		try:
			return g.req_id
		except AttributeError:
			g.req_id = uuid.uuid4().hex
			return g.req_id

	sqltap_sess = sqltap.start(user_context_fn = context_fn)

# -- main menu handing (context processor) --
@app.context_processor
def _myapp_contextproc_menu():
	"""
	Context processor for the main menu

	Adds the main menu data into the template context. Menu items are sorted by sort-order, then (case-insensitively) by label.
	"""
	return dict(menu=sorted(app._myapp_menudata, key=lambda mi: (mi['sortorder'], mi['label'].lower())))


# -- post-request teardown --
@app.teardown_request
def shutdown_session(exception=None):
	# if database profiling is enabled, save a report
	if app.config.get('DEBUG_DB_PROFILING', False) and not request.path.startswith('/static'):
		# filter out any statistics which aren't for this request
		stats_all = sqltap_sess.collect()
		stats_req = list(filter(lambda x: x.user_context == g.req_id, sqltap_sess.collect()))
		sqltap.report(stats_all, os.path.join(os.path.dirname(os.path.realpath(__file__)), "static/db_profile_report_all.html"))
		sqltap.report(stats_req, os.path.join(os.path.dirname(os.path.realpath(__file__)), "static/db_profile_report_req.html"))

# -- login management --

from .database import User

# Flask-Login configuration
login_manager = LoginManager()
login_manager.setup_app(app)
login_manager.login_view = 'login'
login_manager.login_message = u'Please log in to access this page.'

# TODO -- For 'fresh_login_required' to work, we need a "reauthenticate" handler.
#   See https://github.com/maxcountryman/flask-login/blob/master/example/login-example.py for a code example
#login_manager.refresh_view = 'reauth'
#login_manager.needs_refresh_message = u'To protect your account, please re-authenticate to access this page.'

@login_manager.user_loader
def load_user(userid):
	userrec = None
	try:
		userrec = User.query.filter(User.id == int(userid)).one()
	except MultipleResultsFound:
		app.logger.error("USER LOGIN FAILURE: User '%s' has a doppelganger (duplicate username found)")
	except NoResultFound:
		app.logger.warning("Userloader: id '%d' returned no results" % int(userid))
		pass # with userrec = None
	return userrec

@app.route("/login", methods=["GET","POST"])
def login():
	class LoginForm(FlaskForm):
		username=TextField("Username", validators=[Required()])
		password=PasswordField("Password", validators=[Required()])
		submit=SubmitField("Log in")

	form = LoginForm()
	if form.validate_on_submit():
		# login and validate the user
		userrec = None
		try:
			userrec = User.query.filter(User.username == form.username.data).one()
		except MultipleResultsFound:
			app.logger.error("USER LOGIN FAILURE: User '%s' has a doppelganger (duplicate username found)")
		except NoResultFound:
			pass # with userrec = None

		if userrec is not None:
			# check password
			if userrec.checkPassword(form.password.data):
				login_user(userrec)
				#flash("Logged in successfully", "success")
				return redirect(request.args.get("next") or url_for("myapp.blueprints.index.index"))

	if request.method == 'POST':
		flash("Error logging in - please check your username and password and ensure that CAPS LOCK is turned off.", "error")
	return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
	logout_user()
	flash("You have now been logged out.", "info")
	return redirect(url_for("login"))

# vim: ts=4 sw=4 noet

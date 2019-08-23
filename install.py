# install script
# creates all the required databases
# python install.py

from flask import Flask
from myapp.database import db, User
import sys

if __name__ == '__main__':
	# quickly check that the user hasn't left the secret key at the default setting
	# Create a Flask instance so we can access the application configuration
	app = Flask(__name__)
	app.config.from_pyfile('myapp/myapp.cfg')
	if app.config['SECRET_KEY'] == "0123456789ABCDEF":
		print("Secret key has not been set!")
		print("Please read the installation instructions.")
		sys.exit(1)

	# initialise the database
	db.create_all()

	# Create an 'admin' user (but only if one does not exist already)
	if User.query.filter(User.username == 'admin').first() != None:
		print("User 'admin' already exists. Skipping user create.")
	else:
		print("Creating new administrator user 'admin' with password 'password'.")
		adminUser = User()
		adminUser.username = 'admin'
		adminUser.setPassword('password')
		db.session.add(adminUser)
		db.session.flush()
		db.session.commit()

# vim: noet ts=4 sw=4

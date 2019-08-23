from sqlalchemy import Column, ForeignKey, Sequence
from sqlalchemy import Integer, String, Text, Enum
from sqlalchemy.orm import relationship, backref
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import bcrypt
from .app import app

db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Links (tags)
class Tag(db.Model):
	__tablename__ = 'ft_tag'
	tag_id			= Column(Integer, Sequence('link_id_seq'), primary_key=True)
	tag_url			= Column(String(200))
	owner_id		= relationship("User", backref='links')

# User
class User(db.Model):
	__tablename__ = 'user'
	id				= Column(Integer, Sequence('user_id_seq'), primary_key=True)
	username		= Column(String(50), nullable=False, unique=True)
	password_hash	= Column(String(60), nullable=False)

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		if self.id is not None:
			return str(self.id)

	def setPassword(self, password):
		# Hash the password with Bcrypt
		self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

	def checkPassword(self, password):
		# Use Bcrypt to verify the password
		try:
			return (bcrypt.hashpw(password.encode('utf-8'), self.password_hash) == self.password_hash)
		except:
			# Bcrypt throws a ValueError if the salt is invalid (wrong password format)
			# In which case it's a fair bet the account is locked or has been mucked around with.
			return False

# vim: ts=4 sw=4 noet

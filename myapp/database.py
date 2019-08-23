from sqlalchemy import Column, ForeignKey, Sequence
from sqlalchemy import Integer, String, Text, Enum
from sqlalchemy.orm import relationship, backref
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import bcrypt
from .app import app

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Category
class Category(db.Model):
	__tablename__ = 'category'
	id				= Column(Integer, Sequence('category_id_seq'), primary_key=True)
	parent_id		= Column(Integer, ForeignKey('category.id'))
	name			= Column(String(200))
	children		= relationship("Category", backref=backref('parent', remote_side=[id]))
	parts			= relationship("Part")

# Company
class Company(db.Model):
	__tablename__ = 'company'
	id				= Column(Integer, Sequence('company_id_seq'), primary_key=True)
	name			= Column(String(200), nullable=False, unique=True)
	short_name		= Column(String(50))
	website			= Column(String(200))
	notes			= Column(Text)
	type			= Column(Enum('supplier', 'manufacturer', 'both'), nullable=False)
	parts			= relationship("Part")

# Container
class Container(db.Model):
	__tablename__ = 'container'
	id				= Column(Integer, Sequence('container_id_seq'), primary_key=True)
	parent_id		= Column(Integer, ForeignKey('container.id'))
	name			= Column(String(50), nullable=False)
	description		= Column(String(200))
	children		= relationship("Container", backref=backref('parent', remote_side=[id]))
	# TODO: Stockentries
	contents		= relationship("StockEntry")

# Part
class Part(db.Model):
	__tablename__ = 'part'
	id				= Column(Integer, Sequence('part_id_seq'), primary_key=True)
	manufacturer_id	= Column(Integer, ForeignKey('company.id'), nullable=False)
	part_number		= Column(String(255), nullable=False)
	stock_code		= Column(String(255))
	description		= Column(Text, nullable=False)
	notes			= Column(Text)
	category		= Column(Integer, ForeignKey('category.id'))
	manufacturer	= relationship("Company")
	attachments		= relationship("PartAttachment")
	# Relations where this part is the source
	related_source	= relationship("PartRelation", primaryjoin='Part.id==PartRelation.src_part_id')
	# Relations where this part is the target
	related_target	= relationship("PartRelation", primaryjoin='Part.id==PartRelation.dest_part_id')
	# Any relation
	# TODO - "Bidirectional" attribute, get rid of rel_src and rel_tgt.
	related_any		= relationship("PartRelation", primaryjoin='or_(Part.id==PartRelation.src_part_id, Part.id==PartRelation.dest_part_id)')

# Attachments (e.g. datasheets) associated with parts
class PartAttachment(db.Model):
	__tablename__ = 'part_attachment'
	id				= Column(Integer, Sequence('part_attachment_id_seq'), primary_key=True)
	part_id			= Column(Integer, ForeignKey('part.id'), nullable=False)
	# TODO: Download filename, UUID, etc.

# Relation between two parts
class PartRelation(db.Model):
	__tablename__ = 'part_relation'
	id				= Column(Integer, Sequence('part_relation_id_seq'), primary_key=True)
	src_part_id		= Column(Integer, ForeignKey('part.id'), nullable=False)
	dest_part_id	= Column(Integer, ForeignKey('part.id'), nullable=False)
	notes			= Column(Text)
	type			= Column(Enum('exact', 'similar', 'accessory'), nullable=False)
	src_part		= relationship("Part", primaryjoin="Part.id==PartRelation.src_part_id")
	dest_part		= relationship("Part", primaryjoin="Part.id==PartRelation.dest_part_id")

# Stock holding information
class StockEntry(db.Model):
	__tablename__ = 'stock_entry'
	id				= Column(Integer, Sequence('stock_entry_id_seq'), primary_key=True)
	part_id			= Column(Integer, ForeignKey('part.id'), nullable=False)
	location_id		= Column(Integer, ForeignKey('container.id'), nullable=False)
	supplier_id		= Column(Integer, ForeignKey('company.id'), nullable=False)
	stockqty		= Column(Integer, nullable=False)
	# TODO: unit of measure
	notes			= Column(Text)
	supplier		= relationship("Company")
	part			= relationship("Part")
	location		= relationship("Container")

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

import os
from .app import app

from .blueprints import dashboard

def load_blueprints():
	""" Load all the blueprints (modules or .py files) in a specified directory and its subdirectories.
	Returns a list of module objects (as returned by __import__)
	"""

	mods = list()

	# import all modules and packages in the 'blueprints' directory
	import pkgutil
	from . import blueprints
	for importer,modname,ispkg in pkgutil.iter_modules(blueprints.__path__):
		try:
			# import the module and add it to 'mods'
			module = __import__("blueprints.%s" % modname, globals(), locals(), [modname], 1)
			mods.append(module)
			app.logger.debug("load_blueprints: Loaded %s" % modname)
		except Exception as e:
			app.logger.error("load_blueprints: Blueprint '%s' failed to load: %s" % (modname, e))
			continue

	return mods


# Load pluggable blueprints
for blueprint in load_blueprints():
	try:
		app.register_blueprint(getattr(blueprint, 'blueprint'))
	except Exception as e:
		app.logger.error("init: Blueprint '%s' failed to load: %s" % (blueprint, e))

# vim: ts=4 sw=4 noet

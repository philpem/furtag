#!/usr/bin/env python3
#
# Run regsys in debug mode
#
# run: python3 devtools/run_debug.py

import os, os.path, sys

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from regsys.app import app

if __name__ == '__main__':
	def walk(path, ext=None):
		extra_files=[path,]
		for dirname, dirs, files in os.walk(path):
			for filename in files:
				if ext != None and filename[-len(ext):] != ext:
					continue
				filename = os.path.join(dirname, filename)
				if os.path.isfile(filename):
					extra_files.append(filename)
		return extra_files

	# create a list of extra files to watch
	extra_files = []
	extra_files.extend(walk('regsys/blueprints', '.py'))
	extra_files.extend(walk('regsys/templates', '.html'))

	# start the application
	app.run(debug=True, extra_files=extra_files)

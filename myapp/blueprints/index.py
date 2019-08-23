from flask import Blueprint, render_template
from flask_login import current_user, login_required
from ..app import app

blueprint = Blueprint(__name__, __name__,
		template_folder='templates')

app.add_menu_item("Viewer", "%s.index" % __name__, -1000)

# -- dashboard --
@blueprint.route("/")
def index():
	return render_template('dashboard.html')


# vim: ts=4 sw=4 noet

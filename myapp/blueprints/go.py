from flask import Blueprint, render_template
from flask_login import current_user, login_required
from ..app import app
from ..database import Tag

blueprint = Blueprint(__name__, __name__,
		template_folder='templates')

# go to tag url
@blueprint.route('/go/<int:tag_id>')
def go(tag_id):
	tagrec = Tag.query.filter(Tag.tag_id == tag_id).one()
	if tagrec is not None:
		return redirect(tagrec.tag_url)
	else:
		return render_template('tag_not_found.html'), 404

# vim: ts=4 sw=4 noet

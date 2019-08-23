from flask import Blueprint, render_template, redirect
from flask_login import current_user, login_required
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from ..app import app
from ..database import Tag

blueprint = Blueprint(__name__, __name__,
		template_folder='templates')

# go to tag url
@blueprint.route('/go/<int:tag_id>')
def go(tag_id):
	try:
		tagrec = Tag.query.filter(Tag.tag_id == tag_id).one()
		return redirect(tagrec.tag_url)
	except (NoResultFound, MultipleResultsFound):
		return render_template('tag_not_found.html'), 404

# vim: ts=4 sw=4 noet

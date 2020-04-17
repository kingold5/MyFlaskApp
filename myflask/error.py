# pylint: disable=missing-docstring,too-few-public-methods,invalid-name,line-too-long,wrong-import-order
from flask import render_template
from myflask import app, db


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error_404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('error_500.html'), 500

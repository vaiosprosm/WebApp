from flask import render_template
from WebApp import app
from flask_wtf.csrf import CSRFError
from werkzeug.exceptions import HTTPException
import json


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('errors/csrf_error.html', reason=e.description), 400

@app.errorhandler(404)
def page_not_found(e):
    #note that we set the 404 status explicitly
    return render_template('errors/404.html'),404

@app.errorhandler(415)
def unsupported_media_type(e):
    # note that we set the 415 status explicitly
    return render_template('errors/415.html'), 415

@app.errorhandler(500)
def internal_server_error(e):
    # note that we set the 500 status explicitly
    return render_template('errors/500.html',e=e),500


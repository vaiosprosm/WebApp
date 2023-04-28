from flask import render_template
from WebApp import app

@app.errorhandler(404)
def page_not_found(e):
    #note that we set the 404 status explicitly
    return render_template('errors/404.html'),404


@app.errorhandler(500)
def internal_server_error(e):
    # note that we set the 500 status explicitly
    return render_template('errors/500.html',e=e),500
### ERROR HANDLERS END ###
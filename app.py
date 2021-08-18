from flask import Flask, render_template

def page_not_found(e):
    return render_template('index.html'), 404
    
def create_app():
    app = Flask(__name__)
    app.register_error_handler(404, page_not_found)
    import blueprint
    app.register_blueprint(blueprint.bp)
    return app
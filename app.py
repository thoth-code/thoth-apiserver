from flask import Flask, render_template

def page_not_found(e):
    return render_template('index.html'), 200
    
def create_app():
    app = Flask(__name__)
    app.register_error_handler(404, page_not_found)
    import blueprint
    app.register_blueprint(blueprint.bp)
    return app

if __name__ == '__main__' :
    create_app().run(host='0.0.0.0')
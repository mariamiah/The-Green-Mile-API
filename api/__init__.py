from flask import Flask, jsonify
from api.views.user_views import user
from api.views.package_views import package
from api.views.invoice_views import invoice
from api.views.status_views import status
from decouple import config
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)
CORS(app)
app.register_blueprint(user)
app.register_blueprint(package)
app.register_blueprint(invoice)
app.register_blueprint(status)
app.config['JWT_SECRET_KEY'] = config('JWT_SECRET_KEY')
jwt = JWTManager(app)


# Define a swagger template
template = {
    "swagger": "2.0",
    "info": {
        "title":
        "Green Mile API",
        "description":
        "Green Mile is an application that helps owners manage\
         package deliveries",
        "version":
        "1.0.0"
    },
    "schemes": ["http", "https"]
}

# Instantiate swagger docs
swagger = Swagger(app, template=template)



@app.route('/')
def index():
    return jsonify({"message": "welcome to the green mile application"})



@app.route('/apidocs')
def showdocs():
    return redirect('/apidocs/')
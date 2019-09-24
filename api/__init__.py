from flask import Flask, jsonify
from api.views.user_views import user
from api.views.package_views import package
from api.views.invoice_views import invoice
from api.views.status_views import status
from decouple import config
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.register_blueprint(user)
app.register_blueprint(package)
app.register_blueprint(invoice)
app.register_blueprint(status)
app.config['JWT_SECRET_KEY'] = config('JWT_SECRET_KEY')
jwt = JWTManager(app)


@app.route('/')
def index():
    return jsonify({"message": "welcome to the green mile application"})

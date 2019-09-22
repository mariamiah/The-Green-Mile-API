from flask import Flask, jsonify
from api.views.user_views import user
from api.views.package_views import package
from decouple import config
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.register_blueprint(user)
app.register_blueprint(package)
app.config['JWT_SECRET_KEY'] = config('JWT_SECRET_KEY')
jwt = JWTManager(app)

@app.route('/')
def index():
    return jsonify({"message": "welcome to the green mile application"})
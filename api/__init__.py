from flask import Flask, jsonify
from api.views.user_views import user

app = Flask(__name__)
app.register_blueprint(user)

@app.route('/')
def index():
    return jsonify({"message": "welcome to the green mile application "})
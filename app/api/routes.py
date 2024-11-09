from flask import Blueprint, jsonify

# Define a blueprint that will contain all routes.
api_bp = Blueprint('api', __name__)

# test route to see server is starting up
@api_bp.route('/test', methods=['GET'])
def test():
    return jsonify(message="Flask server is up and running!")

from controller.contoller import index, serve_js, serve_css, serve_media, stockAlert
from flask import Blueprint, send_from_directory
blueprint = Blueprint('home', __name__, static_folder='static')
blueprint.route('/', methods=['GET'])(index)
blueprint.route('/static/js/<path:path>', methods=['GET'])(serve_js)
blueprint.route('/static/css/<path:path>', methods=['GET'])(serve_css)
blueprint.route('/static/media/<path:path>', methods=['GET'])(serve_media)
blueprint.route('/api/v1/stockAlert', methods=['POST'])(stockAlert)




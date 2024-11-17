from flask import Flask, jsonify
import os
from flask_up import up_ul
from flask_cors import CORS

opw = os.getenv('opw')
app = Flask(__name__)

CORS(app)

@app.route('/')
def hello_world():
    return 'Hello from Koyeb'

@app.route('/upload')
def up_f():
    required_params = ['url', 'opw']
    missing_params = [param for param in required_params if not request.args.get(param)]
    if missing_params:
        return jsonify({
            's':0,
            'error': 'Some required parameters are missing or empty'
        }), 400
    url = request.args.get('url')
    #cid = request.args.get('cid')
    rpw = int(request.args.get('opw'))
    if opw == rpw:
        return await up_ul(url)

    else:
        return jsonify({
            's':0,
            'error': 'auth failed'
        }), 400
if __name__ == "__main__":
    app.run(port=8000)

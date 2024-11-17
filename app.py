from flask import Flask
import os, time
from bot import bot
from moviepy.editor import VideoFileClip
from display_progress import progress_for_pyrogram, humanbytes, TimeFormatter
import requests
import math
from PIL import Image

opw = 2003
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Koyeb'

@app.route('/upload')
def up_f():
    required_params = ['url', 'cid', 'opw']
    missing_params = [param for param in required_params if not request.args.get(param)]
    if missing_params:
        return jsonify({
            's':0,
            'error': 'Some required parameters are missing or empty'
        }), 400
    url = request.args.get('url')
    cid = request.args.get('cid')
    opw = request.args.get('opw')
    

if __name__ == "__main__":
    app.run(port=8000)

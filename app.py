from flask import Flask, jsonify
import os
#from flask_up import up_ul
from flask_cors import CORS
from pyrogram import Client
from bot import bot,
from bot import

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
      try:
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))  
        filename = url.split("/")[-1]  # Extract the filename from the URL
        if '?' in filename:
           filename = filename.split("?")[0]
        
        downloaded_size = 0  # Track the downloaded size
        with open(filename, 'wb') as file:
           for chunk in response.iter_content(chunk_size=1024):
               if chunk:
                  file.write(chunk)
                  downloaded_size += len(chunk)
                  # Update progress approximately every 2%
                  if total_size > 0 and downloaded_size % (total_size // 50) == 0:
                      #make a progress bar...
                      progress_i = int(20 * downloaded_size / total_size)
                      progress='[' + '✅️' * progress_i + '❌️' * (20 - progress_i) + ']'
                      #progress = progress_bar(downloaded_size, total_size)
                      percent = (downloaded_size / total_size) * 100
                      #await reply_msg.edit_text(f"Downloading: {progress} {percent:.2f}%")
                      print(percent)
        thumb_path='thumb.jpg'
        with VideoFileClip(filename) as video:
              frame = video.get_frame(3.0)
              img = Image.fromarray(frame)
              img.save(thumb_path, "JPEG")
        #await reply_msg.edit("Thumbnail generated. Uploading to Telegram...")
        start_time=time.time()
        s_vid = await bot.send_video(
          chat_id=mcid,
          video=filename,
          caption=f'{filename}',
          thumb=thumb_path,
          supports_streaming=True
        )
        try:
           os.remove(filename)
           if thumb_path and os.path.exists(thumb_path):
             os.remove(thumb_path)
        except Exception as e:
           pass
        return jsonify({
            's':1,
            'msg': 'done!',
            'fid': s_vid.video.file_id
          }), 200
    except Exception as e:
        print(f"Err while dl:{e}")
        return jsonify({
            's':0,
            'error': f'Err while uplaod: {e}',
        }), 400
 else:
    return jsonify({
      's':0,
      'error': 'auth failed'
     }), 400
if __name__ == "__main__":
    app.run(port=8000)

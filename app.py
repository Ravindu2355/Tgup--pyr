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
    try:
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
      await bot.send_video(
          chat_id=cid,
          video=filename,
          caption=f'Uploaded: {filename}',
          thumb=thumb_path,
          supports_streaming=True,  # Ensure the video is streamable
          progress=progress_for_pyrogram,
          progress_args=(
            "uploading!",
             reply_msg,
             start_time
           )
      )
      try:
         os.remove(filename)
         if thumb_path and os.path.exists(thumb_path):
           os.remove(thumb_path)
      except Exception as e:
         pass

    except Exception as e:
        print(f"Err while dl:{e}")
        

if __name__ == "__main__":
    app.run(port=8000)

import os, time
from pyrogram import Client, filters
from pyrogram.types import Message
from moviepy.editor import VideoFileClip
from display_progress import progress_for_pyrogram, humanbytes, TimeFormatter
import requests
import math


# Load environment variables for API credentials
API_ID = os.getenv('apiid')
API_HASH = os.getenv('apihash')
BOT_TOKEN = os.getenv('tk')

# Ensure all required environment variables are set
if not all([API_ID, API_HASH, BOT_TOKEN]):
    raise ValueError("API_ID, API_HASH, and BOT_TOKEN environment variables must be set.")

# Create the Pyrogram client
app = Client("bot_session", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Function to format progress as a progress bar
def progress_bar(completed, total, length=20):
    progress = int(length * completed / total)
    return '[' + '=' * progress + ' ' * (length - progress) + ']'

# Function to generate a thumbnail from a video using ffmpeg

@app.on_message(filters.command("upload") & filters.private)
async def upload_from_url(client: Client, message: Message):
    try:
        # Check if the command contains a URL argument
        if len(message.text.split()) < 2:
            await message.reply("Please provide a URL!")
            return

        # Extract the URL from the command
        url = message.text.split()[1]
        reply_msg = await message.reply("Starting download...")

        # Start downloading the file
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))  # Get the total file size
        filename = url.split("/")[-1]  # Extract the filename from the URL
        
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
                        await reply_msg.edit_text(f"Downloading: {progress} {percent:.2f}%")
                        print(percent)
        await reply_msg.edit_text("Download complete. Generating thumbnail...")

        # Generate a thumbnail for the video
        #await reply_msg.edit_text("Thumbnail generated. Uploading to Telegram...")

        # Send the file with the thumbnail and streamable option
        thumb_path='thumb.jpg'
        with VideoFileClip(filename) as video:
              frame = video.get_frame(3.0)
              img = Image.fromarray(frame)
              img.save(thumb_path, "JPEG")
        await reply_msg.edit("Thumbnail generated. Uploading to Telegram...")
        start_time=time.time()
        await client.send_video(
            chat_id=message.chat.id,
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
        
        # Clean up the local files after uploading
        os.remove(filename)
        if thumb_path and os.path.exists(thumb_path):
            os.remove(thumb_path)

        await reply_msg.edit_text("Upload complete!")

    except Exception as e:
        # Handle any errors and notify the user
        await message.reply(f"An error occurred: {str(e)}")

# Start the bot and keep it running
print("Bot is running...")
app.run()

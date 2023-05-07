from pyrogram import Client
from matrix_api import MatrixClient
from config import API_ID, API_HASH, TELEGRAM_TITLE, MATRIX_HOMESERVER, ACCESS_TOKEN, ROOM_ID, TEST_ROOM_ID

app = Client('my_account', api_id=API_ID, api_hash=API_HASH)

@app.on_message()
def read_post(clinet, msg):
    if msg.chat.title == TELEGRAM_TITLE:
        matrix = MatrixClient(ACCESS_TOKEN=ACCESS_TOKEN, ROOM_ID=ROOM_ID, MATRIX_HOMESERVER=MATRIX_HOMESERVER)
        try:
            if msg.photo:
                media_format = "jpg"
            elif msg.video:
                media_format = "mp4"
            else:
                matrix.send_text(msg.text)
                
            app.download_media(msg.media.file_id, file_name=f'{msg.media.file_unique_id}.{media_format}')
            media_path = f'downloads/{msg.media.file_unique_id}.{media_format}'
            
            if msg.caption:
                matrix.send_media(media_path, msg.caption)
            else:
                matrix.send_media(media_path)
        except Exception as ex:
            print(f"ERROR:{ex}") 
    else:
        pass


app.run()
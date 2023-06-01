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
                message_type = "m.image"
                file_id = msg.photo.file_id
                file_unique_id = msg.photo.file_unique_id
            elif msg.video:
                media_format = "mp4"
                message_type = "m.video"
                file_id = msg.video.file_id
                file_unique_id = msg.video.file_unique_id
            elif msg.animation:
                media_format = "gif"
                message_type = "m.video"
                file_id = msg.animation.file_id
                file_unique_id = msg.animation.file_unique_id
            else:
                matrix.send_text(msg.text)
                
            app.download_media(file_id, file_name=f'{file_unique_id}.{media_format}')
            media_path = f'downloads/{file_unique_id}.{media_format}'
            
            if msg.caption:
                matrix.send_media(filename=media_path, msgtype=message_type, body=msg.caption)
            else:
                matrix.send_media(filename=media_path, msgtype=message_type)
        except Exception as ex:
            print(f"ERROR:{ex}") 
    else:
        pass


app.run()

import os
import sys
import uuid
import json
import logging
import requests
from datetime import datetime

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

class MatrixClient:

    def __init__(self, ACCESS_TOKEN, ROOM_ID, MATRIX_HOMESERVER):
        """
        Initializes the MatrixClient with the provided access token, room ID, and Matrix homeserver URL.

        Args:
            ACCESS_TOKEN (str): The access token for the Matrix client.
            ROOM_ID (str): The ID of the room to send messages to.
            MATRIX_HOMESERVER (str): The URL of the Matrix homeserver. Defaults to "https://matrix.org".
        """
        self.ACCESS_TOKEN = ACCESS_TOKEN
        self.ROOM_ID = ROOM_ID
        self.MATRIX_HOMESERVER = MATRIX_HOMESERVER 
        self.MEDIA_API_URL = f"{MATRIX_HOMESERVER}/_matrix/media/r0/upload"
        self.logger = logging.getLogger(__name__)


    def send_text(self, body):
        """
        Sends a text message to the Matrix server.

        Args:
            body (str): The body of the text message to send.

        Returns:
            The response object, or None if the message failed to send.
        """
        message = {
            "body": body,
            "msgtype": "m.text"
        }
        try:
            response = requests.put(
                f"{self.MATRIX_HOMESERVER}/_matrix/client/r0/rooms/{self.ROOM_ID}/send/m.room.message/{self.transaction_id()}",
                headers={
                    "Authorization": f"Bearer {self.ACCESS_TOKEN}",
                    "Content-Type": "application/json",
                    "accept": "application/json",
                },
                json=message
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.logger.error("Error sending text message: %s", e)
            return None
        
        self.logger.info("Text message sent successfully\nINFO:body='%s'", body)
        return response


    def upload_media(self, filename, media_type):
        """
        Uploads a media file to the Matrix server.
        
        Args:
            filename (str): The path to the media file to upload.
            media_type (str): The media type of the file being uploaded. 
                Can be one of "image/jpeg", "image/png", "image/gif", "video/mp4", "audio/mpeg".
        
        Returns:
            The content URI of the uploaded media, or None if the upload failed.
        """
        try:
            with open(filename, "rb") as f:
                response = requests.post(
                    self.MEDIA_API_URL,
                    headers={
                        "Authorization": f"Bearer {self.ACCESS_TOKEN}",
                        "Content-Type": f"{media_type}"
                    },
                    data=f.read()
                )
            response.raise_for_status()
        except (OSError, requests.exceptions.RequestException) as e:
            self.logger.error("Error uploading image: %s", e)
            return None
        
        media_url = json.loads(response.text)["content_uri"]
        self.logger.info("Image uploaded successfully")
        return media_url


    def send_media(self, filename, msgtype, body=""):
        """
        Sends a media file to the Matrix server.

        Args:
            filename (str): The path to the media file to send.
            body (str): The message body to accompany the media file.

        Returns:
            The response object, or None if the message failed to send.
        """
        
        content_types = {
            ".gif": "image/gif",
            ".mp4": "video/mp4",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".mp3": "audio/mpeg",
        }
        file_extension = os.path.splitext(filename)[1]
        media_type = content_types.get(file_extension)

        media_url = self.upload_media(filename, media_type=media_type)
        if not media_url:
            return None

        message = {
            "body": body,
            "url": media_url,
            "msgtype": msgtype,
        }
        try:
            response = requests.put(
                f"{self.MATRIX_HOMESERVER}/_matrix/client/r0/rooms/{self.ROOM_ID}/send/m.room.message/{self.transaction_id()}",
                headers={
                    "Authorization": f"Bearer {self.ACCESS_TOKEN}",
                    "Content-Type": "application/json",
                    "accept": "application/json",
                },
                json=message
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.logger.error("Error sending image: %s", e)
            return None
        
        self.logger.info("Image sent successfully\nINFO:filenane='%s'", filename)
        return response


    @staticmethod
    def transaction_id():
        return int(uuid.uuid4())

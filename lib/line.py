import requests

from .consts import LINE_NOTIFY_URL

def post_to_line_notify(
    message: str,
    token: str
):
    r = requests.post(
        LINE_NOTIFY_URL,
        headers = {
            'Authorization' : f'Bearer {token}'
        },
        params = {
            'message': message
        }
    )

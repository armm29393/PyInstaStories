from instagrapi import Client
from pathlib import Path
import time
import os

ACCOUNT_USERNAME = ''
ACCOUNT_PASSWORD = ''
IG_CREDENTIAL_PATH = f'./ig_settings_{ACCOUNT_USERNAME}.json'
SLEEP_TIME = '20' # in seconds

def main(username: str, amount: int = 5) -> dict:
    """
    Download all medias from instagram profile
    """
    amount = int(amount)
    cl = Client()
    if os.path.exists(IG_CREDENTIAL_PATH):
        cl.load_settings(IG_CREDENTIAL_PATH)
        cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)
    else:
        cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)
        cl.dump_settings(IG_CREDENTIAL_PATH)
    user_id = cl.user_id_from_username(username)
    medias = cl.user_medias(user_id)
    result = {}
    i = 0
    for m in medias:
        if i >= amount:
            break
        paths = []
        if m.media_type == 1:
            # Photo
            dir = f'./{username}/photo'
            paths.append(cl.photo_download(m.pk, dir))
        elif m.media_type == 2 and m.product_type == 'feed':
            # Video
            dir = f'./{username}/video'
            paths.append(cl.video_download(m.pk, dir))
        elif m.media_type == 2 and m.product_type == 'igtv':
            # IGTV
            dir = f'./{username}/igtv'
            paths.append(cl.video_download(m.pk, dir))
        elif m.media_type == 2 and m.product_type == 'clips':
            # Reels
            dir = f'./{username}/reels'
            paths.append(cl.video_download(m.pk, dir))
        elif m.media_type == 8:
            # Album
            dir = f'./{username}/album'
            for path in cl.album_download(m.pk, dir):
                paths.append(path)
        result[m.pk] = paths
        print(f'http://instagram.com/p/{m.code}/', paths)
        i += 1
        time.sleep(int(SLEEP_TIME))
    return result

def initial(username):
    dirs = [
        f'./{username}/photo',
        f'./{username}/video',
        f'./{username}/igtv',
        f'./{username}/reels',
        f'./{username}/album',
    ]
    for dir in dirs:
        Path(dir).mkdir(parents=True, exist_ok=True)

if __name__ == '__main__':
    username = input('Enter username: ')
    while True:
        amount = input('How many posts to process (default: 5)? ').strip()
        if amount == '':
            amount = '5'
        if amount.isdigit():
            break
    initial(username)
    main(username, amount)

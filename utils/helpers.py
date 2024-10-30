import re


def sanitize_filename(url):
    return re.sub(r'[\\/*?:"<>|]', "_", url)

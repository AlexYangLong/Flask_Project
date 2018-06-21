import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

UPLOAD_DIR = os.path.join(BASE_DIR, 'static/upload')

if not os.path.exists(UPLOAD_DIR):
    os.mkdir(UPLOAD_DIR)

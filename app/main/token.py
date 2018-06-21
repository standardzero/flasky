from itsdangerous import URLSafeTimedSerializer
from flask import current_app


def generate_confirmation_token(blog_id):
    serialzer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serialzer.dumps(blog_id, salt='hard to guess me')


def confirm_token(token, expiration=36000):
    serialzer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        info = serialzer.loads(token, salt='hard to guess me',
                                  max_age=expiration)
    except:
        info = None
    return info

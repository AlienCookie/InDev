import os

import jwt

private_key_path = os.environ.get('GP_RSA_PRIVATE_KEY_PATH', '/var/run/secrets/test/rsa/id_rsa')
public_key_path = os.environ.get('GP_RSA_PUBLIC_KEY_PATH', '/var/run/secrets/test/rsa/id_rsa.pub')

def encode_user_token(user_id):
    with open(private_key_path) as s:
        data = {
            'user': {
                'id': user_id
            },
            'type': 'user'
        }

        return jwt.encode(data, key=s.read(), algorithm='RS256')

def decode(encoded):
    with open(public_key_path) as s:
        return jwt.decode(encoded, key=s.read(), algorithm='RS256')

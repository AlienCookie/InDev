import base64
from functools import wraps

from flask import Flask, g, jsonify, request, abort

from pygputils import get_logger
from pygputils.db import DB, connect_db
from pygputils.token import decode

app = Flask(__name__)
app.url_map.strict_slashes = False

logger = get_logger('gpflask')

def get_token():
    auth = dict(request.headers).get('Authorization', None)
    cookie = request.cookies.get('token', None)

    if auth:
        if auth.startswith("Basic "):
            auth = auth.split(" ")[1]

            try:
                decoded = base64.b64decode(auth)
            except:
                logger.warn('could not base64 decode auth header')
                abort(401, 'Unauthorized')

            s = decoded.split('gp:')

            if len(s) != 2:
                logger.warn('Invalid auth header format')
                abort(401, 'Unauthorized')

            try:
                token = decode(s[1])
            except Exception as e:
                logger.exception(e)
                abort(401, 'Unauthorized')

            return token
        elif auth.startswith("token ") or auth.startswith("bearer "):
            token = auth.split(" ")[1]

            try:
                token = decode(token.encode('utf8'))
            except Exception as e:
                logger.exception(e)
                abort(401, 'Unauthorized')

            return token
        else:
            logger.warn('Invalid auth header format')
            abort(401, 'Unauthorized')
    elif cookie:
        token = cookie
        try:
            token = decode(token.encode('utf8'))
        except Exception as e:
            logger.exception(e)
            abort(401, 'Unauthorized')

        return token
    else:
        logger.warn('No auth header')
        abort(401, 'Unauthorized')

try:
    #pylint: disable=ungrouped-imports,wrong-import-position
    from pygputils import dbpool
    logger.info('Using DB Pool')

    @app.before_request
    def before_request():
        g.db = dbpool.get()

        def release_db():
            db = getattr(g, 'db', None)
            if not db:
                return

            dbpool.put(db)
            g.db = None

        g.release_db = release_db

except:
    @app.before_request
    def before_request():
        g.db = DB(connect_db())

        def release_db():
            db = getattr(g, 'db', None)
            if not db:
                return

            db.close()
            g.db = None

        g.release_db = release_db

@app.teardown_request
def teardown_request(_):
    try:
        release_db = getattr(g, 'release_db', None)
        if release_db:
            release_db()
    except Exception as e:
        logger.error(_)
        logger.exception(e)


@app.errorhandler(404)
def not_found(error):
    msg = error.description

    if not msg:
        msg = 'Not Found'

    return jsonify({'message': msg, 'status': 404}), 404

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({'message': error.description, 'status': 401}), 401

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'message': error.description, 'status': 400}), 400

def OK(message, data=None):
    d = {'message': message, 'status': 200}

    if data:
        d['data'] = data

    return jsonify(d)

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        g.token = get_token()
        return f(*args, **kwargs)

    return decorated_function

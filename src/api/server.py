import os
from flask import request, abort, g, jsonify, Flask

import flask_socketio
import socketio

from pygputils import get_env, get_logger
from pygputils import db, gpflask

logger = get_logger('api')

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/ping')
def ping():

    result = g.db.execute_one('''SELECT * FROM gp''')[0]

    return jsonify({'status': result})


class ClientManager(socketio.base_manager.BaseManager):
    def __init__(self):
        super(ClientManager, self).__init__()
        self.__rooms = {}

    def enter_room(self, sid, namespace, room):
        super(ClientManager, self).enter_room(sid, namespace, room)
        logger.debug('%s joined room %s', sid, room)

        if room not in self.__rooms:
            self.__rooms[room] = 0

        self.__rooms[room] += 1

    def leave_room(self, sid, namespace, room):
        super(ClientManager, self).leave_room(sid, namespace, room)
        logger.debug('%s left room %s', sid, room)
        self.__rooms[room] -= 1

        if not self.__rooms[room]:
            del self.__rooms[room]

    def has_clients(self, room):
        clients = self.__rooms.get(room, None)

        if clients:
            return True

        return False


def main():  # pragma: no cover
    get_env('GP_SERVICE')
    get_env('GP_VERSION')
    get_env('GP_DATABASE_HOST')
    get_env('GP_DATABASE_USER')
    get_env('GP_DATABASE_PASSWORD')
    get_env('GP_DATABASE_PORT')
    get_env('GP_DATABASE_DB')

    client_manager = ClientManager()
    sio = flask_socketio.SocketIO(app,
                                  path='/api/v1/socket.io',
                                  async_mode='eventlet',
                                  client_manager=client_manager)

    port = int(os.environ.get('INFRABOX_PORT', 8080))
    logger.info('Starting Server on port %s', port)
    sio.run(app, host='0.0.0.0', port=port)

if __name__ == "__main__": # pragma: no cover
    try:
        main()
    except:
        print(stackdriver())
        sys.exit(1)
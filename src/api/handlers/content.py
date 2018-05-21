from flask import g, abort, request
from flask_restplus import Resource, fields

from pygputils import get_logger
from pygputils.gprestplus import api
from pygputils.gpflask import auth_required, OK

from api.namespaces import content as ns

logger = get_logger('content')

message_model = api.model('Message', {
    'id': fields.String(required=True),
    'sender': fields.String(required=True),
    'receiver': fields.String(required=True),
    'data': fields.String(required=True)
})

add_message_schema = {
    'type': "object",
    'properties': {
        'receiver_id': {'type': "string"},
        'data': {'type': 'string'}
    },
    'required': ["name", "type", "receiver_id"]
}

add_message_model = ns.schema_model('AddMessage', add_message_schema)


def get_headers(token_name, api_token):
    if token_name == 'api_token':
        headers = {
            "Authorization": "token " + api_token,
        }
    else:
        headers = {}

    return headers

@ns.route('/message/')
class Messages(Resource):
    @auth_required(['user'], check_connection=False)
    @api.marshal_list_with(message_model)
    def get(self):
        messages = g.db.execute_many_dict('''
            SELECT m.id, m.sender, m.receiver, m.data 
            FROM message m
            WHERE m.sender = %s
            ORDER BY m.created_at
        ''', [g.token['user']['id']])

        return messages

    @auth_required(['user'], check_connection=True)
    @api.expect(add_message_model)
    def post(self):
        user_id = g.token['user']['id']

        b = request.get_json()
        receiver = b['name']
        typ = b['type']
        data = b['data']

        message = g.db.execute_one_dict('''
                            INSERT INTO message (sender, receiver, data)
                            VALUES (%s, %s, %s) RETURNING id
                        ''', [user_id, receiver, data])
        message_id = message['id']

        g.db.commit()

        return OK('Message sended')


@ns.route('/message/<messaage_id>')
class MessageManagement(Resource):

    @auth_required(['user'])
    @api.marshal_with(message_model)
    def get(self, message_id):
        p = g.db.execute_one_dict('''
            SELECT m.id, m.sender, m.receiver, m.data 
            FROM message m
            WHERE m.sender = %s
            AND m.id = %s
            ORDER BY m.created_at
        ''', [g.token['user']['id'], message_id])
        return p

    @auth_required(['user'])
    def delete(self, message_id):
        p = g.db.execute_one_dict('''
                DELETE FROM message m
                WHERE m.id = %s
            ''', [message_id])
        return p


post_model = api.model('Post', {
        'id': fields.String(required=True),
        'headline': fields.String(required=True),
        'owner': fields.String(required=True),
        'data': fields.String(required=True)
    })

add_post_schema = {
    'type': "object",
    'properties': {
        'owner': {'type': "string"},
        'data': {'type': 'string'}
    },
    'required': ["headline", "owner"]
}

add_post_model = ns.schema_model('AddMessage', add_post_schema)

def get_headers(token_name, api_token):
    if token_name == 'api_token':
        headers = {
            "Authorization": "token " + api_token,
        }
    else:
        headers = {}

    return headers

@ns.route('/post/')
class Messages(Resource):
    @auth_required(['user'], check_connection=False)
    @api.marshal_list_with(post_model)
    def get(self):
        posts = g.db.execute_many_dict('''
            SELECT p.id, p.owner, p.headline, p.data 
            FROM post p
            WHERE p.owner = %s
            ORDER BY p.created_at
        ''', [g.token['user']['id']])

        return posts

    @auth_required(['user'], check_connection=True)
    @api.expect(add_post_model)
    def post(self):
        user_id = g.token['user']['id']

        b = request.get_json()
        headline = b['headline']
        data = b['data']

        post = g.db.execute_one_dict('''
                            INSERT INTO post (owner, headline, data)
                            VALUES (%s, %s, %s) RETURNING id
                        ''', [user_id, headline, data])
        post_id = post['id']

        g.db.commit()

        return OK('Message sended')

@ns.route('/post/<post_id>')
class MessageManagement(Resource):

    @auth_required(['user'])
    @api.marshal_with(post_model)
    def get(self, post_id):
        p = g.db.execute_one_dict('''
            SELECT p.id, p.sender, p.receiver, p.data 
            FROM post p
            WHERE p.sender = %s
            AND p.id = %s
            ORDER BY p.created_at
        ''', [g.token['user']['id'], post_id])
        return p

    @auth_required(['user'])
    def delete(self, post_id):
        p = g.db.execute_one_dict('''
                DELETE FROM post p
                WHERE p.id = %s
            ''', [post_id])
        return p



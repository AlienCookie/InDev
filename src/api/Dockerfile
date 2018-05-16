FROM alpine:3.6

RUN apk add --no-cache python openssl-dev openssl gcc py2-psycopg2 py2-requests musl-dev py2-pip libffi-dev py2-flask python2-dev && \
    pip install PyJWT jsonschema cryptography flask_restplus eventlet flask_socketio bcrypt && \
    apk del py2-pip python2-dev libffi-dev gcc musl-dev openssl-dev

ENV PYTHONPATH=/

COPY src/api /api
COPY src/pygputils /pygputils

# test rsa keys
COPY test/dummy_data/rsa_keys/id_rsa /var/run/secrets/test/rsa/id_rsa
COPY test/dummy_data/rsa_keys/id_rsa.pub /var/run/secrets/test/rsa/id_rsa.pub

CMD python /api/server.py
from pygputils.gprestplus import api

admin = api.namespace('api/v1/admin/',
                      description='Admin')

content = api.namespace('api/v1/content/',
                        description='Messages related operations')

settings = api.namespace('api/v1/settings/',
                         description='Settings')

user = api.namespace('api/v1/user/',
                     description='User')

account = api.namespace('api/v1/account/',
                        description='Account')

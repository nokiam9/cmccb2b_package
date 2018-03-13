# -*- coding: utf-8 -*-

MONGODB_SETTINGS = {'DB': 'CMCCB2B',
                    'host': 'localhost',  # 0.0.0.0 for local | mongo for docker
                    'port': 27017,
                    'connect': False    # set for pymongo bug fix
                    }
SECRET_KEY = "flask+mongoengine=<3"

# TESTING = True
# DEBUG_TB_INTERCEPT_REDIRECTS = False

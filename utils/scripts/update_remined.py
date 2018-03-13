# -*- coding: utf-8 -*-

# Define my utility file here
#

import pymongo
import json
import smtplib
import datetime
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

MONGO_DICT = {
    'host': 'localhost:27017',
    'dbname': 'CMCCB2B',
    'collection': 'Cmccb2bItem'
}

def apm_get_table(mongo):
        try:
            client = pymongo.MongoClient (mongo['host'])
            db = client[mongo['dbname']]
            client.admin.command('ismaster')
        except (ConnectionFailure, ServerSelectionTimeoutError) as msg:
            print("Connect Mongo server failed! mongo=%s, msg=%s." % (mongo, msg))
            return None
        else:
            print("Connect Mongo server successfully!")
            return db[mongo['collection']]


def apm_is_id_existed(table, notice_id):
    try:
        result = table.find_one({'id': notice_id})
    except Exception as msg:
        print("Mongo sql find_one() failed, msg=%s", msg)
    else:
        return result


def apm_list_unreminded(table):
    try:
        result = table.find({'reminded_time': {'$exists': False}})\
            .sort('published_date', pymongo.DESCENDING)
    except Exception as msg:
        print("Mongo sql find() failed, msg=%s", msg)
    else:
        return result


def apm_set_reminded(table, notice_id, now=datetime.datetime.utcnow()):
    """Changed!! """
    try:
        result = table.update_one({'id': notice_id}, {'$set' :{'reminded_time': now}})
    except Exception as msg:
        print("Mongo sql update_one() failed, msg=%s", msg)
    else:
        return result

if __name__ == '__main__' :
    print("Starting remined.py...")
    table = apm_get_table(MONGO_DICT)
    if not table:
        print('Connect mongo server failed, setting is %s' % MONGO_DICT) 
    else:
        id_list = []
        for rec in apm_list_unreminded(table):
            id_list.append(rec['id'])

        if id_list:
            now = datetime.datetime.utcnow()
            print("Prepare to update, id list=%s" % id_list)

            for notice_id in id_list:
               apm_set_reminded(table, notice_id, now)
            print("Update mongdb with remined_time successfully!!")
        else:
            print("No record need to update.")

 


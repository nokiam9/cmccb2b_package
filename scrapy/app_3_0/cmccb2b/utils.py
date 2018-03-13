# -*- coding: utf-8 -*-

# Define my utility file here
#

import pymongo
import json
import smtplib
import datetime
import logging
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from scrapy.exceptions import DropItem, NotConfigured

logger = logging.getLogger(__name__)


def apm_get_settings(crawler):
    mongo = dict(
        host=crawler.settings.get('AP_MONGO_HOST'),
        dbname=crawler.settings.get('AP_MONGO_DB'),
        collection=crawler.settings.get('AP_MONGO_COLLECTION')
    )
    if all(mongo.values()):
        return mongo
    else:
        return None


def apm_get_table(mongo):
        try:
            client = pymongo.MongoClient(mongo['host'])
            db = client[mongo['dbname']]
            client.admin.command('ismaster')
        except (ConnectionFailure, ServerSelectionTimeoutError) as msg:
            logger.error("Connect Mongo server failed! mongo=%s, msg=%s." % (mongo, msg))
            return None
        else:
            logger.info("Connect Mongo server successfully!")
            return db[mongo['collection']]


def apm_insert_item(table, item):
    rec = dict(item)
    rec['published_date'] = datetime.datetime.strptime(rec['published_date'], '%Y-%m-%d')
    rec['crawled_time'] = datetime.datetime.utcnow()
    try:
        result = table.insert_one(dict(rec))
    except Exception as msg:
        logger.error("Mongo sql insert_one() failed, msg is %s\n record=%s"
                     % (msg, json.dumps(dict(item), encoding='UTF-8', ensure_ascii=False)))
        return None
    else:
        return result


def apm_is_id_existed(table, notice_id):
    try:
        result = table.find_one({'id': notice_id})
    except Exception as msg:
        logger.error("Mongo sql find_one() failed, msg=%s", msg)
    else:
        return result


def apm_list_unreminded(table):
    try:
        result = table.find({'reminded_time': {'$exists': False}})\
            .sort('published_date', pymongo.DESCENDING)
    except Exception as msg:
        logger.error("Mongo sql find() failed, msg=%s", msg)
    else:
        return result


def apm_set_reminded(notice_id):
    try:
        result = table.update_one({'id': notice_id}, {'reminded_time': datetime.datetime.utcnow()})
    except Exception as msg:
        logger.error("Mongo sql update_one() failed, msg=%s", msg)
    else:
        return result




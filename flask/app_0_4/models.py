# -*- coding: utf-8 -*-

from flask_mongoengine import MongoEngine

db = MongoEngine()  # 初始化数据库连接db


class Todo (db.Document):
    meta = {
        'collection': 'Cmccb2bItem'     # set collection name here!
    }
    _id = db.StringField()  # 必须增加，不然打开已存在的table时会报错
    id = db.StringField()
    title = db.StringField()
    published_date = db.DateTimeField()
    notice_typ = db.StringField()
    notice_url = db.StringField()
    crawled_time = db.DateTimeField()
    notice_type = db.StringField()
    source_ch = db.StringField()
    reminded_time = db.DateTimeField()
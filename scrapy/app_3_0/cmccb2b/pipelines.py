# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from scrapy.exceptions import NotConfigured
from cmccb2b.utils import apm_get_settings, apm_get_table, apm_insert_item, apm_is_id_existed

import logging

logger = logging.getLogger(__name__)
MAX_DUPLICATE_RECORDS = 20


class Cmccb2bPipeline(object):
    def __init__(self, mongo, full_mode=False):
        self.mongo = mongo
        self.full_mode = full_mode
        self.table = None
        self.dup_count = 0

    @classmethod
    def from_crawler(cls, crawler):
        mongo = apm_get_settings(crawler)
        full_mode = crawler.settings.getbool('AP_CRAWLER_IGNORE_DUPLICATE_RECORD')
        return cls(mongo, full_mode)

    def open_spider(self, spider):
        self.table = apm_get_table(self.mongo)
        if not self.table:
            logger.error('Mongo server failed! mongo=%s' % self.mongo)

    def close_spider(self, spider):
        logger.warning("Spider will be closed, current_page=%i." % spider.current_page)
        # if self.table:
        #     self.table.logout()

    def process_item(self, item, spider):
        # unique key is id, if not exist insert it, else update value of this id
        if apm_is_id_existed(self.table, item['id']):
            logger.warning("Duplicated record ! id=%s.\n dict=%s" %
                           (item['id'], json.dumps(dict(item), encoding='UTF-8', ensure_ascii=False)))
            self.dup_count += 1
        else:
            if apm_insert_item(self.table, item):
                logger.debug("Insert record ok. id=%s." % item['id'])
            self.dup_count = 0

        # when find too many duplicated records, it means web site isn't updated, then stop spider
        if (not self.full_mode) and (self.dup_count >= MAX_DUPLICATE_RECORDS):
            logger.error("Too many duplicate records, dup_count is %i." % self.dup_count)
            spider.require_close = "max_duplicate_records"
        return item


# -*- coding: utf-8 -*-

# Define my extension file here
#

from scrapy import signals
from scrapy.exceptions import NotConfigured

import smtplib
from email.mime.text import MIMEText
from email.header import Header

from cmccb2b.utils import apm_get_settings, apm_get_table, apm_list_unreminded, apm_set_reminded

import logging
logger = logging.getLogger(__name__)


class MailAlert(object):
    def __init__(self, mailer, mongo):
        self.mailer = mailer
        self.mongo = mongo

    @classmethod
    def from_crawler(cls, crawler):
        # first check if the extension should be enabled and raise\
        # NotConfigured otherwise
        if not crawler.settings.getbool('MAILALERT_ENABLED'):
            raise NotConfigured

        # get mail and mongo items from settings
        mailer = dict(
            to_list=crawler.settings.get('AP_MAIL_TO_LIST'),
            host=crawler.settings.get('AP_MAIL_HOST'),
            user=crawler.settings.get('AP_MAIL_USER'),
            passwd=crawler.settings.get('AP_MAIL_PASSWD'),
            postfix=crawler.settings.get('AP_MAIL_POSTFIX')
        )

        mongo = apm_get_settings(crawler)

        if not (all(mailer.values()) and all(mongo.values())):
            raise NotConfigured

        # Notice: construct ext, include process connected with signals
        ext = cls(mailer, mongo)

        # connect the extension object to signals
        # crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        # crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)

        # return the extension object
        return ext

    # def spider_opened(self, spider):
    #     logger.info("In MyExtentions: opened spider %s" % spider.name)

    def spider_closed(self, spider):
        logger.info('In MyExtentions: closed spider %s' % spider.name)
        logger.info('In MyExtentions: Start send alert mail, return code=%i' % self.send_mail(self.mailer))

    # def item_scraped(self, item, spider):
    #     logger.info("In MyExtentions: item scraped spider %s" % spider.name)

    def send_mail(self, mailer):
        content = self._create_mail_content(self.mongo)
        if not content:
            return None

        me = "scrapy" + "<" + mailer['user'] + "@" + mailer['postfix'] + ">"
        sub = u'来自alex_scrapy的extentions的消息'.encode('utf-8')
        msg = MIMEText(content, _subtype='plain', _charset='utf-8')
        msg['Subject'] = sub
        msg['From'] = me
        msg['To'] = ";".join(mailer['to_list'])

        try:
            # server = smtplib.SMTP()
            server = smtplib.SMTP_SSL(mailer['host'], 465)
            server.connect(mailer['host'])
            server.login(mailer['user'], mailer['passwd'])
            server.sendmail(me, mailer['to_list'], msg.as_string())
            server.close()
        except Exception, e:
            logger.error('Send mail failed, msg=%s' % e)
            return None
        else:
            logger.info('Send mail successfully!')
            return 0

    def _create_mail_content(self, mongo):
        content = ''
        id_list = []

        table = apm_get_table(mongo)
        for i, rec in enumerate(apm_list_unreminded(table)):
            content += ('%4i: %s, %s, %s\n'
                        % (i, rec['published_date'].strftime('%Y-%m-%d'), rec['source_ch'], rec['title']))
            id_list.append(rec['id'])

        # next add code for apm_set_reminded
        return content


# -*- coding: utf-8 -*-

# Scrapy settings for CMCCB2B project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'cmccb2b'

SPIDER_MODULES = ['cmccb2b.spiders']
NEWSPIDER_MODULE = 'cmccb2b.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'CMCCB2B (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'CMCCB2B.middlewares.Cmccb2BSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'CMCCB2B.middlewares.Cmccb2BDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
EXTENSIONS = {
    # 'scrapy.extensions.telnet.TelnetConsole': None,
    'cmccb2b.extensions.MailAlert': 100
}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'cmccb2b.pipelines.Cmccb2bPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
MAILALERT_ENABLED = False

# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# ----------------------------------------
# ALEX PROJECT SETTING
# ----------------------------------------
# AP_MONGO_HOST = os.environ['MONGO_PORT_27017_TCP_ADDR'] +':' + os.environ['MONGO_PORT_27017_TCP_PORT']
AP_MONGO_HOST = "mongo:27017"                   # 本机测试 0.0.0.0 ，docker中为mongo
AP_MONGO_DB = "cmccb2b"
AP_MONGO_COLLECTION = "Cmccb2bItem"

AP_MAIL_TO_LIST = ['18809314002@139.com'] 	    # 收件人(列表)
AP_MAIL_HOST = 'smtp.139.com'		    	    # 使用的邮箱的smtp服务器地址，这里是163的smtp地址
AP_MAIL_USER = '13901214002'		       	    # 发件人的用户名
AP_MAIL_PASSWD = 'eos5d3'			            # 密码
AP_MAIL_POSTFIX = '139.com'		    	        # 邮箱的后缀，网易就是163.com

# AP_CRAWLER_IGNORE_DUPLICATE_RECORD = True 	# if false or unset, close spider when find too many duplicate records
# ----------------------------------------


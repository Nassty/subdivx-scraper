# Scrapy settings for subdivx project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'subdivx'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['subdivx.spiders']
NEWSPIDER_MODULE = 'subdivx.spiders'
DEFAULT_ITEM_CLASS = 'subdivx.items.SubdivxItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)


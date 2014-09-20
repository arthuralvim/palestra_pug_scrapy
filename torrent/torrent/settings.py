# -*- coding: utf-8 -*-

BOT_NAME = 'torrent'

SPIDER_MODULES = ['torrent.spiders']
NEWSPIDER_MODULE = 'torrent.spiders'

from unipath import Path
SPIDER_DOWNLOAD_DIR = Path(__file__).absolute().ancestor(1)

LOG_FILE = u'torrent.log'

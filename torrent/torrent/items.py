# -*- coding: utf-8 -*-

from scrapy import Field
from scrapy import Item


class TorrentItem(Item):
    name = Field()
    url = Field()
    size = Field()
    number_files = Field()
    age = Field()
    seed = Field()
    leech = Field()
    magnet = Field()
    file = Field()

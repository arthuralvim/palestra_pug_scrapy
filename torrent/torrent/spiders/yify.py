# -*- coding: utf-8 -*-

from scrapy import Spider
from torrent.items import TorrentItem
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.utils.project import get_project_settings as Settings
from unipath import Path
from os.path import exists
from os import makedirs
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
import HTMLParser

settings = Settings()
BASE_DIR = settings['SPIDER_DOWNLOAD_DIR']

def response_to_file(name, response):
    with open(name, 'wb') as f:
        f.write(response.body)


class YifySpider(Spider):
    name = 'yify'
    allowed_domains = ['kickass.to', 'torcache.net']

    # start_urls = (
    #     'http://kickass.to/usearch/yify/',
    # )

    start_urls = ['http://kickass.to/usearch/yify/{0}/'.format(page)
        for page in xrange(1, 215)]

    # rules = (Rule(SgmlLinkExtractor(allow=('\\?page=\\d')),'parse_start_url',follow=True),)

    def parse(self, response):
        hxs = Selector(response)
        trs = hxs.xpath('//table[@class="data"]/tr')

        tor_files = []
        for tr in trs[1:]:
            tor = TorrentItem()
            tor['name'] = tr.xpath('.//a[@class="cellMainLink"]/text()').extract()[0][:-3]
            tor['url'] = tr.xpath('.//a[@class="cellMainLink"]/@href').extract()[0]
            tor['size'] = tr.xpath('.//td//text()').extract()[-6] + tr.xpath('.//td//text()').extract()[-5]
            tor['number_files'] = tr.xpath('.//td//text()').extract()[-4]
            tor['age'] = tr.xpath('.//td//text()').extract()[-3]
            tor['seed'] = tr.xpath('.//td//text()').extract()[-2]
            tor['leech'] = tr.xpath('.//td//text()').extract()[-1]
            tor['magnet'] = tr.xpath('.//a[contains(@class, "imagnet")]/@href').extract()[0]
            url = tr.xpath('.//a[contains(@class, "idownload")]/@href').extract()[1]
            tor['file'] = url
            tor_files.append(url)
            yield tor

        for url in tor_files:
            yield Request(url, callback=self.save_torrent)

    def save_torrent(self, response):
        filename = (response.url).split('/')[-1]
        filename = filename.replace('%5B', '[')
        filename = filename.replace('%5D', ']')
        directory = Path(BASE_DIR, ('output'))
        if not exists(directory):
            makedirs(directory)
        path = Path(directory, filename)
        with open(path, "wb") as f:
            f.write(response.body)

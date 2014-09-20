# -*- coding: utf-8 -*-

from scrapy.contrib.spiders.init import InitSpider
from scrapy.http import Request
from scrapy.selector import Selector
from decouple import config
import re
import json
import requests
from urlparse import urljoin
from scrapy.utils.project import get_project_settings as Settings


STGS = Settings()

CITY_FROM = 'REC'
CITY_TO = 'RIO'
NUMBER_ADULTS = 2
DATE_GO = '2014-09-20'
DATE_BACK = '2014-09-25'


class JSCallError(Exception):

    def __init__(self, message):
        super(JSCallError, self).__init__(message)
        self.message = u'Erro na chamada da função.'

def response_to_file(name, response):
    with open(name, 'wb') as f:
        f.write(response.body)


class DecolarSpider(InitSpider):
    name = "decolar"
    allowed_domains = ["decolar.com.br"]
    start_urls = [
        'http://www.decolar.com/shop/flights/results/roundtrip/REC/RIO/2014-09-20/2014-09-25/1/0/0',
    ]

    def init_request(self):
        city1 = CITY_FROM
        city2 = CITY_TO
        date_go = DATE_GO
        date_back = DATE_BACK
        number_adults = NUMBER_ADULTS

        u = 'http://www.decolar.com/shop/flights/results/roundtrip/{0}' \
               '/{1}/{2}/{3}/{4}/0/0'.format(city1, city2, date_go, date_back,
                                             number_adults, )

        return Request(url=u, callback=self.get_url, meta={'referer': u, })

    def get_url(self, response):

        hxs = Selector(response)
        scripts = hxs.xpath('//script[contains(text(), "search :")]')
        url_code_line = scripts[0].extract().split('\n')[3]
        url_part = re.findall(r"'(.*?)'", url_code_line)[0]
        nurl = urljoin(self.start_urls[0], url_part)
        referer = response.meta['referer']
        import ipdb; ipdb.set_trace()

        headers = {
            'User-Agent': STGS['USER_AGENT'],
            "Content-Type": "application/json",
            'X-Requested-With': 'XMLHttpRequest',
            "Referer": referer,
        }

        try:
            post = requests.get(nurl, headers=headers)
        except JSCallError, e:
            raise e

        consegui = post.json()



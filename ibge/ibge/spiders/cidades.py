# -*- coding: utf-8 -*-

from ibge.items import CityItemDjango
from decouple import config
from scrapy.contrib.spiders.init import InitSpider
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.utils.project import get_project_settings as Settings
import datetime
import requests
from urlparse import urljoin


def response_to_file(name, response):
    with open(name, 'wb') as f:
        f.write(response.body)


class CidadesSpider(InitSpider):
    name = "cidades"
    allowed_domains = ["cidades.ibge.gov.br"]
    start_urls = (
        'http://www.cidades.ibge.gov.br/xtras/home.php',
    )


    def init_request(self):
        return Request(url=self.start_urls[0], callback=self.states)

    def states(self, response):
        # response_to_file('output/main.html', response)
        hxs = Selector(response)
        menu = hxs.xpath('//ul[@id="menu_ufs"]/li/a/@href')
        states = hxs.xpath('//ul[@id="menu_ufs"]/li/a/text()')
        reqs = []
        for m, s in zip(menu, states):
            nurl = urljoin(self.start_urls[0], m.extract())
            nreq = Request(url=nurl,  callback=self.parse,
                           meta={'state': s.extract()})
            reqs.append(nreq)
        for r in reqs:
            yield r

    def parse(self, response):
        # response_to_file('output/state.html', response)
        hxs = Selector(response)
        cities = hxs.xpath('//ul[@id="lista_municipios"]/li/a/text()')
        state = response.meta['state']
        for cid in cities:
            ci = CityItemDjango()
            ci['name'] = cid.extract()
            ci['state'] = state
            ci.save()
            yield ci

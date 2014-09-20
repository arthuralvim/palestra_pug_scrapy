# -*- coding: utf-8 -*-

from scrapy import Item
from scrapy import Field
from core.models import City
from scrapy.contrib.djangoitem import DjangoItem


class CityItem(Item):
    name = Field()
    state = Field()


class CityItemDjango(DjangoItem):
    django_model = City

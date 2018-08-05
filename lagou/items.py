# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class LagouItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection = 'lagou_jobs'
    url = Field()
    company = Field()
    job_name = Field()
    job_request = Field()
    advantage = Field()
    describe = Field()
    location = Field()

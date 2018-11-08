# -*- coding: utf-8 -*-
import scrapy


class NewsItem(scrapy.Item):
    title = scrapy.Field()
    article_url = scrapy.Field()
    tag = scrapy.Field()
    summary = scrapy.Field()
    paragraphs = scrapy.Field()

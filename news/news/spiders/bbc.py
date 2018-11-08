# -*- coding: utf-8 -*-
import re
import requests
import scrapy
from bs4 import BeautifulSoup
from datetime import datetime
from requests.exceptions import ConnectionError

from news.logger import get_logger
from news.items import NewsItem


class BbcSpider(scrapy.Spider):
    name = 'bbc'
    allowed_domains = ['www.bbc.com']
    start_urls = ['https://www.bbc.com/']
    logger = get_logger(name, name+'.log')

    def parse(self, response):
        media_contents = self._extract_text_by_css(response, '.media__content')
        titles = self._extract_text_by_css(response, '.media__link::text')
        article_urls = self._get_article_urls(response)
        tags = self._extract_text_by_css(response, '.media__tag::text')
        summaries = self._get_summaries(media_contents)

        for idx, title in enumerate(titles):
            item = NewsItem()
            paragraphs = self._get_paragraphs(article_urls[idx])
            try:
                item['title'] = title
                item['article_url'] = article_urls[idx]
                item['tag'] = tags[idx]
                item['summary'] = summaries[idx]
                item['paragraphs'] = paragraphs
                item['scraped_date'] = datetime.now().strftime("%Y-%m-%d")
            except IndexError as e:
                logger.error(e+'The html structure might have been changed')

            yield item

    def _get_paragraphs(self, article_url):
        superfluous_elements = [
            'Share this with', 'Email', 'Facebook', 'Messenger',
            'Messenger', 'Twitter', 'Pinterest', 'WhatsApp', 'LinkedIn',
            'Copy this link', '\n',
            'These are external links and will open in a new window',
            'The BBC is not responsible for the content of external Internet sites']
        text_content = []
        try:
            page = requests.get(article_url)
            soup = BeautifulSoup(page.content, "html.parser")
            paragraphs = soup.find_all("p")
            for paragraph in paragraphs:
                text = paragraph.text.strip()
                if text and text not in superfluous_elements:
                    text_content.append(text)
        except ConnectionError as e:
            logger.error(e)
        return text_content

    def _get_article_urls(self, response):
        domain = response.url.replace(
            'http://', '').replace('https://', '').replace('.com/', '.co')
        scraped_urls = [raw_data.strip() for raw_data in response.css(
            '.media__link::attr(href)').extract()]
        for idx, article_url in enumerate(scraped_urls):
            if domain not in article_url:
                scraped_urls[idx] = response.url[:-1] + article_url
        return scraped_urls

    def _get_summaries(self, media_contents):
        return self._extract_text_by_html(
            media_contents, '<p class="media__summary">\n(.*)</p>')

    def _extract_text_by_html(self, media_contents, target):
        arr = []
        for media_content in media_contents:
            raw_data = re.search(target, media_content)
            arr.append(raw_data.group(1).strip() if raw_data else None)
        return arr

    def _extract_text_by_css(self, response, target):
        return [raw_data.strip()for raw_data in response.css(target).extract()]

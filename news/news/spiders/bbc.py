# -*- coding: utf-8 -*-
import re
import requests
import scrapy
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError


class BbcSpider(scrapy.Spider):
    name = 'bbc'
    allowed_domains = ['www.bbc.com']
    start_urls = ['http://www.bbc.com/']

    def parse(self, response):
        media_contents = self._extract_text_by_css(response, '.media__content')
        titles = self._extract_text_by_css(response, '.media__link::text')
        article_urls = self._get_article_urls(response)
        tags = self._extract_text_by_css(response, '.media__tag::text')
        summaries = self._get_summaries(media_contents)

        for idx, title in enumerate(titles):
            scraped_info = {}
            paragraphs = self._get_paragraphs(article_urls[idx])
            try:
                scraped_info['title'] = title
                scraped_info['article_url'] = article_urls[idx]
                scraped_info['tag'] = tags[idx]
                scraped_info['summary'] = summaries[idx]
                scraped_info['paragraphs'] = paragraphs
            except IndexError as e:
                # TODO the print func below should be replaced with a logger
                print(e, 'The html structure might have been changed')

            yield scraped_info

    def _get_paragraphs(self, article_url):
        superfluous_elements = [
                '', 'Share this with', 'Email', 'Facebook', 'Messenger',
                'Messenger', 'Twitter', 'Pinterest', 'WhatsApp', 'LinkedIn',
                'Copy this link',
                'These are external links and will open in a new window']
        text_content = []
        try:
            page = requests.get(article_url)
            soup = BeautifulSoup(page.content, "html.parser")
            paragraphs = soup.find_all("p")
            for paragraph in paragraphs:
                if paragraph.text not in superfluous_elements:
                    text_content.append(paragraph.text)
        except ConnectionError as e:
            # TODO the print func below should be replaced with a logger
            print(e)
        return text_content

    def _get_article_urls(self, response):
        base_url = response.url
        scraped_urls = [raw_data.strip() for raw_data in response.css(
            '.media__link::attr(href)').extract()]
        for idx, article_url in enumerate(scraped_urls):
            if not article_url.startswith(base_url):
                scraped_urls[idx] = base_url + article_url
        return scraped_urls

    def _get_summaries(self, media_contents):
        return self._extract_text_by_html(
            media_contents, '<p class="media__summary">\n(.*)</p>')

    def _extract_text_by_html(self, media_contents, target):
        arr = []
        for media_content in media_contents:
            raw_data = re.search(target, media_content)
            if raw_data:
                arr.append(raw_data.group(1).strip())
            else:
                arr.append(None)
        return arr

    def _extract_text_by_css(self, response, target):
        return [raw_data.strip()for raw_data in response.css(target).extract()]

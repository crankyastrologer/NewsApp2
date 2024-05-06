import scrapy
from newspaper import Article
import os
from urllib.parse import urlparse

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['https://hindustantimes.com/']  # Replace with your website's URL
    allowed_domains = ['hindustantimes.com']  # Replace with your website's domain
    custom_settings = {
        'DEPTH_LIMIT': 5  # Change this to the maximum depth you want to allow
    }

    def parse(self, response):
        article = Article(response.url)
        article.download()
        article.parse()

        # Create a directory structure that mirrors the structure of the website
        path = 'scraped_data' + urlparse(response.url).path
        if not os.path.exists(path):
            os.makedirs(path)

        filename = 'index.txt'
        with open(os.path.join(path, filename), 'w', encoding='utf-8') as f:
            f.write(f'Title: {article.title}\n')
            f.write(f'Authors: {", ".join(article.authors)}\n')
            f.write(f'Publish Date: {article.publish_date}\n')
            f.write(f'Top Image: {article.top_image}\n\n')
            f.write(f'Text: {article.text}')

        for href in response.css('a::attr(href)').getall():
            if href.startswith('http') or href.startswith('www'):
                yield response.follow(href, self.parse)

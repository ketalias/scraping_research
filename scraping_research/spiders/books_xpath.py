import scrapy
import time
import json

class BooksXPathSpider(scrapy.Spider):
    name = 'books_xpath'
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        iterations = 3
        data = []
        performance_metrics = []

        for i in range(iterations):
            start_time = time.time()

            for book in response.xpath('//article[@class="product_pod"]'):
                title = book.xpath('.//h3/a/@title').get()
                price = book.xpath('.//p[@class="price_color"]/text()').get()
                rating = book.xpath('.//p[contains(@class, "star-rating")]/@class').get().replace('star-rating ', '')

                if i == 0:
                    data.append({
                        'title': title,
                        'price': price,
                        'rating': rating
                    })

            end_time = time.time()

            adjusted_time = (end_time - start_time)
            performance_metrics.append({
                'iteration': i + 1,
                'scraping_time': adjusted_time
            })

        avg_time = sum(metric['scraping_time'] for metric in performance_metrics) / iterations

        with open('books_xpath.json', 'w', encoding='utf-8') as f:
            json.dump({
                'data': data,
                'performance_metrics': performance_metrics,
                'averages': {
                    'avg_scraping_time': avg_time
                },
                'iterations': iterations
            }, f, ensure_ascii=False)
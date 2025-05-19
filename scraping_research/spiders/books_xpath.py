import scrapy
import time
import json
import statistics

class BooksXPathSpider(scrapy.Spider):
    name = 'books_xpath'
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        iterations = 100  # Збільшено для точності
        data = []
        performance_metrics = []

        for i in range(iterations):
            start_time = time.perf_counter()  # Початок заміру (включає ініціалізацію)
            books = response.xpath('//article[@class="product_pod"]')  # Ініціалізація селекторів
            for book in books:
                title = book.xpath('.//h3/a/@title').get()
                price = book.xpath('.//p[@class="price_color"]/text()').get()
                rating = book.xpath('.//p[contains(@class, "star-rating")]/@class').get().replace('star-rating ', '')
                if i == 0:  # Збирати дані тільки для першої ітерації
                    data.append({
                        'title': title,
                        'price': price,
                        'rating': rating
                    })
            end_time = time.perf_counter()  # Кінець заміру
            adjusted_time = end_time - start_time
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
                    'avg_scraping_time': avg_time,
                },
                'iterations': iterations
            }, f, ensure_ascii=False, indent=2)
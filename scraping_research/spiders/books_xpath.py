import scrapy
import time
import json
import psutil

class BooksXPathSpider(scrapy.Spider):
    name = 'books_xpath'
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        iterations = 10
        times = []
        cpu_usages = []
        memory_usages = []
        data = []
        sleep_duration = 1

        for _ in range(iterations):
            start_time = time.time()
            process = psutil.Process()
            time.sleep(sleep_duration)
            cpu_start = process.cpu_percent(interval=None)

            for book in response.xpath('//article[@class="product_pod"]'):
                title = book.xpath('.//h3/a/@title').get()
                price = book.xpath('.//p[@class="price_color"]/text()').get()
                rating = book.xpath('.//p[contains(@class, "star-rating")]/@class').get().replace('star-rating ', '')

                if _ == 0:
                    data.append({
                        'title': title,
                        'price': price,
                        'rating': rating
                    })

            end_time = time.time()
            cpu_end = process.cpu_percent(interval=None)
            memory = process.memory_info().rss / 1024 / 1024

            adjusted_time = (end_time - start_time) - sleep_duration
            times.append(adjusted_time)
            cpu_usages.append((cpu_start + cpu_end) / 2)
            memory_usages.append(memory)

        avg_time = sum(times) / iterations
        avg_cpu = sum(cpu_usages) / iterations
        avg_memory = sum(memory_usages) / iterations

        with open('books_xpath.json', 'w', encoding='utf-8') as f:
            json.dump({
                'data': data,
                'avg_scraping_time': avg_time,
                'avg_cpu_usage_percent': avg_cpu,
                'avg_memory_usage_mb': avg_memory,
                'iterations': iterations
            }, f, ensure_ascii=False)
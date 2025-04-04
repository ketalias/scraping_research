import scrapy
import time
import json
import psutil

class BooksCSSSpider(scrapy.Spider):
    name = 'books_css'
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        iterations = 3
        data = []
        sleep_duration = 1
        performance_metrics = []
        process = psutil.Process()

        for i in range(iterations):
            start_time = time.time()
            cpu_start = process.cpu_percent(interval=0.1)

            for book in response.css('article.product_pod'):
                title = book.css('h3 a::attr(title)').get()
                price = book.css('p.price_color::text').get()
                rating = book.css('p.star-rating::attr(class)').get().replace('star-rating ', '')

                if i == 0:
                    data.append({
                        'title': title,
                        'price': price,
                        'rating': rating
                    })

            end_time = time.time()
            cpu_end = process.cpu_percent(interval=0.1)
            memory = process.memory_info().rss / 1024 / 1024

            adjusted_time = (end_time - start_time)
            performance_metrics.append({
                'iteration': i + 1,
                'scraping_time': adjusted_time,
                'cpu_usage_percent': max((cpu_start + cpu_end) / 2, 0.1),
                'memory_usage_mb': memory
            })

            time.sleep(sleep_duration)

        # Calculate averages
        avg_time = sum(metric['scraping_time'] for metric in performance_metrics) / iterations
        avg_cpu = sum(metric['cpu_usage_percent'] for metric in performance_metrics) / iterations
        avg_memory = sum(metric['memory_usage_mb'] for metric in performance_metrics) / iterations

        with open('books_css.json', 'w', encoding='utf-8') as f:
            json.dump({
                'data': data,
                'performance_metrics': performance_metrics,
                'averages': {
                    'avg_scraping_time': avg_time,
                    'avg_cpu_usage_percent': avg_cpu,
                    'avg_memory_usage_mb': avg_memory
                },
                'iterations': iterations
            }, f, ensure_ascii=False)
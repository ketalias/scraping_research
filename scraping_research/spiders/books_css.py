import scrapy
import time
import json

class BooksCSSSpider(scrapy.Spider):
    name = 'books_css'
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        iterations = 100  # Збільшено для точності
        data = []
        performance_metrics = []

        for i in range(iterations):
            start_time = time.perf_counter()  # Початок заміру (включає ініціалізацію)
            books = response.css('article.product_pod')  # Ініціалізація селекторів
            for book in books:
                title = book.css('h3 a::attr(title)').get()
                price = book.css('p.price_color::text').get()
                rating = book.css('p.star-rating::attr(class)').get().replace('star-rating ', '')
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

        with open('books_css.json', 'w', encoding='utf-8') as f:
            json.dump({
                'data': data,
                'performance_metrics': performance_metrics,
                'averages': {'avg_scraping_time': avg_time},
                'iterations': iterations
            }, f, ensure_ascii=False, indent=2)

import scrapy
import time
import json
from bs4 import BeautifulSoup

class BooksBS4Spider(scrapy.Spider):
    name = 'books_bs4'
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        iterations = 3
        data = []
        performance_metrics = []

        soup = BeautifulSoup(response.text, 'html.parser')

        for i in range(iterations):
            start_time = time.time()

            for book in soup.find_all('article', class_='product_pod'):
                title = book.find('h3').find('a')['title']
                price = book.find('p', class_='price_color').get_text()
                rating = book.find('p', class_='star-rating')['class'][1]

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

        with open('books_bs4.json', 'w', encoding='utf-8') as f:
            json.dump({
                'data': data,
                'performance_metrics': performance_metrics,
                'averages': {
                    'avg_scraping_time': avg_time
                },
                'iterations': iterations
            }, f, ensure_ascii=False)
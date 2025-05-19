import scrapy
import time
import json

class HNXPathSpider(scrapy.Spider):
    name = 'hn_xpath'
    start_urls = ['https://news.ycombinator.com/']

    def parse(self, response):
        iterations = 100  # Як у scrape_books_bs4 і HNCSSSpider
        data = []
        performance_metrics = []

        for i in range(iterations):
            start_time = time.perf_counter()  # Початок заміру (включає ініціалізацію)
            items = response.xpath('//tr[contains(@class, "athing")]')  # Ініціалізація селекторів
            for item in items:
                title = item.xpath('.//span[@class="titleline"]/a/text()').get()
                url = item.xpath('.//span[@class="titleline"]/a/@href').get()
                subtext = item.xpath('./following-sibling::tr[1]/td[@class="subtext"]/span[@class="subline"]')
                score = subtext.xpath('.//span[@class="score"]/text()').get()
                author = subtext.xpath('.//a[@class="hnuser"]/text()').get()
                comments = subtext.xpath('.//a[last()]/text()').get()
                if i == 0:  # Збирати дані тільки для першої ітерації
                    data.append({
                        'title': title,
                        'url': url,
                        'score': score,
                        'author': author,
                        'comments': comments
                    })
            end_time = time.perf_counter()  # Кінець заміру
            adjusted_time = end_time - start_time
            performance_metrics.append({
                'iteration': i + 1,
                'scraping_time': adjusted_time
            })

        avg_time = sum(metric['scraping_time'] for metric in performance_metrics) / iterations

        with open('hn_xpath.json', 'w', encoding='utf-8') as f:
            json.dump({
                'data': data,
                'performance_metrics': performance_metrics,
                'averages': {'avg_scraping_time': avg_time},
                'iterations': iterations
            }, f, ensure_ascii=False, indent=2)
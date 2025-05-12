import scrapy
import time
import json

class HNCSSSpider(scrapy.Spider):
    name = 'hn_css'
    start_urls = ['https://news.ycombinator.com/']

    def parse(self, response):
        iterations = 3
        data = []
        performance_metrics = []

        for i in range(iterations):
            start_time = time.time()

            items = response.css('tr.athing')
            subtext_rows = response.css('td.subtext span.subline')
            
            for index, item in enumerate(items):
                title = item.css('span.titleline a::text').get()
                url = item.css('span.titleline a::attr(href)').get()
                if index >= len(subtext_rows):
                    continue
                subtext = subtext_rows[index]
                score = subtext.css('span.score::text').get()
                author = subtext.css('a.hnuser::text').get()
                comments = subtext.css('a:last-child::text').get()

                if i == 0:
                    data.append({
                        'title': title,
                        'url': url,
                        'score': score,
                        'author': author,
                        'comments': comments
                    })

            end_time = time.time()

            adjusted_time = (end_time - start_time)
            performance_metrics.append({
                'iteration': i + 1,
                'scraping_time': adjusted_time
            })

        avg_time = sum(metric['scraping_time'] for metric in performance_metrics) / iterations

        with open('hn_css.json', 'w', encoding='utf-8') as f:
            json.dump({
                'data': data,
                'performance_metrics': performance_metrics,
                'averages': {
                    'avg_scraping_time': avg_time
                },
                'iterations': iterations
            }, f, ensure_ascii=False)
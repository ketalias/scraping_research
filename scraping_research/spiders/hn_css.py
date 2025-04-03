import scrapy
import time
import json
import psutil

class HNCSSSpider(scrapy.Spider):
    name = 'hn_css'
    start_urls = ['https://news.ycombinator.com/']

    def parse(self, response):
        iterations = 3
        data = []
        sleep_duration = 0.1 
        performance_metrics = []
        process = psutil.Process()

        for i in range(iterations):
            start_time = time.time()
            cpu_start = process.cpu_percent(interval=0.1)

            for item in response.css('tr.athing'):
                title = item.css('span.titleline a::text').get()
                url = item.css('span.titleline a::attr(href)').get()
                subtext = item.xpath('./following-sibling::tr[1]/td[@class="subtext"]').css('span.subline')
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

        with open('hn_css.json', 'w', encoding='utf-8') as f:
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
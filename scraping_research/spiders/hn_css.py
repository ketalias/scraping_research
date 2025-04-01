import scrapy
import time
import json
import psutil

class HNCSSSpider(scrapy.Spider):
    name = 'hn_css'
    start_urls = ['https://news.ycombinator.com/']

    def parse(self, response):
        iterations = 10
        times = []
        cpu_usages = []
        memory_usages = []
        data = []
        sleep_duration = 0.1 

        for _ in range(iterations):
            start_time = time.time()
            process = psutil.Process()
            time.sleep(sleep_duration) 
            cpu_start = process.cpu_percent(interval=None)

            for item in response.css('tr.athing'):
                title = item.css('span.titleline a::text').get()
                url = item.css('span.titleline a::attr(href)').get()
                subtext = item.xpath('./following-sibling::tr[1]/td[@class="subtext"]').css('span.subline')
                score = subtext.css('span.score::text').get()
                author = subtext.css('a.hnuser::text').get()
                comments = subtext.css('a:last-child::text').get()

                if _ == 0:  # Збираємо дані лише в першій ітерації
                    data.append({
                        'title': title,
                        'url': url,
                        'score': score,
                        'author': author,
                        'comments': comments
                    })

            end_time = time.time()
            cpu_end = process.cpu_percent(interval=None)
            memory = process.memory_info().rss / 1024 / 1024  

            # Віднімаємо sleep_duration від часу скрапінгу
            adjusted_time = (end_time - start_time) - sleep_duration
            times.append(adjusted_time)
            cpu_usages.append((cpu_start + cpu_end) / 2)
            memory_usages.append(memory)

        avg_time = sum(times) / iterations
        avg_cpu = sum(cpu_usages) / iterations
        avg_memory = sum(memory_usages) / iterations

        with open('hn_css.json', 'w', encoding='utf-8') as f:
            json.dump({
                'data': data,
                'avg_scraping_time': avg_time,
                'avg_cpu_usage_percent': avg_cpu,
                'avg_memory_usage_mb': avg_memory,
                'iterations': iterations
            }, f, ensure_ascii=False)
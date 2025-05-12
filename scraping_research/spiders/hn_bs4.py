import scrapy
import time
import json
from bs4 import BeautifulSoup

class HNBS4Spider(scrapy.Spider):
    name = 'hn_bs4'
    start_urls = ['https://news.ycombinator.com/']

    def parse(self, response):
        iterations = 3
        data = []
        performance_metrics = []

        soup = BeautifulSoup(response.text, 'html.parser')

        for i in range(iterations):
            start_time = time.time()

            items = soup.find_all('tr', class_='athing')
            for item in items:
                titleline = item.find('span', class_='titleline')
                if not titleline or not titleline.find('a'):
                    continue  
                title = titleline.find('a').get_text()
                url = titleline.find('a')['href']
                next_tr = item.find_next_sibling('tr')
                if not next_tr:
                    continue  
                subtext = next_tr.find('td', class_='subtext')
                if not subtext or not subtext.find('span', class_='subline'):
                    continue 
                subtext = subtext.find('span', class_='subline')
                score = subtext.find('span', class_='score').get_text() if subtext.find('span', class_='score') else None
                author = subtext.find('a', class_='hnuser').get_text() if subtext.find('a', class_='hnuser') else None
                comments = subtext.find_all('a')[-1].get_text() if subtext.find_all('a') else None

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

        # Calculate average scraping time
        avg_time = sum(metric['scraping_time'] for metric in performance_metrics) / iterations

        # Save to JSON
        with open('hn_bs4.json', 'w', encoding='utf-8') as f:
            json.dump({
                'data': data,
                'performance_metrics': performance_metrics,
                'averages': {
                    'avg_scraping_time': avg_time
                },
                'iterations': iterations
            }, f, ensure_ascii=False)
import requests
from bs4 import BeautifulSoup
import time
import json

def scrape_hn_bs4():
    url = 'https://news.ycombinator.com/'
    iterations = 100  # Як у scrape_books_bs4
    data = []
    performance_metrics = []

    # Один HTTP-запит перед циклом
    response = requests.get(url)
    html_text = response.text  # Зберігаємо HTML для повторного використання

    for i in range(iterations):
        start_time = time.perf_counter()  # Початок заміру (включає ініціалізацію)
        soup = BeautifulSoup(html_text, 'lxml')  # Ініціалізація парсера з lxml
        items = soup.find_all('tr', class_='athing')
        for item in items:
            titleline = item.find('span', class_='titleline')
            title = titleline.find('a').get_text()
            url = titleline.find('a')['href']
            next_tr = item.find_next_sibling('tr')
            subtext = next_tr.find('td', class_='subtext').find('span', class_='subline')
            score = subtext.find('span', class_='score').get_text() if subtext.find('span', class_='score') else None
            author = subtext.find('a', class_='hnuser').get_text() if subtext.find('a', class_='hnuser') else None
            comments = subtext.find_all('a')[-1].get_text() if subtext.find_all('a') else None
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

    # Запис у JSON після всіх ітерацій
    with open('hn_bs4.json', 'w', encoding='utf-8') as f:
        json.dump({
            'data': data,
            'performance_metrics': performance_metrics,
            'averages': {'avg_scraping_time': avg_time},
            'iterations': iterations
        }, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    scrape_hn_bs4()
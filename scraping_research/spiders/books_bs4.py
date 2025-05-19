import requests
from bs4 import BeautifulSoup
import time
import json

def scrape_books_bs4():
    url = 'http://books.toscrape.com/'
    iterations = 100  # Збільшено для точності
    data = []
    performance_metrics = []

    # Один HTTP-запит перед циклом
    response = requests.get(url)
    html_text = response.text  # Зберігаємо HTML для повторного використання

    for i in range(iterations):
        start_time = time.perf_counter()  # Початок заміру (включає ініціалізацію)
        soup = BeautifulSoup(html_text, 'lxml')  # Ініціалізація парсера
        for book in soup.find_all('article', class_='product_pod'):
            title = book.find('h3').find('a')['title']
            price = book.find('p', class_='price_color').get_text()
            rating = book.find('p', class_='star-rating')['class'][1]
            if i == 0:  # Збирати дані тільки для першої ітерації
                data.append({'title': title, 'price': price, 'rating': rating})
        end_time = time.perf_counter()  # Кінець заміру
        adjusted_time = end_time - start_time
        performance_metrics.append({'iteration': i + 1, 'scraping_time': adjusted_time})

    avg_time = sum(metric['scraping_time'] for metric in performance_metrics) / iterations

    # Запис у JSON після всіх ітерацій
    with open('books_bs4.json', 'w', encoding='utf-8') as f:
        json.dump({
            'data': data,
            'performance_metrics': performance_metrics,
            'averages': {'avg_scraping_time': avg_time},
            'iterations': iterations
        }, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    scrape_books_bs4()
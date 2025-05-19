import json
import matplotlib.pyplot as plt

# Список JSON-файлів і їхніх назв для графіків
json_files = {
    'books_bs4.json': 'Books BS4',
    'books_css.json': 'Books CSS',
    'books_xpath.json': 'Books XPath',
    'hn_bs4.json': 'Hacker News BS4',
    'hn_css.json': 'Hacker News CSS',
    'hn_xpath.json': 'Hacker News XPath'
}

# Зчитування даних із JSON-файлів
data = {}
for file, name in json_files.items():
    try:
        with open(file, 'r', encoding='utf-8') as f:
            data[name] = json.load(f)
    except FileNotFoundError:
        print(f"Warning: Could not find {file}. Skipping {name}.")
        data[name] = {'averages': {'avg_scraping_time': 0}}

# Витягуємо середній час скрапінгу
scraping_times = [data[name]['averages'].get('avg_scraping_time', 0) for name in json_files.values()]
labels = list(json_files.values())

# Дані для групової діаграми (Books і Hacker News окремо)
books_times = [data['Books BS4']['averages'].get('avg_scraping_time', 0),
               data['Books CSS']['averages'].get('avg_scraping_time', 0),
               data['Books XPath']['averages'].get('avg_scraping_time', 0)]
hn_times = [data['Hacker News BS4']['averages'].get('avg_scraping_time', 0),
            data['Hacker News CSS']['averages'].get('avg_scraping_time', 0),
            data['Hacker News XPath']['averages'].get('avg_scraping_time', 0)]
tools = ['BS4', 'CSS', 'XPath']

# Налаштування стилю графіків
plt.style.use('ggplot')

# 1. Стовпчиковий графік (оригінальний)
fig1, ax1 = plt.subplots(figsize=(10, 6))
bars1 = ax1.bar(labels, scraping_times, color='skyblue')
ax1.set_title('Average Scraping Time (100 iterations, seconds)')
ax1.set_ylabel('Time (s)')
ax1.set_xticklabels(labels, rotation=45, ha='right')
for bar in bars1:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, height, f'{height:.6f}', 
             ha='center', va='bottom', fontsize=9)
plt.tight_layout(pad=3.0)
plt.savefig('scraping_comparison_bar.png', dpi=300, bbox_inches='tight')
plt.close(fig1)

# 2. Лінійний графік
fig2, ax2 = plt.subplots(figsize=(10, 6))
ax2.plot(labels[:3], scraping_times[:3], marker='o', linestyle='-', color='dodgerblue', label='Books')
ax2.plot(labels[3:], scraping_times[3:], marker='s', linestyle='-', color='orange', label='Hacker News')
ax2.set_title('Scraping Time Comparison (100 iterations)')
ax2.set_ylabel('Time (s)')
ax2.set_xticklabels(labels, rotation=45, ha='right')
ax2.legend()
for i, (x, y) in enumerate(zip(labels, scraping_times)):
    ax2.text(x, y, f'{y:.6f}', ha='center', va='bottom' if i < 3 else 'top', fontsize=9)
plt.tight_layout(pad=3.0)
plt.savefig('scraping_comparison_line.png', dpi=300, bbox_inches='tight')
plt.close(fig2)

# 3. Групова стовпчикова діаграма
fig3, ax3 = plt.subplots(figsize=(10, 6))
bar_width = 0.35
x = range(len(tools))
bars_books = ax3.bar([i - bar_width/2 for i in x], books_times, bar_width, label='Books', color='skyblue')
bars_hn = ax3.bar([i + bar_width/2 for i in x], hn_times, bar_width, label='Hacker News', color='salmon')
ax3.set_title('Scraping Time by Tool and Site (100 iterations)')
ax3.set_ylabel('Time (s)')
ax3.set_xticks(x)
ax3.set_xticklabels(tools)
ax3.legend()
for bars in [bars_books, bars_hn]:
    for bar in bars:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2, height, f'{height:.6f}', 
                 ha='center', va='bottom', fontsize=9)
plt.tight_layout(pad=3.0)
plt.savefig('scraping_comparison_grouped.png', dpi=300, bbox_inches='tight')
plt.close(fig3)

# Відображення всіх графіків
plt.show()
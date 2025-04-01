import json
import matplotlib.pyplot as plt

json_files = {
    'hn_css.json': 'Hacker News CSS',
    'hn_xpath.json': 'Hacker News XPath',
    'books_css.json': 'Books CSS',
    'books_xpath.json': 'Books XPath'
}

data = {}
for file, name in json_files.items():
    with open(file, 'r', encoding='utf-8') as f:
        data[name] = json.load(f)

scraping_times = [data[name]['avg_scraping_time'] for name in json_files.values()]
cpu_usages = [data[name]['avg_cpu_usage_percent'] for name in json_files.values()]
memory_usages = [data[name]['avg_memory_usage_mb'] for name in json_files.values()]
labels = list(json_files.values())

plt.style.use('ggplot') 
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 15))

ax1.bar(labels, scraping_times, color='skyblue')
ax1.set_title('Average Scraping Time (seconds)')
ax1.set_ylabel('Time (s)')
for i, v in enumerate(scraping_times):
    ax1.text(i, v + 0.001, f'{v:.4f}', ha='center', va='bottom')

ax2.bar(labels, cpu_usages, color='lightgreen')
ax2.set_title('Average CPU Usage (%)')
ax2.set_ylabel('CPU (%)')
for i, v in enumerate(cpu_usages):
    ax2.text(i, v + 0.1, f'{v:.1f}', ha='center', va='bottom')

ax3.bar(labels, memory_usages, color='salmon')
ax3.set_title('Average Memory Usage (MB)')
ax3.set_ylabel('Memory (MB)')
for i, v in enumerate(memory_usages):
    ax3.text(i, v + 1, f'{v:.1f}', ha='center', va='bottom')

plt.tight_layout()
plt.savefig('scraping_comparison.png', dpi=300) 
plt.show()  
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
    try:
        with open(file, 'r', encoding='utf-8') as f:
            data[name] = json.load(f)
    except FileNotFoundError:
        print(f"Warning: Could not find {file}. Skipping {name}.")
        data[name] = {'averages': {'avg_scraping_time': 0, 'avg_cpu_usage_percent': 0, 'avg_memory_usage_mb': 0}}

scraping_times = [data[name]['averages'].get('avg_scraping_time', 0) for name in json_files.values()]
cpu_usages = [data[name]['averages'].get('avg_cpu_usage_percent', 0) for name in json_files.values()]
memory_usages = [data[name]['averages'].get('avg_memory_usage_mb', 0) for name in json_files.values()]
labels = list(json_files.values())

plt.style.use('ggplot')
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 15))

bars1 = ax1.bar(labels, scraping_times, color='skyblue')
ax1.set_title('Average Scraping Time (seconds)')
ax1.set_ylabel('Time (s)')
for bar in bars1:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, height, f'{height:.4f}', 
             ha='center', va='bottom', fontsize=9)

bars2 = ax2.bar(labels, cpu_usages, color='lightgreen')
ax2.set_title('Average CPU Usage (%)')
ax2.set_ylabel('CPU (%)')
for bar in bars2:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2, height, f'{height:.1f}', 
             ha='center', va='bottom', fontsize=9)

bars3 = ax3.bar(labels, memory_usages, color='salmon')
ax3.set_title('Average Memory Usage (MB)')
ax3.set_ylabel('Memory (MB)')
for bar in bars3:
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2, height, f'{height:.1f}', 
             ha='center', va='bottom', fontsize=9)

plt.tight_layout(pad=3.0)
plt.savefig('scraping_comparison.png', dpi=300, bbox_inches='tight')
plt.show()
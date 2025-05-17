from operator import itemgetter
import requests
import matplotlib.pyplot as plt
import webbrowser

# Fetch Hacker News data (from hn_submissions.py)
url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
r = requests.get(url)
print(f"Status code: {r.status_code}")

submission_ids = r.json()
submission_dicts = []

for submission_id in submission_ids[:30]:
    url = f"https://hacker-news.firebaseio.com/v0/item/{submission_id}.json"
    r = requests.get(url)
    print(f"id: {submission_id}\tstatus: {r.status_code}")
    response_dict = r.json()

    if response_dict is None:
        continue

    submission_dict = {
        'title': response_dict.get('title', 'No Title'),
        'hn_link': f"https://news.ycombinator.com/item?id={submission_id}",
        'comments': response_dict.get('descendants', 0)
    }
    submission_dicts.append(submission_dict)

# Sort by number of comments
submission_dicts = sorted(submission_dicts, key=itemgetter('comments'), reverse=True)

# Prepare data for the bar chart
titles = [s['title'] for s in submission_dicts]
comments = [s['comments'] for s in submission_dicts]
urls = [s['hn_link'] for s in submission_dicts]

# Function to make bars clickable
def make_label_clickable(bar, url):
    def on_click(event):
        if event.inaxes:
            for b in bars:
                if b.contains(event)[0]:
                    webbrowser.open(url)
                    break
    return on_click

# Create the bar chart
fig, ax = plt.subplots(figsize=(12, 8))
bars = ax.bar(range(len(titles)), comments, tick_label=titles)

# Customize the chart
ax.set_xlabel('Submissions', fontsize=12)
ax.set_ylabel('Number of Comments', fontsize=12)
ax.set_title('Most Active Hacker News Discussions (Top 30)', fontsize=14)
plt.xticks(rotation=45, ha='right', fontsize=10)

# Make bars clickable
for i, bar in enumerate(bars):
    fig.canvas.mpl_connect('button_press_event', make_label_clickable(bar, urls[i]))

# Adjust layout to prevent label cutoff
plt.tight_layout()

# Show the plot
plt.show()
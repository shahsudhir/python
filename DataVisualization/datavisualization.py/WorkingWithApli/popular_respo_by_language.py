import requests
import matplotlib.pyplot as plt
import numpy as np
from operator import itemgetter

# List of programming languages to query
languages = ['Python', 'JavaScript', 'Ruby', 'C', 'Java', 'Perl', 'Haskell', 'Go']

# Store data for plotting
language_data = []
max_repos = 5  # Number of top repos to display per language

for language in languages:
    # Make API call to search repositories by language, sorted by stars
    url = f'https://api.github.com/search/repositories?q=language:{language}&sort=stars&order=desc&per_page={max_repos}'
    try:
        r = requests.get(url)
        if r.status_code == 403 and 'X-RateLimit-Remaining' in r.headers and r.headers['X-RateLimit-Remaining'] == '0':
            print(f"Rate limit exceeded for {language}. Consider using a GitHub API token.")
            continue
        r.raise_for_status()  # Raise exception for other bad status codes
        response_dict = r.json()
        
        # Extract repository data
        repo_dicts = response_dict.get('items', [])
        if not repo_dicts:
            print(f"No repositories found for {language}.")
            continue
        repo_names = []
        repo_stars = []
        
        for repo_dict in repo_dicts:
            repo_names.append(repo_dict['name'][:15])  # Truncate names to 15 chars
            repo_stars.append(repo_dict['stargazers_count'])
        
        # Store data for this language
        language_data.append({
            'language': language,
            'names': repo_names,
            'stars': repo_stars
        })
    except requests.RequestException as e:
        print(f"Error fetching data for {language}: {e}")

# Create a bar chart
plt.style.use('ggplot')  # Use 'ggplot' style instead of 'seaborn'
fig, ax = plt.subplots(figsize=(14, 8))

# Plot bars for each language
bar_width = 0.1
x = np.arange(max_repos)
colors = plt.cm.tab10(np.linspace(0, 1, len(languages)))

for i, lang_data in enumerate(language_data):
    language = lang_data['language']
    stars = lang_data['stars']
    # Adjust bar positions for each language
    ax.bar(x + i * bar_width, stars, bar_width, label=language, color=colors[i])

# Customize the chart
ax.set_xlabel('Repository', fontsize=12)
ax.set_ylabel('Stars (Log Scale)', fontsize=12)
ax.set_title('Most Popular Repositories by Language on GitHub', fontsize=14)
ax.set_xticks(x + bar_width * (len(languages) - 1) / 2)

# Use repository names from the first language as x-axis labels
if language_data:
    ax.set_xticklabels(language_data[0]['names'], rotation=45, ha='right')
    ax.set_yscale('log')  # Use logarithmic scale for stars
    ax.legend()

# Adjust layout to prevent label cutoff
plt.tight_layout()

# Save the chart
plt.savefig('popular_repos_by_language.png', dpi=300, bbox_inches='tight')
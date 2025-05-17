import requests
import plotly.express as px

# --- GitHub Data Fetching ---
github_username = "octocat"
github_url = f"https://api.github.com/users/{github_username}"
github_response = requests.get(github_url)
github_data = github_response.json()
repos_count = github_data.get("public_repos", 0)

# --- Hacker News Data Fetching ---
hn_top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
hn_top_ids = requests.get(hn_top_stories_url).json()

# Use the first story ID to fetch a single story (simplified)
story_id = hn_top_ids[0]
hn_story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
hn_story = requests.get(hn_story_url).json()
hn_title = hn_story.get("title", "Hacker News Story")
hn_comments = hn_story.get("descendants", 0)

# --- Create Plotly Bar Chart ---
data_labels = ["GitHub Public Repos", "Hacker News Comments"]
data_values = [repos_count, hn_comments]

fig = px.bar(
    x=data_labels,
    y=data_values,
    labels={"x": "Platform", "y": "Count"},
    title=f"GitHub vs Hacker News ({github_username} & 1 Top Story)",
    text=data_values,
)

# Customize the style
fig.update_layout(
    template="plotly_dark",
    title_font_size=22,
    title_font_color="lightblue",
    yaxis=dict(title="Count", showgrid=True),
    xaxis=dict(title="Source"),
)
fig.update_traces(marker_color=["#636EFA", "#EF553B"], textposition='outside')

# --- Show the plot ---
fig.show()

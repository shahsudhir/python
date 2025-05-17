from operator import itemgetter
import requests

# Make an API call and store the response
url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
r = requests.get(url)
print(f"Status code: {r.status_code}")

# Process information about each submission
submission_ids = r.json()
submission_dicts = []

for submission_id in submission_ids[:30]:
    # Make a separate API call for each submission
    url = f"https://hacker-news.firebaseio.com/v0/item/{submission_id}.json"
    r = requests.get(url)
    print(f"id: {submission_id}\tstatus: {r.status_code}")
    response_dict = r.json()

    if response_dict is None:
        continue  # Skip if the submission is not found

    # Build a dictionary for each article
    submission_dict = {
        'title': response_dict.get('title', 'No Title'),
        'hn_link': f"https://news.ycombinator.com/item?id={submission_id}",
        'comments': response_dict.get('descendants', 0)
    }
    submission_dicts.append(submission_dict)

# Sort the list of dictionaries by number of comments
submission_dicts = sorted(submission_dicts, key=itemgetter('comments'), reverse=True)

# Print the information
for submission in submission_dicts:
    print(f"\nTitle: {submission['title']}")
    print(f"Discussion link: {submission['hn_link']}")
    print(f"Comments: {submission['comments']}")

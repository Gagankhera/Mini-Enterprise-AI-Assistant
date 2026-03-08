import json

def get_github_summary():

    with open("data/github_data.json") as f:
        data = json.load(f)

    commits = data["commits"]

    summary = f"Repository {data['repo']} has {len(commits)} recent commits."

    return summary
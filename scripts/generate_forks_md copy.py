import os
import requests

API_URL = f"https://api.github.com/orgs/FabricEssentials/repos?per_page=100&type=owner"

def get_all_repos(url):
    repos = []
    while url:
        r = requests.get(url)
        r.raise_for_status()
        repos.extend(r.json())
        # Pagination
        url = r.links.get('next', {}).get('url')
    return repos

repos = get_all_repos(API_URL)
forks = [repo for repo in repos if repo.get("fork")]

with open("forks.md", "w", encoding="utf-8") as f:
    f.write("# Forked Repositories\n\n")
    if forks:
        for repo in forks:
            name = repo["name"]
            desc = repo.get("description") or ""
            url = repo["html_url"]
            f.write(f"- [{name}]({url}) - {desc}\n")
    else:
        f.write("No forked repositories found.\n")
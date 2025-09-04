import os
import requests

# Replace with your GitHub username or organization name
github_org = "FabricEssentials"

# GitHub API URL to fetch repositories
url = f"https://api.github.com/orgs/{github_org}/repos"
headers = {
    "Accept": "application/vnd.github.v3+json"
}

def fetch_repositories(api_url, headers):
    """Fetch all repositories for the given GitHub account."""
    repos = []
    while api_url:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        repos.extend(response.json())
        # Check for pagination
        api_url = response.links.get('next', {}).get('url')
    return repos

def fetch_repository_details(repo_name, headers):
    """Fetch detailed information for a specific repository."""
    repo_url = f"https://api.github.com/repos/{github_org}/{repo_name}"
    response = requests.get(repo_url, headers=headers)
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()

def generate_forks_markdown(forked_repos, microsoft_file="microsoftforks.md", community_file="communityforks.md"):
    """Generate two Markdown files: one for Microsoft-related forks and one for community forks."""
    microsoft_repos = []
    community_repos = []

    # Separate repositories based on the original owner
    for repo in forked_repos:
        parent = repo.get("parent", {})
        original_owner = parent.get("owner", {}).get("login", "").lower()
        if original_owner in {"azure", "microsoft"}:
            microsoft_repos.append(repo)
        else:
            community_repos.append(repo)

    # Write Microsoft-related forks to microsoft_file
    write_markdown_file(microsoft_repos, microsoft_file, "Microsoft Forked Repositories")

    # Write community forks to community_file
    write_markdown_file(community_repos, community_file, "Community Forked Repositories")


def write_markdown_file(repos, output_file, title):
    """Helper function to write a Markdown file for a list of repositories."""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        if repos:
            # Sort repos by name before writing
            sorted_repos = sorted(repos, key=lambda repo: repo["name"].lower())
            for repo in sorted_repos:
                name = repo["name"]
                description = repo.get("description", "No description available")
                fork_url = repo["html_url"]
                parent = repo.get("parent", {})

                original_url = parent.get("html_url", "Unknown")
                original_owner = parent.get("owner", {}).get("login", "Unknown")

                f.write(f"- **[{name}]({fork_url})**\n")
                f.write(f"  - **Original Repository**: [{original_url}]({original_url})\n")
                f.write(f"  - **Original Owner**: {original_owner}\n")
                f.write(f"  - **Description**: {description}\n\n")
        else:
            f.write("No forked repositories found.\n")

def main():
    # Fetch all repositories
    repos = fetch_repositories(url, headers)

    # Fetch detailed information for forked repositories
    forked_repos = []
    for repo in repos:
        if repo.get("fork"):
            detailed_repo = fetch_repository_details(repo["name"], headers)
            forked_repos.append(detailed_repo)

    # Sort forked_repos by repo["name"]
    forked_repos.sort(key=lambda repo: repo["name"])

    # Generate the Markdown file
    generate_forks_markdown(forked_repos)

if __name__ == "__main__":
    main()
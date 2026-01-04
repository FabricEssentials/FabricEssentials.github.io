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

def generate_forks_html(forked_repos, microsoft_file="microsoftforks.html", community_file="communityforks.html"):
    """Generate two HTML files: one for Microsoft-related forks and one for community forks."""
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
    write_html_file(microsoft_repos, microsoft_file, "Microsoft Repositories", "🏢", "Access Microsoft Fabric tools and resources hosted in Microsoft GitHub repositories, which may include non-official or unsupported projects")

    # Write community forks to community_file
    write_html_file(community_repos, community_file, "Community Repositories", "🌟", "Discover amazing tools and solutions created by talented members of the Microsoft Data Platform community available on GitHub")


def write_html_file(repos, output_file, title, emoji, subtitle):
    """Helper function to write an HTML file for a list of repositories."""
    html_template_start = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Fabric Essentials</title>
    <link rel="stylesheet" href="assets/css/style.css">
    <style>
        .repo-list {{
            max-width: 1000px;
            margin: 0 auto;
        }}
        
        .repo-item {{
            background: var(--white);
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px var(--shadow);
            border-left: 4px solid var(--fabric-green);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        
        .repo-item:hover {{
            transform: translateX(5px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }}
        
        .repo-name {{
            color: var(--fabric-green);
            font-size: 1.5em;
            font-weight: 600;
            margin: 0 0 15px 0;
            text-decoration: none;
            display: inline-block;
        }}
        
        .repo-name:hover {{
            color: var(--fabric-dark-green);
        }}
        
        .repo-meta {{
            display: flex;
            flex-direction: column;
            gap: 8px;
            margin-bottom: 15px;
            font-size: 0.95em;
        }}
        
        .repo-meta-item {{
            display: flex;
            align-items: baseline;
        }}
        
        .repo-meta-label {{
            font-weight: 600;
            color: var(--text-dark);
            margin-right: 8px;
            min-width: 150px;
        }}
        
        .repo-meta-value {{
            color: var(--text-light);
        }}
        
        .repo-meta-value a {{
            color: var(--fabric-teal);
            word-break: break-all;
        }}
        
        .repo-description {{
            color: var(--text-light);
            line-height: 1.6;
            margin-top: 10px;
            padding-top: 15px;
            border-top: 1px solid var(--background-light);
        }}
        
        .back-button {{
            display: inline-block;
            background: linear-gradient(135deg, var(--fabric-green) 0%, var(--fabric-teal) 100%);
            color: var(--white);
            padding: 12px 30px;
            border-radius: 25px;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 8px var(--shadow);
            margin: 20px 0;
        }}
        
        .back-button:hover {{
            transform: scale(1.05);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
            text-decoration: none;
        }}
        
        @media (max-width: 768px) {{
            .repo-meta-item {{
                flex-direction: column;
            }}
            
            .repo-meta-label {{
                min-width: auto;
                margin-bottom: 5px;
            }}
        }}
    </style>
</head>
<body>
    <div class="hero-section">
        <div class="logo-container">
            <img src="./images/fabric_48_color.png" alt="Microsoft Fabric">
            <img src="./images/The FE listings.png" alt="Fabric Essentials Listings" class="no-shadow">
        </div>
        <h1>{emoji} {title}</h1>
        <p class="subtitle">{subtitle}</p>
    </div>
    
    <div class="container">
        <div style="text-align: center; margin-bottom: 30px;">
            <a href="index.html" class="back-button">← Back to Home</a>
        </div>
        
        <div class="repo-list">
'''
    
    html_template_end = '''        </div>
        
        <div style="text-align: center; margin-top: 30px;">
            <a href="index.html" class="back-button">← Back to Home</a>
        </div>
    </div>
</body>
</html>
'''
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_template_start.format(title=title, emoji=emoji, subtitle=subtitle))
        
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

                repo_html = f'''            <div class="repo-item">
                <a href="{fork_url}" class="repo-name" target="_blank">{name}</a>
                <div class="repo-meta">
                    <div class="repo-meta-item">
                        <span class="repo-meta-label">Original Repository:</span>
                        <span class="repo-meta-value"><a href="{original_url}" target="_blank">{original_url}</a></span>
                    </div>
                    <div class="repo-meta-item">
                        <span class="repo-meta-label">Original Owner:</span>
                        <span class="repo-meta-value">{original_owner}</span>
                    </div>
                </div>
                <div class="repo-description">{description}</div>
            </div>
            
'''
                f.write(repo_html)
        else:
            f.write('            <p>No forked repositories found.</p>\n')
        
        f.write(html_template_end)

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

    # Generate the HTML files
    generate_forks_html(forked_repos)

if __name__ == "__main__":
    main()
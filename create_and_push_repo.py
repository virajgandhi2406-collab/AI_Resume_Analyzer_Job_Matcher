"""
One-Click GitHub Creator & Deployer for ResumePulse AI
------------------------------------------------------
Takes a GitHub Personal Access Token (PAT), creates the remote repository
on GitHub via the GitHub REST API, configures the remote origin, and pushes
the main branch.
"""

import os
import sys
import json
import urllib.request
import urllib.error
import dulwich.repo
import dulwich.porcelain

def create_github_repo(token, repo_name="AI_Resume_Analyzer_Job_Matcher", description=None, private=False):
    url = "https://api.github.com/user/repos"
    payload = {
        "name": repo_name,
        "description": description or "⚡ ResumePulse AI: Intelligent ATS Resume Analyzer & Job Matcher Platform (FastAPI, Python, Glassmorphic UI)",
        "private": private,
        "auto_init": False
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "ResumePulse-Deployer"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode())
            print(f"✅ Created new GitHub repository: {res_data.get('html_url')}")
            return res_data
    except urllib.error.HTTPError as e:
        err_body = e.read().decode()
        if e.code == 422:
            print(f"ℹ️ Repository '{repo_name}' already exists on your GitHub account. Proceeding to push...")
            return {"name": repo_name}
        else:
            print(f"❌ GitHub API Error ({e.code}): {err_body}")
            raise

def push_to_repo(token, username, repo_name="AI_Resume_Analyzer_Job_Matcher"):
    repo_path = os.path.dirname(os.path.abspath(__file__))
    repo = dulwich.repo.Repo(repo_path)

    clean_remote = f"https://github.com/{username}/{repo_name}.git"
    auth_remote = f"https://{token}@github.com/{username}/{repo_name}.git"
    display_url = f"https://github.com/{username}/{repo_name}"

    # Set remote origin in git config
    config = repo.get_config()
    config.set(("remote", "origin"), "url", clean_remote)
    config.write_to_path()
    print(f"✅ Configured remote origin: {clean_remote}")

    print(f"🚀 Pushing main branch to {display_url} ...")
    dulwich.porcelain.push(repo, auth_remote, "refs/heads/main:refs/heads/main")
    print("\n" + "="*65)
    print("🎉 SUCCESS! Your repository is LIVE on your GitHub Profile!")
    print(f"🌟 URL: {display_url}")
    print("="*65 + "\n")

def get_authenticated_user(token):
    url = "https://api.github.com/user"
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "ResumePulse-Deployer"
        }
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        return data.get("login")

def main():
    token = os.environ.get("GITHUB_TOKEN")
    if len(sys.argv) > 1:
        token = sys.argv[1].strip()

    if not token:
        print("Please provide your GitHub Personal Access Token (PAT).")
        print("Usage: python create_and_push_repo.py <GITHUB_TOKEN>")
        return

    print("🔐 Authenticating with GitHub...")
    try:
        username = get_authenticated_user(token)
        print(f"👤 Authenticated as: @{username}")
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return

    repo_name = "AI_Resume_Analyzer_Job_Matcher"
    if len(sys.argv) > 2:
        repo_name = sys.argv[2].strip()

    try:
        create_github_repo(token, repo_name=repo_name)
        push_to_repo(token, username, repo_name=repo_name)
    except Exception as e:
        print(f"❌ Deployment failed: {e}")

if __name__ == "__main__":
    main()

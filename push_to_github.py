"""
ResumePulse AI - GitHub Deployment & Push Utility
-------------------------------------------------
Pushes your local repository to a new or existing GitHub repository using Dulwich
(Pure Python Git engine) without requiring system git.exe to be installed.

Usage:
  1. Interactive mode (prompts for details):
     python push_to_github.py

  2. Direct URL:
     python push_to_github.py https://github.com/<USERNAME>/<REPO_NAME>.git

  3. Authenticated push with Personal Access Token (PAT):
     python push_to_github.py --user <USERNAME> --repo <REPO_NAME> --token <GITHUB_PAT>
"""

import sys
import os
import getpass
import argparse
import dulwich.repo
import dulwich.porcelain

def get_repo():
    repo_path = os.path.dirname(os.path.abspath(__file__))
    return dulwich.repo.Repo(repo_path)

def set_remote_origin(repo, remote_url):
    config = repo.get_config()
    config.set(("remote", "origin"), "url", remote_url)
    config.write_to_path()

def push_repository(repo, push_url, display_url):
    print(f"\n📡 Connecting to GitHub: {display_url}")
    print("⏳ Pushing 'main' branch...")
    try:
        dulwich.porcelain.push(repo, push_url, "refs/heads/main:refs/heads/main")
        print("\n" + "="*60)
        print("🎉 SUCCESS! Project is now LIVE on your GitHub profile!")
        print(f"🔗 Repository URL: {display_url}")
        print("="*60 + "\n")
        return True
    except Exception as e:
        err_msg = str(e)
        print("\n❌ Push failed. Error details:")
        print(f"   {err_msg}\n")
        print("💡 Why did this happen?")
        print("   1. GitHub requires a Personal Access Token (PAT) for HTTPS authentication.")
        print("      Create a token here: https://github.com/settings/tokens (classic, with 'repo' scope)")
        print("   2. The repository might not be created on GitHub yet.")
        print("      Create a new empty repo first at: https://github.com/new\n")
        print("👉 How to retry with your Token:")
        print("   python push_to_github.py --user <YOUR_GITHUB_USERNAME> --repo <YOUR_REPO_NAME> --token <YOUR_PAT_TOKEN>")
        return False

def main():
    parser = argparse.ArgumentParser(description="Push ResumePulse AI to GitHub")
    parser.add_argument("url", nargs="?", help="GitHub repository URL")
    parser.add_argument("--user", help="GitHub username")
    parser.add_argument("--repo", help="GitHub repository name")
    parser.add_argument("--token", help="GitHub Personal Access Token (PAT)")
    args = parser.parse_args()

    repo = get_repo()

    print("\n" + "="*60)
    print("⚡ ResumePulse AI — GitHub Deployment Helper")
    print("="*60)

    if args.url:
        remote_url = args.url.strip()
        set_remote_origin(repo, remote_url)
        push_repository(repo, remote_url, remote_url)
        return

    if args.user and args.repo:
        username = args.user.strip()
        repo_name = args.repo.strip()
        token = args.token.strip() if args.token else None
    else:
        print("\nEnter your GitHub repository details:")
        username = input("1. GitHub Username: ").strip()
        if not username:
            print("❌ Username cannot be empty.")
            return

        repo_name = input("2. GitHub Repository Name [default: AI_Resume_Analyzer_Job_Matcher]: ").strip()
        if not repo_name:
            repo_name = "AI_Resume_Analyzer_Job_Matcher"

        print("3. GitHub Personal Access Token (PAT):")
        print("   (Generate one at https://github.com/settings/tokens with 'repo' scope)")
        token = getpass.getpass("   Enter Token (or press Enter if using public/cached auth): ").strip()

    display_url = f"https://github.com/{username}/{repo_name}"
    clean_repo_url = f"https://github.com/{username}/{repo_name}.git"

    if token:
        push_url = f"https://{token}@github.com/{username}/{repo_name}.git"
    else:
        push_url = clean_repo_url

    set_remote_origin(repo, clean_repo_url)
    print(f"\n✅ Configured remote origin: {clean_repo_url}")
    push_repository(repo, push_url, display_url)

if __name__ == "__main__":
    main()

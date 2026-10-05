"""
Helper script to push ResumePulse AI repository to GitHub using pure Python (Dulwich)
or standard Git CLI.

Usage:
    python push_to_github.py https://github.com/<YOUR_USERNAME>/<YOUR_REPO>.git
"""

import sys
import dulwich.porcelain
import dulwich.repo

def main():
    if len(sys.argv) < 2:
        print("\n⚡ ResumePulse AI - GitHub Push Helper")
        print("---------------------------------------")
        print("Usage:")
        print("  python push_to_github.py <GITHUB_REPO_URL>")
        print("\nExample:")
        print("  python push_to_github.py https://github.com/myusername/AI_Resume_Analyzer_Job_Matcher.git\n")
        return

    remote_url = sys.argv[1].strip()
    repo = dulwich.repo.Repo(".")

    # Set or update remote origin
    config = repo.get_config()
    config.set(("remote", "origin"), "url", remote_url)
    config.write_to_path()
    print(f"✅ Configured remote origin: {remote_url}")

    print("🚀 Pushing main branch to GitHub...")
    try:
        dulwich.porcelain.push(repo, remote_url, "refs/heads/main:refs/heads/main")
        print("🎉 Successfully pushed to GitHub!")
    except Exception as e:
        print(f"\nNote: Push requires GitHub credentials/token if private. Error detail:\n{e}")
        print("\nAlternative: If you use VS Code, click 'Publish to GitHub' in the Source Control tab.")

if __name__ == "__main__":
    main()

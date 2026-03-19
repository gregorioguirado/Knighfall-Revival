"""
Triggers the track_players GitHub Actions workflow via the GitHub API.
Requires GITHUB_PAT in .env with Actions:write scope.
"""

import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

OWNER = "gregorioguirado"
REPO  = "Knighfall-Revival"
WORKFLOW_FILE = "track_players.yml"
BRANCH = "main"

token = os.getenv("GITHUB_PAT")
if not token:
    print("ERROR: GITHUB_PAT not found in .env")
    print("Create a fine-grained PAT at https://github.com/settings/tokens")
    print("Required permission: Actions > Read and write")
    print("Then add to .env:  GITHUB_PAT=your_token_here")
    sys.exit(1)

url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/workflows/{WORKFLOW_FILE}/dispatches"
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}
payload = {"ref": BRANCH}

resp = requests.post(url, headers=headers, json=payload)

if resp.status_code == 204:
    print("Workflow triggered successfully.")
    print(f"Check progress: https://github.com/{OWNER}/{REPO}/actions")
else:
    print(f"Failed ({resp.status_code}): {resp.text}")
    sys.exit(1)

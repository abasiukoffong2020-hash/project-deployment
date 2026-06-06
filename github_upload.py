"""
Upload repository files to a GitHub repository using the Contents API.
Usage:
  python github_upload.py --token <TOKEN> --owner <OWNER> --repo <REPO> [--create]

If --create is supplied, the script will attempt to create a repo under the
authenticated user account before uploading files.

Notes:
- Ensure `loan_model.pkl` and `scaler_top5.pkl` are committed; they are small in this repo.
- This script uploads all files under the current project directory recursively.
"""

import os
import base64
import argparse
import requests

API = "https://api.github.com"


def create_repo(token, name, private=True):
    url = f"{API}/user/repos"
    headers = {"Authorization": f"token {token}"}
    data = {"name": name, "private": private}
    r = requests.post(url, json=data, headers=headers)
    r.raise_for_status()
    return r.json()


def get_file_sha(token, owner, repo, repo_path, branch="main"):
    url = f"{API}/repos/{owner}/{repo}/contents/{repo_path}?ref={branch}"
    headers = {"Authorization": f"token {token}"}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.json().get("sha")
    return None


def upload_file(token, owner, repo, filepath, repo_path, message="Add file", branch="main"):
    url = f"{API}/repos/{owner}/{repo}/contents/{repo_path}"
    headers = {"Authorization": f"token {token}"}
    with open(filepath, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf-8")
    data = {"message": message, "content": content, "branch": branch}
    sha = get_file_sha(token, owner, repo, repo_path, branch=branch)
    if sha:
        data["sha"] = sha
    r = requests.put(url, json=data, headers=headers)
    if r.status_code not in (201, 200):
        raise RuntimeError(f"Failed to upload {repo_path}: {r.status_code} {r.text}")
    return r.json()


def find_files(root):
    exclude = {".git", "__pycache__"}
    for dirpath, dirnames, filenames in os.walk(root):
        # filter out excluded dirs
        dirnames[:] = [d for d in dirnames if d not in exclude]
        for fn in filenames:
            # skip large or unwanted files if necessary
            yield os.path.join(dirpath, fn)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", required=True, help="GitHub personal access token")
    parser.add_argument("--owner", required=True, help="GitHub owner (username or org)")
    parser.add_argument("--repo", required=True, help="Target repository name")
    parser.add_argument("--create", action="store_true", help="Create the repo under authenticated user")
    parser.add_argument("--branch", default="main")
    parser.add_argument("--path", default=".", help="Local project path to upload")
    args = parser.parse_args()

    if args.create:
        print(f"Creating repository {args.repo}...")
        create_repo(args.token, args.repo)

    files = list(find_files(args.path))
    print(f"Found {len(files)} files to upload (including hidden).\nUploading...")

    for fp in files:
        # compute repo path relative to project root
        repo_path = os.path.relpath(fp, args.path).replace("\\\\", "/")
        print(f"Uploading {repo_path}...")
        try:
            upload_file(args.token, args.owner, args.repo, fp, repo_path, message=f"Add {repo_path}", branch=args.branch)
        except Exception as e:
            print(f"Error uploading {repo_path}: {e}")
            raise

    print("Upload complete.")

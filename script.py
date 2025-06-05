import requests
import os

token = os.getenv("GITHUB_TOKEN")
org = "tier4"
headers = {"Authorization": f"token {token}"}
repos = []

page = 1
while True:
    url = f"https://api.github.com/orgs/{org}/repos?per_page=100&page={page}"
    response = requests.get(url, headers=headers)
    data = response.json()
    if not data:
        break
    repos.extend(data)
    page += 1
    break

for repo in repos:
    print(repo["full_name"])

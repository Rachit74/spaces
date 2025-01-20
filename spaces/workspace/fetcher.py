from github import Github

with open('../pat.txt') as r:
    pat = r.read().strip()  # Read the file and remove any leading/trailing spaces


def fetch_repository_commits(repository_url):
    g = Github(pat)

    repository_name = repository_url.split("github.com/")[-1]

    repository = g.get_repo(repository_name)

    commits = repository.get_commits()

    return commits
import os
from github import Github, Auth

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_ORG_NAME = os.getenv("GITHUB_ORG_NAME")
# Github Repo names is a string of items separated by a comma.
# e.g: name1,name2. Once the script runs the names will be
# ["name1", "name2"]
GITHUB_REPO_NAMES = os.getenv("GITHUB_REPO_NAMES")


class GithubClient:
    def __init__(self, token: str = GITHUB_TOKEN) -> None:
        self.gh = self._get_client(token)

    def _get_client(self, token: str) -> Github:
        _auth = Auth.Token(token)
        _g = Github(auth=_auth)
        _ = _g.get_user().login
        return _g

    def create_repos(self, org: str, repo_names: list[str]) -> bool:
        _gh_organization = self.gh.get_organization(org)
        for repo_name in repo_names:
            _ = _gh_organization.create_repo(
                repo_name,
                allow_rebase_merge=True,
                auto_init=False,
                has_issues=True,
                has_projects=False,
                has_wiki=False,
            )


def get_repo_names_list(names: str) -> list[str]:
    return names.split(",")


if __name__ == "__main__":
    github_client = GithubClient()
    repo_names_list = get_repo_names_list(GITHUB_REPO_NAMES)
    github_client.create_repos(GITHUB_ORG_NAME, repo_names_list)
    print(f"Successfully created {len(repo_names_list)} repos.")

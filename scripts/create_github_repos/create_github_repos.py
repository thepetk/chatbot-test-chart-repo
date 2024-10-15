from dataclasses import dataclass
import os
import base64
from github import Github
from github.Auth import Auth
from github.Repository import Repository
from github.InputGitTreeElement import InputGitTreeElement

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_ORG_NAME = os.getenv("GITHUB_ORG_NAME")
# Github Repo names is a string of items separated by a comma.
# e.g: name1,name2. Once the script runs the names will be
# ["name1", "name2"]
GITHUB_APP_REPO = os.getenv("GITHUB_APP_REPO")
GITHUB_GITOPS_REPO = os.getenv("GITHUB_GITOPS_REPO")
GITHUB_SOURCE_REPO = os.getenv("GITHUB_SOURCE_REPO")
GITHUB_DEFAULT_BRANCH = os.getenv("GITHUB_DEFAULT_BRANCH")
SOURCE_REPO_APP_CONTENT_PATH = "content"
SOURCE_REPO_GITOPS_CONTENT_PATH = "charts/ai-rhdh-software-templates/chatbot/0.2.0"


@dataclass
class GithubBlob:
    path: str
    content: str
    btype: str = "blob"
    mode: str = "100644"


class GithubClient:
    def __init__(self, token: str = GITHUB_TOKEN) -> None:
        self.gh = self._get_client(token)

    def _get_client(self, token: str) -> Github:
        _g = Github(login_or_token=token)
        _ = _g.get_user().login
        return _g

    def _get_new_target_file_path(
        self, target_file_path: str, target_dir_path: str = ""
    ) -> str:
        return (
            f"{target_dir_path}/{target_file_path}"
            if target_dir_path
            else target_file_path
        )

    def _commit_new_files(
        self, blobs: list[GithubBlob], target_repo: Repository
    ) -> bool:
        _gh_tree_elements: list[InputGitTreeElement] = []

        for blob in blobs:
            _gh_blob = target_repo.create_git_blob(blob.content, "utf-8")
            _gh_tree_elements.append(
                InputGitTreeElement(
                    path=blob.path, mode=blob.mode, type=blob.btype, sha=_gh_blob.sha
                )
            )
        _gh_head_sha = target_repo.get_branch(target_repo.default_branch).commit.sha
        _gh_base_tree = target_repo.get_git_tree(sha=_gh_head_sha)
        _gh_new_tree = target_repo.create_git_tree(_gh_tree_elements, _gh_base_tree)
        _gh_parent_commit = target_repo.get_git_commit(sha=_gh_head_sha)
        _gh_new_commit = target_repo.create_git_commit(
            "Copy repo content", _gh_new_tree, [_gh_parent_commit]
        )
        _default_refs = target_repo.get_git_ref(f"heads/{target_repo.default_branch}")
        _default_refs.edit(sha=_gh_new_commit.sha)

        return True

    def _copy_contents_from_source(
        self,
        source_repo: Repository,
        target_repo: Repository,
        source_path: str = "",
        target_path: str = "",
    ) -> bool:
        _src_contents = source_repo.get_contents(source_path)
        _new_blobs: list[GithubBlob] = []
        for content_file in _src_contents:

            if content_file.type == "dir":
                new_target_path = self._get_new_target_file_path(
                    target_path, content_file.path
                )
                _ = self._copy_contents_from_source(
                    source_repo, target_repo, content_file.path, new_target_path
                )
            else:
                file_content = base64.b64decode(content_file.content).decode("utf-8")
                blob_path = content_file.path.replace(f"{source_path}/", "")
                _new_blobs.append(GithubBlob(path=blob_path, content=file_content))
        import pdb

        pdb.set_trace()

        _r = self._commit_new_files(_new_blobs, target_repo)
        return _r

    def _create_repo(self, org: str, repo_name: str, default_branch: str) -> bool:
        _gh_organization = self.gh.get_organization(org)
        _repo = _gh_organization.create_repo(
            repo_name,
            allow_rebase_merge=True,
            auto_init=False,
            has_issues=True,
            has_projects=False,
            has_wiki=False,
        )
        _repo.create_file(".gitignore", "Initial Commit", "", branch=default_branch)
        _repo.edit(default_branch=default_branch)
        return _repo

    def create_repo(
        self,
        org: str,
        repo_name: str,
        source_repo_path: str,
        source_repo: str = GITHUB_SOURCE_REPO,
        default_branch: str = GITHUB_DEFAULT_BRANCH,
    ) -> bool:
        _target_repo = self._create_repo(org, repo_name, default_branch)
        _source_repo = self.gh.get_repo(source_repo)

        _ = self._copy_contents_from_source(
            _source_repo,
            _target_repo,
            source_repo_path,
        )
        return True


if __name__ == "__main__":
    github_client = GithubClient()
    github_client.create_repo(
        GITHUB_ORG_NAME,
        GITHUB_APP_REPO,
        SOURCE_REPO_APP_CONTENT_PATH,
        GITHUB_SOURCE_REPO,
    )
    github_client.create_repo(
        GITHUB_ORG_NAME,
        GITHUB_GITOPS_REPO,
        SOURCE_REPO_GITOPS_CONTENT_PATH,
        GITHUB_SOURCE_REPO,
    )
    print(f"Successfully created 2 repos.")

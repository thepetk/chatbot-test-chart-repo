from dataclasses import dataclass
import os
import base64
import logging
import sys
from github import Github
from github.Repository import Repository
from github.InputGitTreeElement import InputGitTreeElement
from github.ContentFile import ContentFile

APP_NAME = os.getenv("APP_NAME")
APP_NAMESPACE = os.getenv("APP_NAMESPACE")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_ORG_NAME = os.getenv("GITHUB_ORG_NAME")
GITHUB_SOURCE_REPO = os.getenv("GITHUB_SOURCE_REPO")
GITHUB_TETKON_SOURCE_REPO = os.getenv("GITHUB_TETKON_SOURCE_REPO")
GITHUB_DEFAULT_BRANCH = os.getenv("GITHUB_DEFAULT_BRANCH")
SOURCE_REPO_APP_CONTENT_PATH = "chatbot"
SOURCE_TEKTON_REPO_CONTENT_PATH = "pac/pipelineRuns"
TEKTON_FILE_APP_NAME_REPLACEMENT = "application_name_replace"
TEKTON_FILE_APP_NAMESPACE_REPLACEMENT = "application_namespace_replace"
TEKTON_FILE_QUAY_ACCOUNT_REPLACEMENT = "quay_account_replace"
QUAY_ACCOUNT_NAME = os.getenv("QUAY_ACCOUNT_NAME")


def get_logger() -> logging.Logger:
    logger = logging.getLogger(__name__)
    console_handler = logging.StreamHandler()
    logger.addHandler(console_handler)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "{asctime} - {levelname} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M",
    )
    console_handler.setFormatter(formatter)
    return logger


log = get_logger()


@dataclass
class GithubBlob:
    path: str
    content: str
    btype: str = "blob"
    mode: str = "100644"
    old_str: str = ""
    new_str: str = ""


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

    def _is_tekton_file(self, path: str) -> bool:
        return ".tekton/docker-push.yaml" in path

    def _update_tekton_yaml_content(
        self,
        content: str,
        existing_name: str = TEKTON_FILE_APP_NAME_REPLACEMENT,
        new_name: str = APP_NAME,
        existing_namespace: str = TEKTON_FILE_APP_NAMESPACE_REPLACEMENT,
        new_namespace: str = APP_NAMESPACE,
        existing_quay_account_name: str = TEKTON_FILE_QUAY_ACCOUNT_REPLACEMENT,
        new_quay_account_name: str = QUAY_ACCOUNT_NAME,
    ) -> str:
        return (
            content.replace(existing_name, new_name)
            .replace(existing_namespace, new_namespace)
            .replace(existing_quay_account_name, new_quay_account_name)
        )

    def _commit_new_files(
        self, blobs: "list[GithubBlob]", target_repo: Repository
    ) -> bool:
        _gh_tree_elements: list[InputGitTreeElement] = []

        for blob in blobs:
            content = (
                blob.content
                if not self._is_tekton_file(blob.path)
                else self._update_tekton_yaml_content(blob.content)
            )
            _gh_blob = target_repo.create_git_blob(content, "utf-8")
            _gh_tree_elements.append(
                InputGitTreeElement(
                    path=blob.path, mode=blob.mode, type=blob.btype, sha=_gh_blob.sha
                )
            )
        # creates a new commit tree for all blobs in order to push all files with
        # one commit
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

    def _create_content_blobs(
        self,
        contents: "list[ContentFile]",
        repo: Repository,
        initial_source: str = "",
    ) -> "list[GithubBlob]":
        _new_blobs: list[GithubBlob] = []
        for content_file in contents:
            if content_file.type == "dir":
                _updated_contents = repo.get_contents(content_file.path)
                _new_blobs += self._create_content_blobs(
                    _updated_contents,
                    repo,
                    initial_source,
                )
            else:
                file_content = base64.b64decode(content_file.content).decode("utf-8")
                blob_path = content_file.path.replace(f"{initial_source}/", "")
                _new_blobs.append(GithubBlob(path=blob_path, content=file_content))

        return _new_blobs

    def _add_blobs_to_target_repo(
        self, new_blobs: "list[GithubBlob]", target_repo: Repository
    ) -> bool:
        _r = self._commit_new_files(new_blobs, target_repo)
        log.info("blobs were commited succussfully")
        return _r

    def _create_repo(self, org: str, repo_name: str, default_branch: str) -> bool:
        # creates the repo in the given organization.
        _gh_organization = self.gh.get_organization(org)
        _repo = _gh_organization.create_repo(
            repo_name,
            allow_rebase_merge=True,
            auto_init=False,
            has_issues=True,
            has_projects=False,
            has_wiki=False,
        )
        # sets the default branch for the new repo
        _repo.create_file(".gitignore", "Initial Commit", "", branch=default_branch)
        _repo.edit(default_branch=default_branch)
        log.info(f"{repo_name} repo created and new default branch is {default_branch}")
        return _repo

    def create_repo(
        self,
        org: str,
        repo_name: str,
        source_repo_path: str,
        source_repo_name: str = GITHUB_SOURCE_REPO,
        tekton_repo_name: str = GITHUB_TETKON_SOURCE_REPO,
        tekton_repo_path: str = SOURCE_TEKTON_REPO_CONTENT_PATH,
        default_branch: str = GITHUB_DEFAULT_BRANCH,
    ) -> bool:
        log.info(f"creating {repo_name} in {org} org")
        _target_repo = self._create_repo(org, repo_name, default_branch)
        _source_repo = self.gh.get_repo(source_repo_name)
        _tekton_repo = self.gh.get_repo(tekton_repo_name)

        log.info(
            f"getting all contents from {source_repo_name} repo from the {source_repo_path} path"
        )
        _source_contents = _source_repo.get_contents(source_repo_path)
        new_blobs = self._create_content_blobs(
            _source_contents, _source_repo, source_repo_path
        )

        log.info(
            f"getting all contents from {tekton_repo_name} repo from the {tekton_repo_path} path"
        )
        _tekton_contents = _tekton_repo.get_contents(tekton_repo_path)
        new_blobs += self._create_content_blobs(
            _tekton_contents, _tekton_repo, tekton_repo_path
        )

        log.info(f"copying all {len(new_blobs)} to the {_target_repo.name} repo")
        _ = self._add_blobs_to_target_repo(new_blobs, _target_repo)
        return True


if __name__ == "__main__":
    log.info("Connecting to github")
    github_client = GithubClient()

    # Check if github repo already exists
    try:
        _ = github_client.gh.get_repo(f"{GITHUB_ORG_NAME}/{APP_NAME}")
        sys.exit(f"{APP_NAME} repository already exists in {GITHUB_ORG_NAME}")
    except Exception:
        pass

    github_client.create_repo(
        GITHUB_ORG_NAME,
        APP_NAME,
        SOURCE_REPO_APP_CONTENT_PATH,
        GITHUB_SOURCE_REPO,
    )

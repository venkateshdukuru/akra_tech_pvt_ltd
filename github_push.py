import re
from urllib.parse import urlparse
from github import Github
from github.Repository import Repository
import github
from typing import Optional

def does_object_exists_in_branch(repo: Repository, branch: str, object_path: str) -> bool:
    """Checks whether the file already exists or not."""
    try:
        repo.get_contents(object_path, branch)
        return True
    except github.UnknownObjectException:
        return False

def link_validator(repository_link: str) -> bool:
    """Link Validator."""
    return re.search("https://github.com/[\\w-]+/[\\w-]+$", repository_link) is not None

def parse_repository(repository_link: str) -> str:
    """Parses the repository link to get the repository name."""
    parsed_url = urlparse(repository_link)
    path_components = parsed_url.path.split('/')
    repository_name = "/".join(path_components[1:3])
    return repository_name

def create_config_file(repository: Repository, file_name: str, yaml_content: str) -> str:
    """Creates a new file in the repository."""
    repository.create_file(file_name, "Created YAML file", yaml_content)
    return "YAML file created successfully!"

def update_config_file(repository: Repository, file_name: str, yaml_content: str) -> str:
    """Updates an existing file in the repository."""
    contents = repository.get_contents(file_name)
    repository.update_file(file_name, "Updated YAML file", yaml_content, contents.sha)
    return "YAML file updated successfully!"

def get_repository(github_token: str, repository_name: str) -> Repository:
    """Gets the repository object."""
    g = Github(github_token)
    return g.get_repo(repository_name)

def push_to_github(access_token: str, yaml_content: str, repository_link: str) -> Optional[str]:
    """Pushes or updates the YAML file in the GitHub repository."""
    if not link_validator(repository_link):
        return "Invalid repository link."

    repository_name = parse_repository(repository_link)
    repository = get_repository(access_token, repository_name)
    file_name = ".github/workflows/config.yml"

    try:
        if does_object_exists_in_branch(repository, "main", file_name):
            return update_config_file(repository, file_name, yaml_content)
        else:
            return create_config_file(repository, file_name, yaml_content)
    except Exception as e:
        return f"Error during GitHub interaction: {str(e)}"

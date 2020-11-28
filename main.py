from secrets import github_token, project_path
from github import Github
from git import Repo
import sys


class ProjectInitAutomator:
    def __init__(self, repo_name, is_private):
        self.repo_name = repo_name
        self.is_private = is_private
        self.repo_full_name = self.create_github_repo(
            self.repo_name, self.is_private)
        self.clone_repo(self.repo_full_name, project_path)

    def create_github_repo(self, repo_name, is_private):
        """ This function creates a new Github repo(public or private), with its own .gitignore for Python and a Readme.md file """
        g = Github(github_token)
        user = g.get_user()

        try:
            repo_full_name = user.create_repo(
                name=repo_name, private=is_private, auto_init=True, gitignore_template="Python").full_name
            print("Done! New repo full name is\t{}".format(repo_full_name))
            return repo_full_name
        except Exception as e:
            error_message = e.args[1]["message"]
            error_cause = e.args[1]["errors"][0]["message"]
            print("{}\n{}".format(error_message, error_cause))
            sys.exit()

    def clone_repo(self, repo_full_name, project_path):
        """ This function clones the repo from Github """
        g = Github(github_token)
        repo = g.get_repo(repo_full_name)
        clone_url = repo.clone_url
        repo_cloned_path = project_path + repo.name
        try:
            Repo.clone_from(clone_url, repo_cloned_path)
            print("Done! New repo cloned in {}".format(repo_cloned_path))
        except Exception as e:
            print("There's a problem cloning the repo:\n{}".format(
                e.args[2].decode('UTF-8')))

    def create_vevn(self):
        """ Function that creates a virtual environment inside the project
        folder, and that install some packages needed by VS Code, and excludes
        the .vscode folder in .gitignore """

        pass

    def repo_config(self):
        pass


if __name__ == '__main__':
    pia = ProjectInitAutomator("repo_name", True)

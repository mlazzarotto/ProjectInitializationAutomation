from secrets import github_token, project_path, code_path
from github import Github
from git import Repo
import venv
import subprocess
import sys
import os
import pip


class ProjectInitAutomator:
    def __init__(self, repo_name, is_private):
        self.repo_name = repo_name
        self.is_private = is_private
        self.repo_path = project_path + self.repo_name

        self.repo_full_name = self.create_github_repo(
            self.repo_name, self.is_private)
        self.clone_repo(self.repo_full_name, self.repo_path)
        self.create_venv(self.repo_path)
        self.repo_config(self.repo_path)
        self.gitignore_modifier(self.repo_path)
        self.file_creator(self.repo_path)

        # Command to open the folder in VS Code
        subprocess.run(code_path + " -a " + self.repo_path)
        print("All done! Enjoi :)")

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

    def clone_repo(self, repo_full_name, repo_path):
        """ This function clones the repo from Github """
        g = Github(github_token)
        repo = g.get_repo(repo_full_name)
        clone_url = repo.clone_url

        try:
            Repo.clone_from(clone_url, repo_path)
            print("Done! New repo cloned in\t{}".format(repo_path))
        except Exception as e:
            print("There's a problem cloning the repo:\n{}".format(
                e.args[2].decode('UTF-8')))

    def create_venv(self, repo_path):
        """ Function that creates a virtual environment inside the project
        folder, and that install some packages needed by VS Code, and excludes
        the .vscode folder in .gitignore """
        venv_dir = repo_path + "\\.venv"
        try:
            venv.create(venv_dir)
            print("Done! Created a new virtual environment in\t{}".format(venv_dir))
        except Exception as e:
            print(e)

    def repo_config(self, repo_path):
        """ Functions that updates pip and installs autopep8 and pylint inside
        the virual environment"""
        env = os.environ
        virtual_env = repo_path + "\\.venv"
        env.update({"VIRTUAL_ENV": virtual_env})

        path = virtual_env + "\\Scripts;" + env["PATH"]
        env.update({"PATH": path})

        subprocess.run("pip install --upgrade pip",
                       env=env, stdout=subprocess.DEVNULL)
        subprocess.run("pip install autopep8 pylint",
                       env=env, stdout=subprocess.DEVNULL)

    def gitignore_modifier(self, repo_path):
        """ Function that excludes the VS Code folder and the secrets.py from
        being tracked by git """
        gitignore_file = repo_path + "\\.gitignore"
        try:
            with open(gitignore_file, "a") as file:
                file.write("\n\n")
                file.write(".vscode\n")
                file.write("secrets.py\n")
            print("Done! Added vscode and secrets.py to .gitignore")
        except Exception as e:
            print("Couldn't open the file .gitignore!")
            print(e)

    def file_creator(self, repo_path):
        """ Function that creates an empty main.py file """
        if os.path.exists(repo_path):
            with open(os.path.join(repo_path + "\\" + "main.py"), "a"):
                print("Done! Created main.py")


if __name__ == '__main__':
    pia = ProjectInitAutomator("repo_new_final", True)

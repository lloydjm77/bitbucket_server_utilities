"""
Generates a shell script for performing operations on Bitbucket repos.  This
is useful for performing batch commits, for example when updating a Jenkinsfile.
"""

import textwrap
import utils
from project import Project


class GenerateScript:
    """Driver for generating scripts."""

    def __init__(self):
        self.project = Project()

    def generate(self):
        config = utils.parse_config()
        commands = config.get('commands')
        output = ''
        separator = ' && '
        for repo in self.project.get_repos(**config):
            clone_info = repo.get('links').get('clone')
            for clone_info_item in clone_info:
                if clone_info_item.get('name') == 'http':
                    clone_http_href = clone_info_item.get('href')
                if clone_info_item.get('name') == 'ssh':
                    clone_ssh_href = clone_info_item.get('href')

            for command in commands:
                command_replaced = command.replace(
                    '{url}', clone_http_href).replace(
                    '{url:htttp}', clone_http_href).replace(
                    '{url:ssh}', clone_ssh_href).replace(
                    '{project}', config.get('bitbucket').get(
                        'project')).replace('{repo}', repo.get('slug'))
                output += textwrap.dedent(f'{command_replaced}{separator}')

        if output.endswith(separator):
            output=output[:len(output)-4]

        print(output)



if __name__ == '__main__':
    GenerateScript().generate()

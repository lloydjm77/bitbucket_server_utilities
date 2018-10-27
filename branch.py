"""
Utilities for working with Bitbucket branches.
"""
import json
import requests
from tabulate import tabulate
from utils import log

class Branch:
    """Utilities for working with Bitbucket branches."""

    __create_branch_data__ = {"name": "", "startPoint": ""}

    __all_users_branch_permission_data_list__ = [
        {'type': 'fast-forward-only', 'matcher': {'id': '',
                                                  'type': {'id': 'BRANCH'}, 'active': 'true'}},
        {'type': 'no-deletes', 'matcher': {'id': '',
                                           'type': {'id': 'BRANCH'}, 'active': 'true'}}
    ]
    __specific_users_branch_permission_data_list__ = [
        {'type': 'pull-request-only', 'matcher': {'id': '',
                                                  'type': {'id': 'BRANCH'}, 'active': 'true'},
         'users': []}
    ]

    @log
    def set_default_permissions_for_project(self, **kwargs):
        """Sets standard branch permissions for a repo."""
        bitbucket_config = kwargs.get('bitbucket')
        branch_list = ['release', 'master']

        url = f"http://{bitbucket_config.get('host')}/rest/branch-permissions/2.0"
        url += f"/projects/{bitbucket_config.get('project')}/restrictions"

        self.allow_bypass_pull_request_for_project("jenkins-bitbucket-user", **kwargs)

        responses = []
        for branch in branch_list:
            for data in self.__all_users_branch_permission_data_list__:
                data['matcher']['id'] = f'refs/heads/{branch}'
                responses.append(requests.request(
                    'POST', url, headers=kwargs.get('default_headers'), json=data))

        return responses

    @log
    def allow_bypass_pull_request_for_project(self, users, **kwargs):
        """Removes standard branch permissions for a repo."""
        bitbucket_config = kwargs.get('bitbucket')
        branch_list = ['release', 'master']

        url = f"http://{bitbucket_config.get('host')}/rest/branch-permissions/2.0"
        url += f"/projects/{bitbucket_config.get('project')}/restrictions"

        responses = []
        branch_list = ['release', 'master']
        for branch in branch_list:
            for data in self.__specific_users_branch_permission_data_list__:
                data['matcher']['id'] = f'refs/heads/{branch}'
                data['users'] = users.split(',')
                responses.append(requests.request(
                    'POST', url, headers=kwargs.get('default_headers'), json=data))

        return responses

    @log
    def set_default_permissions(self, **kwargs):
        """Sets standard branch permissions for a repo."""
        bitbucket_config = kwargs.get('bitbucket')
        branch_list = ['release', 'master']

        url = f"http://{bitbucket_config.get('host')}/rest/branch-permissions/2.0"
        url += f"/projects/{bitbucket_config.get('project')}/repos/{bitbucket_config.get('repo')}"
        url += "/restrictions"

        self.allow_bypass_pull_request("jenkins-bitbucket-user", **kwargs)

        responses = []
        for branch in branch_list:
            for data in self.__all_users_branch_permission_data_list__:
                data['matcher']['id'] = f'refs/heads/{branch}'
                responses.append(requests.request(
                    'POST', url, headers=kwargs.get('default_headers'), json=data))

        return responses

    @log
    def allow_bypass_pull_request(self, users, **kwargs):
        """Removes standard branch permissions for a repo."""
        bitbucket_config = kwargs.get('bitbucket')
        branch_list = ['release', 'master']

        url = f"http://{bitbucket_config.get('host')}/rest/branch-permissions/2.0"
        url += f"/projects/{bitbucket_config.get('project')}/repos/{bitbucket_config.get('repo')}"
        url += "/restrictions"

        responses = []
        branch_list = ['release', 'master']
        for branch in branch_list:
            for data in self.__specific_users_branch_permission_data_list__:
                data['matcher']['id'] = f'refs/heads/{branch}'
                data['users'] = users.split(',')
                responses.append(requests.request(
                    'POST', url, headers=kwargs.get('default_headers'), json=data))

        return responses

    @log
    def set_default_branch(self, json_input, **kwargs):
        """Sets the default branch for a repo."""
        bitbucket_config = kwargs.get('bitbucket')
        parameters = json.loads(json_input)
        url = f"http://{bitbucket_config.get('host')}/rest/api/1.0"
        url += f"/projects/{bitbucket_config.get('project')}"
        url += f"/repos/{bitbucket_config.get('repo')}/branches/default"
        return requests.request('PUT', url, headers=kwargs.get(
            'default_headers'), json={'id': parameters['name']})

    def list_branches(self, **kwargs):
        """List branches in a repo."""
        bitbucket_config = kwargs.get('bitbucket')
        url = f"http://{bitbucket_config.get('host')}/rest/api/1.0"
        url += f"/projects/{bitbucket_config.get('project')}"
        url += f"/repos/{bitbucket_config.get('repo')}/branches?details=true"

        api_response = requests.request('GET', url, headers=kwargs.get(
            'default_headers'))

        # print(api_response.text)
        data = json.loads(api_response.text)
        
        print(f"\n{bitbucket_config.get('project')}/{bitbucket_config.get('repo')}")
        headers = ['Name', 'Ahead/Behind Release', 'Latest Author']
        table = []

        for branch in data['values']:
            metadata = branch['metadata']
            latestCommitMetadata = metadata['com.atlassian.bitbucket.server.bitbucket-branch:latest-commit-metadata']

            row = []
            row.append(branch['displayId'])
            if 'com.atlassian.bitbucket.server.bitbucket-branch:ahead-behind-metadata-provider' in metadata:
                aheadBehind = metadata['com.atlassian.bitbucket.server.bitbucket-branch:ahead-behind-metadata-provider']
                row.append(f"{aheadBehind['ahead']}/{aheadBehind['behind']}")
            else:
                row.append("N/A")
            row.append(latestCommitMetadata['author']['name'])
            table.append(row)

        print(tabulate(table, headers))

    @log
    def create_branch(self, json_input, **kwargs):
        """Creates a branch in a repo."""
        bitbucket_config = kwargs.get('bitbucket')
        parameters = json.loads(json_input)
        url = f"http://{bitbucket_config.get('host')}/rest/api/1.0"
        url += f"/projects/{bitbucket_config.get('project')}"
        url += f"/repos/{bitbucket_config.get('repo')}/branches"
        data = self.__create_branch_data__
        data['name'] = parameters['name']
        data['startPoint'] = parameters['startPoint']
        return requests.request('POST', url, headers=kwargs.get(
            'default_headers'), json=data)

    @log
    def delete_branch(self, branchArgs, **kwargs):
        """Deletes a branch in a repo."""
        bitbucket = kwargs.get('bitbucket')
        url = f"http://{bitbucket.get('host')}/rest/branch-utils/1.0/projects/"
        url += f"{bitbucket.get('project')}/repos/{bitbucket.get('repo')}/branches"
        return requests.request('DELETE', url, headers=kwargs.get(
            'default_headers'), json={
                'name': branchArgs
            })

"""
Utilities for working with Bitbucket pull requests.
"""
import json
import requests

from utils import log


class PullRequest:
    """Utilities for working with Bitbucket pull requests."""
    __pull_request_settings_data__ = {'mergeConfig': {'defaultStrategy': {'id': 'no-ff'},
                                                      'strategies':
                                                      [{'id': 'no-ff',
                                                        'enabled': True}],
                                                      'type': 'REPOSITORY'},
                                      'requiredApprovers': 1, 'requiredAllApprovers': False,
                                      'requiredAllTasksComplete': True,
                                      'requiredSuccessfulBuilds': 1}

    @log
    def set_pull_request_settings_for_project(self, **kwargs):
        """Sets standard pull request settings for a repo."""
        bitbucket = kwargs.get('bitbucket')
        url = f"http://{bitbucket.get('host')}/rest/api/1.0"
        url += f"/projects/{bitbucket.get('project')}/settings/pull-requests/git"
        return requests.request('POST', url, headers=kwargs.get(
            'default_headers'), json=self.__pull_request_settings_data__)

    @log
    def set_pull_request_settings(self, **kwargs):
        """Sets standard pull request settings for a repo."""
        bitbucket = kwargs.get('bitbucket')
        url = f"http://{bitbucket.get('host')}/rest/api/1.0"
        url += f"/projects/{bitbucket.get('project')}"
        url += f"/repos/{bitbucket.get('repo')}/settings/pull-requests"
        return requests.request('POST', url, headers=kwargs.get(
            'default_headers'), json=self.__pull_request_settings_data__)

    def get_my_pull_requests(self, **kwargs):
        """Gets a list of pull requests for the current user."""
        bitbucket = kwargs.get('bitbucket')
        url = f"http://{bitbucket.get('host')}/rest/api/1.0/inbox/pull-requests?limit=100"
        return requests.request('GET', url, headers=kwargs.get(
            'default_headers'))

    @log
    def update_pull_request_status(self, json_input, **kwargs):
        """Updates a pull request status to APPROVED, DECLINED, etc."""
        bitbucket = kwargs.get('bitbucket')
        parameters = json.loads(json_input)
        from_ref = parameters['fromRef']
        to_ref = parameters['toRef']
        status = parameters['status']
        pull_request = self._get_pull_request_for_refs(from_ref, to_ref, **kwargs)

        if pull_request is None:
            print(
                f"No applicable pull request found to update in repo {bitbucket.get('repo')}.")
        else:
            url = f"http://{bitbucket.get('host')}/rest/api/1.0/projects/"
            url += f"{bitbucket.get('project')}/repos/{bitbucket.get('repo')}/"
            url += f"pull-requests/{pull_request['id']}/participants/{kwargs.get('username')}"
            # print(f"Would have executed: {url} with status {status}")
            return requests.request('PUT', url, headers=kwargs.get(
                'default_headers'), json={'status': status})

    @log
    def merge_pull_request(self, json_input, **kwargs):
        """Merges a pull request."""
        bitbucket = kwargs.get('bitbucket')
        parameters = json.loads(json_input)
        from_ref = parameters['fromRef']
        to_ref = parameters['toRef']
        pull_request = self._get_pull_request_for_refs(from_ref, to_ref, **kwargs)

        if pull_request is None:
            print(
                f"No applicable pull request found to merge in repo {bitbucket.get('repo')}.")
        else:
            url = f"http://{bitbucket.get('host')}/rest/api/1.0/projects/"
            url += f"{bitbucket.get('project')}/repos/{bitbucket.get('repo')}/"
            url += f"pull-requests/{pull_request['id']}/merge"

            headers = kwargs.get('default_headers')
            headers['X-Atlassian-Token'] = 'no-check'

            return requests.request('POST', url, headers=headers, json={
                'version': pull_request['version']
            })

    def _get_pull_requests(self, **kwargs):
        bitbucket = kwargs.get('bitbucket')
        url = f"http://{bitbucket.get('host')}/rest/api/1.0/projects/"
        url += f"{bitbucket.get('project')}/repos/{bitbucket.get('repo')}/pull-requests"
        api_response = requests.request('GET', url, headers=kwargs.get(
            'default_headers'))
        return json.loads(api_response.text)['values']

    def _get_pull_request_for_refs(self, from_ref, to_ref, **kwargs):
        pull_requests = self._get_pull_requests(**kwargs)

        for pull_request in pull_requests:
            if pull_request['open'] and pull_request['fromRef']['id'] == from_ref and pull_request['toRef']['id'] == to_ref:
                return pull_request

        return None
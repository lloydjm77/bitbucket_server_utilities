"""
Utilities for working with Bitbucket projects.
"""
import json
import requests

class Project:
    """Utilities for working with Bitbucket projects."""

    def get_repos(self, **kwargs):
        """Gets a list of Bitbucket repos for the given credentials and project."""
        bitbucket_config = kwargs.get('bitbucket')
        url = f"http://{bitbucket_config.get('host')}/rest/api/1.0/projects/"
        url += f"{bitbucket_config.get('project')}/repos?"
        url += f"limit={bitbucket_config.get('query_limit')}"

        api_response = requests.request("GET", url, headers=kwargs.get('default_headers'))

        data = json.loads(api_response.text)

        inclusions = kwargs.get('inclusions')
        exclusions = kwargs.get('exclusions')

        if inclusions is None or len(inclusions) is 0:
            return self._process_exclusions(data, exclusions)
        else:
            return self._process_inclusions(data, inclusions)

    def _process_inclusions(self, data, inclusions):
        repo_list = []
        for repo in data['values']:
            if repo['slug'] in inclusions:
                repo_list.append(repo)
            else:
                continue
        return repo_list

    def _process_exclusions(self, data, exclusions):
        repo_list = []
        for repo in data['values']:
            if repo['slug'] in exclusions:
                continue
            else:
                repo_list.append(repo)
        return repo_list

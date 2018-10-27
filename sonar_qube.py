"""
Utilities for configuring the Bitbucket SonarQube plugin.
"""
import requests

from utils import log


class SonarQube:
    """Utilities for configuring the Bitbucket SonarQube plugin."""
    __sonar_qube_project_data__ = {
        'project': {
            'analysisMode': 'BRANCH_DIFF',
            'showOnlyNewOrChangedLines': True,
            'illegalBranchCharReplacement': '',
            'pullRequestBranch': '',
            'projectCleanupEnabled': False,
            'forkCleanupEnabled': False
        }
    }

    __sonar_qube_repo_data__ = {
        'project': {
            'sonarEnabled': True,
            'inheritFromProject': True,
            'serverConfigId': 1,
            'masterProjectKey': '',
            'projectBaseKey': '',
            'analysisMode': 'BRANCH_DIFF'
        }
    }

    @log
    def configure_for_project(self, **kwargs):
        """Configures the SonarQube plugin for this project."""
        bitbucket = kwargs.get('bitbucket')
        data = self.__sonar_qube_project_data__
        url = f"http://{bitbucket.get('host')}/rest/sonar4stash/1.0"
        url += f"/projects/{bitbucket.get('project')}/settings"
        return requests.request(
            'POST', url, headers=kwargs.get('default_headers'), json=data)

    @log
    def configure(self, project_base_key, **kwargs):
        """Configures the SonarQube plugin for this repo."""
        bitbucket = kwargs.get('bitbucket')
        data = self.__sonar_qube_repo_data__
        key = f"{project_base_key}:{bitbucket.get('repo')}"
        data['project']['masterProjectKey'] = f"{key}:master"
        data['project']['projectBaseKey'] = key
        url = f"http://{bitbucket.get('host')}/rest/sonar4stash/1.0"
        url += f"/projects/{bitbucket.get('project')}"
        url += f"/repos/{bitbucket.get('repo')}/settings"
        return requests.request(
            'POST', url, headers=kwargs.get('default_headers'), json=data)

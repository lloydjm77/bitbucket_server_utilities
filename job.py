"""
Utilities for working with Jenkins jobs.
"""
import urllib
import requests

from utils import log

class Job:
    """Utilities for working with Jenkins jobs."""

    @log
    def create_pipeline_job(self, **kwargs):
        """Creates a pipeline job for a repo."""
        bitbucket = kwargs.get('bitbucket')
        jenkins = kwargs.get('jenkins')
        url = f"http://{jenkins.get('host')}/job/pipeline-seed-job/buildWithParameters?"
        url += f"project={bitbucket.get('repo')}&scmUrl=http://{bitbucket.get('host')}"
        url += f"/scm/{bitbucket.get('project')}/{bitbucket.get('repo')}.git"
        return requests.request(
            'POST', url, headers=kwargs.get('default_headers'))

    @log
    def delete_pipeline_job(self, **kwargs):
        """Deletes a pipeline job for a repo."""
        bitbucket = kwargs.get('bitbucket')
        jenkins = kwargs.get('jenkins')
        url = f"http://{jenkins.get('host')}/job/{bitbucket.get('repo')}-build/doDelete"
        return requests.request(
            'POST', url, headers=kwargs.get('default_headers'))

    @log
    def trigger_pipeline_job(self, **kwargs):
        """Triggers a pipeline job for a repo.  This will scan all branches for changes."""
        bitbucket = kwargs.get('bitbucket')
        jenkins = kwargs.get('jenkins')
        url = f"http://{jenkins.get('host')}/job/{bitbucket.get('repo')}-build/build"
        return requests.request(
            'POST', url, headers=kwargs.get('default_headers'))

    @log
    def trigger_pipeline_branch_job(self, branch, **kwargs):
        """Triggers a pipeline job for a single branch in a repo."""
        bitbucket = kwargs.get('bitbucket')
        jenkins = kwargs.get('jenkins')
        url = f"http://{jenkins.get('host')}/job/{bitbucket.get('repo')}-build"
        url += f"/job/{urllib.parse.quote_plus(branch)}/build"
        return requests.request(
            'POST', url, headers=kwargs.get('default_headers'))

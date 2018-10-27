"""
Utilities for managing a repo's post-receive hook.
"""
import requests

from utils import log

class PostReceiveHook:
    """Utilities for managing a repo's post-receive hook."""
    __post_receive_hook_data__ = {'version': '3', 'locationCount': '1', 'httpMethod': 'POST',
                                  'url': '', 'useAuth': 'true', 'user': 'SVC_PV_jenkins_usr_T',
                                  'pass': '@ZV28$cnEg$fi6e',
                                  'postContentType': 'application/x-www-form-urlencoded',
                                  'postData': '', 'branchFilter': '', 'tagFilter': '',
                                  'userFilter': '([BbTt][0-9]{1,7})'}

    @log
    def enable_for_project(self, **kwargs):
        """Enables the post receive hook for a project."""
        return self._handle_enable_disable_post_receive_hook_request_for_project(
            True, **kwargs)

    @log
    def disable_for_project(self, **kwargs):
        """Disables the post receive hook for a project."""
        return self._handle_enable_disable_post_receive_hook_request_for_project(
            False, **kwargs)

    @log
    def enable(self, **kwargs):
        """Enables the post receive hook for a repo."""
        return self._handle_enable_disable_post_receive_hook_request(
            True, **kwargs)

    @log
    def disable(self, **kwargs):
        """Disables the post receive hook for a repo."""
        return self._handle_enable_disable_post_receive_hook_request(
            False, **kwargs)

    @log
    def configure_for_project(self, **kwargs):
        """Configures the post-receive hook for all repos in this project."""
        bitbucket = kwargs.get('bitbucket')
        data = self.__post_receive_hook_data__
        data['url'] = 'http://' + kwargs.get('jenkins').get(
            'host') + '/job/${repository.slug}-build/build'
        url = f"http://{bitbucket.get('host')}/rest/api/1.0"
        url += f"/projects/{bitbucket.get('project')}/settings/hooks/"
        url += 'de.aeffle.stash.plugin.stash-http-get-post-receive-hook:http-get-post-receive-hook/settings'
        return requests.request(
            'PUT', url, headers=kwargs.get('default_headers'), json=data)

    @log
    def configure(self, **kwargs):
        """Configures the post-receive hook for this repo."""
        bitbucket = kwargs.get('bitbucket')
        data = self.__post_receive_hook_data__
        data['url'] = 'http://' + kwargs.get('jenkins').get(
            'host') + '/job/${repository.slug}-build/build'
        url = f"http://{bitbucket.get('host')}/rest/api/1.0"
        url += f"/projects/{bitbucket.get('project')}/repos/{bitbucket.get('repo')}"
        url += '/settings/hooks/de.aeffle.stash.plugin.stash-http-get-post-receive-hook:'
        url += 'http-get-post-receive-hook/settings'
        return requests.request(
            'PUT', url, headers=kwargs.get('default_headers'), json=data)

    def _handle_enable_disable_post_receive_hook_request_for_project(self, enable, **kwargs):
        bitbucket = kwargs.get('bitbucket')
        url = f"http://{bitbucket.get('host')}/rest/api/1.0/"
        url += f"projects/{bitbucket.get('project')}"
        url += '/settings/hooks/de.aeffle.stash.plugin.stash-http-get-post-receive-hook:'
        url += 'http-get-post-receive-hook/enabled'
        return requests.request(
            'PUT' if enable else 'DELETE', url, headers=kwargs.get('default_headers'))

    def _handle_enable_disable_post_receive_hook_request(self, enable, **kwargs):
        bitbucket = kwargs.get('bitbucket')
        url = f"http://{bitbucket.get('host')}/rest/api/1.0/"
        url += f"projects/{bitbucket.get('project')}/repos/{bitbucket.get('repo')}"
        url += '/settings/hooks/de.aeffle.stash.plugin.stash-http-get-post-receive-hook:'
        url += 'http-get-post-receive-hook/enabled'
        return requests.request(
            'PUT' if enable else 'DELETE', url, headers=kwargs.get('default_headers'))

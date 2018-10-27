"""
Driver for batch operations.
"""
import utils

from branch import Branch
from job import Job
from post_receive_hook import PostReceiveHook
from project import Project
from pull_request import PullRequest
from sonar_qube import SonarQube

class BatchDriver:
    """Driver for batch operations."""

    def __init__(self):
        self.branch = Branch()
        self.job = Job()
        self.post_receive_hook = PostReceiveHook()
        self.project = Project()
        self.pull_request = PullRequest()
        self.sonar_qube = SonarQube()

        self.__project_ops__ = {
            'branch:set_default_permissions_for_project': self.branch.set_default_permissions_for_project,
            'post_receive_hook:configure_for_project': self.post_receive_hook.configure_for_project,
            'post_receive_hook:disable_for_project': self.post_receive_hook.disable_for_project,
            'post_receive_hook:enable_for_project': self.post_receive_hook.enable_for_project,
            'project:get_repos': self.project.get_repos,
            'pull_request:get_my_pull_requests': self.pull_request.get_my_pull_requests,
            'pull_request:set_pull_request_settings_for_project': self.pull_request.set_pull_request_settings_for_project,
            'sonar_qube:configure_for_project': self.sonar_qube.configure_for_project
        }

        self.__ops__ = {
            'branch:list_branches': self.branch.list_branches,
            'branch:create_branch': self.branch.create_branch,
            'branch:delete_branch': self.branch.delete_branch,
            'branch:set_default_permissions': self.branch.set_default_permissions,
            'branch:set_default_branch': self.branch.set_default_branch,
            'job:create_pipeline_job': self.job.create_pipeline_job,
            'job:delete_pipeline_job': self.job.delete_pipeline_job,
            'job:trigger_pipeline_branch_job': self.job.trigger_pipeline_branch_job,
            'job:trigger_pipeline_job': self.job.trigger_pipeline_job,
            'post_receive_hook:configure': self.post_receive_hook.configure,
            'post_receive_hook:disable': self.post_receive_hook.disable,
            'post_receive_hook:enable': self.post_receive_hook.enable,
            'pull_request:merge_pull_request': self.pull_request.merge_pull_request,
            'pull_request:set_pull_request_settings': self.pull_request.set_pull_request_settings,
            'pull_request:update_pull_request_status': self.pull_request.update_pull_request_status,
            'sonar_qube:configure': self.sonar_qube.configure
        }


    def run_batch(self):
        config = utils.parse_config()
        bitbucket = config.get('bitbucket')
        operations = config.get('operations')
        project_operations = config.get('project-operations')

        self._exec_ops(project_operations, self.__project_ops__, **config)

        for repo in self.project.get_repos(**config):
            bitbucket['repo'] = repo.get('slug')
            self._exec_ops(operations, self.__ops__, **config)


    def _exec_ops(self, ops, available_ops, **config):
        if ops is not None:
            for operation in ops:
                parsed_operation = operation.split('<=')
                func = available_ops.get(parsed_operation[0])

                if len(parsed_operation) > 1:
                    func(parsed_operation[1], **config)
                else:
                    func(**config)


if __name__ == '__main__':
    BatchDriver().run_batch()

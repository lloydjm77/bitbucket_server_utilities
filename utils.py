"""
General utilities for working with Bitbucket repos.
"""

import argparse
import base64
import os
import sys

import yaml

__bitbucket_host__ = 'bitbucket.jlloyd.io'
__bitbucket_query_limit__ = 1000
__username_variable__ = 'SCRIPT_USERNAME'
__password_variable__ = 'SCRIPT_PASSWORD'

def parse_config():
    """Parse the yaml config."""

    parser = argparse.ArgumentParser(
        description='Utilities for managing build pipelines and source code repos.')
    parser.add_argument('-f', '--file', required=True,
                        help='The yaml file containing arg info for running the script.')
    command_line_arguments = parser.parse_args(sys.argv[1:])

    stream = open(command_line_arguments.file, 'r')

    config = yaml.load(stream)

    bitbucket = config.get('bitbucket')
    bitbucket.setdefault('host', __bitbucket_host__)
    bitbucket.setdefault('query_limit', __bitbucket_query_limit__)

    username = os.environ[config.get('username_variable', __username_variable__)]
    password = os.environ[config.get('password_variable', __password_variable__)]

    config.setdefault('username', username)
    config.setdefault('exclusions', [])
    config.setdefault('inclusions', [])
    config['default_headers'] = _default_headers(username, password)

    return config


def log(function):
    """Decorator function used to log calls."""

    def logger(*args, **kwargs):
        """Outputs the function call info."""

        result = function(*args, **kwargs)
        if result is not None:
            bitbucket = kwargs.get('bitbucket')
            message = f"{bitbucket.get('project')}/{bitbucket.get('repo')}: "
            message += f"{function.__module__}:{function.__name__} => {result}"
            if not isinstance(result, list) and not result.ok:
                message += ": " + result.text
            print(message)

    return logger


def _default_headers(username, password):
    """Creates a headers dict containing the Authorization header."""
    basic = base64.encodebytes(bytes(f'{username}:{password}', 'utf-8'))
    basic_decoded = basic.decode('utf-8').replace('\n', '')
    return {
        'Authorization': f'Basic {basic_decoded}'
    }

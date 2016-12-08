#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.utils import is_valid_string, filter_model


class GitRepoVolumeSource(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_gitrepovolumesource
    """

    def __init__(self, model=None):
        super(GitRepoVolumeSource, self).__init__()

        self._repository = None
        self._revision = None
        self._directory = None

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def _build_with_model(self, model=None):
        if 'repository' in model:
            self.repository = model['repository']
        if 'revision' in model:
            self.revision = model['revision']
        if 'directory' in model:
            self.directory = model['directory']

    # ------------------------------------------------------------------------------------- repository

    @property
    def repository(self):
        return self._repository

    @repository.setter
    def repository(self, repo=None):
        if not is_valid_string(repo):
            raise SyntaxError('GitRepoVolumeSource: repository: [ {0} ] is invalid.'.format(repo))
        self._repository = repo

    # ------------------------------------------------------------------------------------- revision

    @property
    def revision(self):
        return self._revision

    @revision.setter
    def revision(self, revision=None):
        if not is_valid_string(revision):
            raise SyntaxError('GitRepoVolumeSource: revision: [ {0} ] is invalid.'.format(revision))
        self._revision = revision

    # ------------------------------------------------------------------------------------- directory

    @property
    def directory(self):
        return self._directory

    @directory.setter
    def directory(self, directory=None):
        if not is_valid_string(directory):
            raise SyntaxError('GitRepoVolumeSource: directory: [ {0} ] is invalid.'.format(directory))
        self._directory = directory

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.repository is not None:
            data['repository'] = self.repository
        if self.revision is not None:
            data['revision'] = self.revision
        if self.directory is not None:
            data['directory'] = self.directory
        return data

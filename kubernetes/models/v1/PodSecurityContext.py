#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.utils import is_valid_list, filter_model


class PodSecurityContext(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_podsecuritycontext
    """

    def __init__(self, model=None):
        super(PodSecurityContext, self).__init__()

        # TODO(froch): add support for the below
        # self.se_linux_options = None

        self._fs_group = None
        self._run_as_non_root = None
        self._run_as_user = None
        self._supplemental_groups = None

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def _build_with_model(self, model=None):
        if 'fsGroup' in model:
            self.fs_group = model['fsGroup']
        if 'runAsNonRoot' in model:
            self.run_as_non_root = model['runAsNonRoot']
        if 'runAsUser' in model:
            self.run_as_user = model['runAsUser']
        if 'supplementalGroups' in model:
            self.supplemental_groups = model['supplementalGroups']

    # ------------------------------------------------------------------------------------- fs group

    @property
    def fs_group(self):
        return self._supplemental_groups

    @fs_group.setter
    def fs_group(self, gid=None):
        if not isinstance(gid, int):
            raise SyntaxError('PodSecurityContext: fs_group: [ {0} ] is invalid.'.format(gid))
        self._fs_group = gid

    # ------------------------------------------------------------------------------------- run as non root

    @property
    def run_as_non_root(self):
        return self._run_as_non_root

    @run_as_non_root.setter
    def run_as_non_root(self, b=None):
        if not isinstance(b, bool):
            raise SyntaxError('PodSecurityContext: run_as_non_root: [ {0} ] is invalid.'.format(b))
        self._run_as_non_root = b

    # ------------------------------------------------------------------------------------- run as user

    @property
    def run_as_user(self):
        return self._run_as_user

    @run_as_user.setter
    def run_as_user(self, uid=None):
        if not isinstance(uid, int):
            raise SyntaxError('PodSecurityContext: run_as_user: [ {0} ] is invalid.'.format(uid))
        self._run_as_user = uid

    # ------------------------------------------------------------------------------------- supplemental groups

    @property
    def supplemental_groups(self):
        return self._supplemental_groups

    @supplemental_groups.setter
    def supplemental_groups(self, gids=None):
        if not is_valid_list(gids, int):
            raise SyntaxError('PodSecurityContext: supplemental_groups: [ {0} ] is invalid.'.format(gids))
        self._supplemental_groups = gids

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.fs_group is not None:
            data['fsGroup'] = self.fs_group
        if self.run_as_non_root is not None:
            data['runAsNonRoot'] = self.run_as_non_root
        if self.run_as_user is not None:
            data['runAsUser'] = self.run_as_user
        if self.supplemental_groups is not None:
            data['supplementalGroups'] = self.supplemental_groups
        return data

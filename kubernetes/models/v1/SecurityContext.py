#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.Capabilities import Capabilities
from kubernetes.models.v1.SELinuxOptions import SELinuxOptions
from kubernetes.utils import filter_model


class SecurityContext(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_securitycontext
    """

    def __init__(self, model=None):
        super(SecurityContext, self).__init__()

        self._capabilities = None
        self._privileged = False
        self._read_only_root_filesystem = False
        self._run_as_non_root = False
        self._run_as_user = None
        self._se_linux_options = None

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def _build_with_model(self, model=None):
        if 'capabilities' in model:
            self.capabilities = Capabilities(model['capabilities'])
        if 'privileged' in model:
            self.privileged = model['privileged']
        if 'readOnlyRootFilesystem' in model:
            self.read_only_root_filesystem = model['readOnlyRootFilesystem']
        if 'runAsNonRoot' in model:
            self.run_as_non_root = model['runAsNonRoot']
        if 'runAsUser' in model:
            self.run_as_user = model['runAsUser']

    # ------------------------------------------------------------------------------------- capabilities

    @property
    def capabilities(self):
        return self._capabilities

    @capabilities.setter
    def capabilities(self, c=None):
        if not isinstance(c, Capabilities):
            raise SyntaxError('SecurityContext: capabilities: [ {} ] is invalid.'.format(c))
        self._capabilities = c

    # ------------------------------------------------------------------------------------- privileged

    @property
    def privileged(self):
        return self._privileged

    @privileged.setter
    def privileged(self, p=None):
        if not isinstance(p, bool):
            raise SyntaxError('SecurityContext: privileged: [ {} ] is invalid.'.format(p))
        self._privileged = p

    # ------------------------------------------------------------------------------------- readOnlyRootFilesystem

    @property
    def read_only_root_filesystem(self):
        return self._read_only_root_filesystem

    @read_only_root_filesystem.setter
    def read_only_root_filesystem(self, r=None):
        if not isinstance(r, bool):
            raise SyntaxError('SecurityContext: read_only_root_filesystem: [ {} ] is invalid.'.format(r))
        self._read_only_root_filesystem = r

    # ------------------------------------------------------------------------------------- runAsNonRoot

    # May also be set in PodSecurityContext.
    # If set in both SecurityContext and PodSecurityContext, the value specified in SecurityContext takes precedence.

    @property
    def run_as_non_root(self):
        return self._run_as_non_root

    @run_as_non_root.setter
    def run_as_non_root(self, r=None):
        if not isinstance(r, bool):
            raise SyntaxError('SecurityContext: run_as_non_root: [ {} ] is invalid.'.format(r))
        self._run_as_non_root = r

    # ------------------------------------------------------------------------------------- runAsUser

    # May also be set in PodSecurityContext.
    # If set in both SecurityContext and PodSecurityContext, the value specified in SecurityContext takes precedence.

    @property
    def run_as_user(self):
        return self._run_as_user

    @run_as_user.setter
    def run_as_user(self, r=None):
        if not isinstance(r, int):
            raise SyntaxError('SecurityContext: run_as_user: [ {} ] is invalid.'.format(r))
        self._run_as_user = r

    # ------------------------------------------------------------------------------------- seLinuxOptions

    # May also be set in PodSecurityContext.
    # If set in both SecurityContext and PodSecurityContext, the value specified in SecurityContext takes precedence.

    @property
    def se_linux_options(self):
        return self._se_linux_options

    @se_linux_options.setter
    def se_linux_options(self, o=None):
        if not isinstance(o, SELinuxOptions):
            raise SyntaxError('SecurityContext: se_linux_options: [ {} ] is invalid.'.format(o))
        self._se_linux_options = o

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.capabilities is not None:
            data['capabilities'] = self.capabilities.serialize()
        if self.privileged is not None:
            data['privileged'] = self.privileged
        if self.read_only_root_filesystem is not None:
            data['readOnlyRootFilesystem'] = self.read_only_root_filesystem
        if self.run_as_non_root is not None:
            data['runAsNonRoot'] = self.run_as_non_root
        if self.run_as_user is not None:
            data['runAsUser'] = self.run_as_user
        if self.se_linux_options is not None:
            data['seLinuxOptions'] = self.se_linux_options.serialize()
        return data


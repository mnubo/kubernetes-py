#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.utils import filter_model


class SecurityContext(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_securitycontext
    """

    def __init__(self, model=None):
        super(SecurityContext, self).__init__()

        # TODO(froch): add support for the below.
        # self.capabilities = None
        # self.se_linux_options = None

        self.privileged = False
        self.run_as_user = None
        self.run_as_non_root = False
        self.read_only_root_file_system = False

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def _build_with_model(self, model=None):
        pass

    # ------------------------------------------------------------------------------------- serialize

    def json(self):
        data = {}
        if self.privileged is not None:
            data['privileged'] = self.privileged
        if self.run_as_user is not None:
            data['runAsUser'] = self.run_as_user
        if self.run_as_non_root is not None:
            data['runAsNonRoot'] = self.run_as_non_root
        if self.read_only_root_file_system is not None:
            data['readOnlyRootFilesystem'] = self.read_only_root_file_system
        return data

#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.utils import is_valid_string


class SELinuxOptions(object):
    """
    https://kubernetes.io/docs/api-reference/v1.6/#selinuxoptions-v1-core
    """

    def __init__(self, model=None):
        super(SELinuxOptions, self).__init__()

        self._level = None
        self._role = None
        self._type = None
        self._user = None

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'level' in model:
            self.level = model['level']
        if 'role' in model:
            self.role = model['role']
        if 'type' in model:
            self.type = model['type']
        if 'user' in model:
            self.user = model['user']

    # ------------------------------------------------------------------------------------- level

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, l=None):
        if not is_valid_string(l):
            raise SyntaxError('SELinuxOptions: level: [ {} ] is invalid.'.format(l))
        self._level = l

    # ------------------------------------------------------------------------------------- role

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, r=None):
        if not is_valid_string(r):
            raise SyntaxError('SELinuxOptions: role: [ {} ] is invalid.'.format(r))
        self._role = r

    # ------------------------------------------------------------------------------------- type

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, t=None):
        if not is_valid_string(t):
            raise SyntaxError('SELinuxOptions: type: [ {} ] is invalid.'.format(t))
        self._level = t

    # ------------------------------------------------------------------------------------- user

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, u=None):
        if not is_valid_string(u):
            raise SyntaxError('SELinuxOptions: user: [ {} ] is invalid.'.format(u))
        self._user = u

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.level is not None:
            data['level'] = self.level
        if self.role is not None:
            data['role'] = self.role
        if self.type is not None:
            data['type'] = self.type
        if self.user is not None:
            data['user'] = self.user
        return data

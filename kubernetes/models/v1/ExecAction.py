#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.utils import is_valid_list


class ExecAction(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_execaction
    """

    def __init__(self):
        super(ExecAction, self).__init__()
        self._command = []

    @property
    def command(self):
        return self._command

    @command.setter
    def command(self, command=None):
        if not is_valid_list(command, str):
            raise SyntaxError('ExecAction: command: [ {0} ] is invalid.'.format(command))
        self._command = command

    def json(self):
        return {'command': self.command}


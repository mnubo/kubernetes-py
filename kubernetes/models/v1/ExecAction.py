#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.BaseModel import BaseModel


class ExecAction(BaseModel):

    def __init__(self):
        super(ExecAction, self).__init__()
        self._command = []

    @property
    def command(self):
        return self._command

    @command.setter
    def command(self, command=None):
        msg = 'ExecAction: command: [ {0} ] is invalid.'.format(command)
        if not isinstance(command, list):
            raise SyntaxError(msg)
        for x in command:
            if not isinstance(x, str):
                raise SyntaxError(msg)
        self._command = command

    def json(self):
        return {'command': self.command}

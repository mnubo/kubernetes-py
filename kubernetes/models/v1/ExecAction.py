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

    def __init__(self, model=None):
        super(ExecAction, self).__init__()

        self._command = []

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'command' in model:
            self.command = model['command']

    # ------------------------------------------------------------------------------------- command

    @property
    def command(self):
        return self._command

    @command.setter
    def command(self, command=None):
        if not is_valid_list(command, str):
            raise SyntaxError('ExecAction: command: [ {0} ] is invalid.'.format(command))
        self._command = command

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.command is not None:
            data['command'] = self.command
        return data

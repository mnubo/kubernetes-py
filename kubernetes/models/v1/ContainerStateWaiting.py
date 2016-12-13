#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.utils import is_valid_string, filter_model


class ContainerStateWaiting(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_containerstatewaiting
    """

    def __init__(self, model=None):
        super(ContainerStateWaiting, self).__init__()

        self._reason = None
        self._message = None

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def _build_with_model(self, model=None):
        if 'reason' in model:
            self.reason = model['reason']
        if 'message' in model:
            self.message = model['message']

    # ------------------------------------------------------------------------------------- reason

    @property
    def reason(self):
        return self._reason

    @reason.setter
    def reason(self, msg=None):
        if not is_valid_string(msg):
            raise SyntaxError('ContainerStateWaiting: reason: [ {0} ] is invalid.'.format(msg))
        self._reason = msg

    # ------------------------------------------------------------------------------------- message

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, msg=None):
        if not is_valid_string(msg):
            raise SyntaxError('ContainerStateWaiting: message: [ {0} ] is invalid.'.format(msg))
        self._message = msg

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.reason is not None:
            data['reason'] = self.reason
        if self.message is not None:
            data['message'] = self.message
        return data

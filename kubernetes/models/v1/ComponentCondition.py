#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#
from kubernetes.utils import filter_model


class ComponentCondition(object):
    """
    https://kubernetes.io/docs/api-reference/v1/definitions/#_v1_componentcondition
    """

    VALID_TYPE = ['Healthy']
    VALID_STATUS = ['True', 'False', 'Unknown']

    def __init__(self, model=None):
        super(ComponentCondition, self).__init__()

        self._type = None
        self._status = None
        self._message = None
        self._error = None

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def _build_with_model(self, model=None):
        if 'type' in model:
            self.type = model['type']
        if 'status' in model:
            self.status = model['status']
        if 'message' in model:
            self.message = model['message']
        if 'error' in model:
            self.error = model['error']

    # ------------------------------------------------------------------------------------- type

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, v):
        if not isinstance(v, str) or v not in self.VALID_TYPE:
            raise SyntaxError('ComponentCondition: type: [ {0} ] is invalid.'.format(v))
        self._type = v

    # ------------------------------------------------------------------------------------- status

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, v):
        if not isinstance(v, str) or v not in self.VALID_STATUS:
            raise SyntaxError('ComponentCondition: status: [ {0} ] is invalid.'.format(v))
        self._status = v

    # ------------------------------------------------------------------------------------- message

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, v):
        if not isinstance(v, str):
            raise SyntaxError('ComponentCondition: message: [ {0} ] is invalid.'.format(v))
        self._message = v

    # ------------------------------------------------------------------------------------- error

    @property
    def error(self):
        return self._error

    @error.setter
    def error(self, v):
        if not isinstance(v, str):
            raise SyntaxError('ComponentCondition: error: [ {0} ] is invalid.'.format(v))
        self._error = v

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.type:
            data['type'] = self.type
        if self.type:
            data['status'] = self.status
        if self.type:
            data['message'] = self.message
        if self.type:
            data['error'] = self.error
        return data

#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#
from kubernetes.utils import filter_model


class NodeAddress(object):
    """
    https://kubernetes.io/docs/api-reference/v1/definitions/#_v1_nodeaddress
    """

    def __init__(self, model=None):
        super(NodeAddress, self).__init__()

        self._type = None
        self._address = None

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def _build_with_model(self, model=None):
        if 'type' in model:
            self.type = model['type']
        if 'address' in model:
            self.address = model['address']

    # ------------------------------------------------------------------------------------- type

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, v):
        if not isinstance(v, str):
            raise SyntaxError('NodeAddress: type: [ {0} ] is invalid.'.format(v))
        self._type = v

    # ------------------------------------------------------------------------------------- address

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, v):
        if not isinstance(v, str):
            raise SyntaxError('NodeAddress: address: [ {0} ] is invalid.'.format(v))
        self._address = v

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.type:
            data['type'] = self.type
        if self.address:
            data['address'] = self.address
        return data

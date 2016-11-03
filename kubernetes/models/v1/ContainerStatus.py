#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.utils import is_valid_string, filter_model


class ContainerStatus(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_containerstatus
    """

    def __init__(self, model=None):
        super(ContainerStatus, self).__init__()
        self._name = None
        self._state = None
        self._last_state = None
        self._ready = False
        self._restart_count = 0
        self._image = None
        self._image_id = None
        self._container_id = None

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def _build_with_model(self, model=None):
        pass

    # ------------------------------------------------------------------------------------- name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name=None):
        if not is_valid_string(name):
            raise SyntaxError('ContainerStatus: name: [ {0} ] is invalid'.format(name))
        self._name = name
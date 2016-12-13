#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.utils import is_valid_string, filter_model


class HostPathVolumeSource(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_hostpathvolumesource
    """

    def __init__(self, model=None):
        super(HostPathVolumeSource, self).__init__()

        self._path = None

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def _build_with_model(self, model=None):
        if 'path' in model:
            self.path = model['path']

    # ------------------------------------------------------------------------------------- path

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path=None):
        if not is_valid_string(path):
            raise SyntaxError('HostPathVolumeSource: path: [ {0} ] is invalid.'.format(path))
        self._path = path

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.path is not None:
            data['path'] = self.path
        return data

#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.utils import filter_model


class EmptyDirVolumeSource(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_emptydirvolumesource
    """

    VALID_MEDIA = ['', 'Memory']

    def __init__(self, model=None):
        super(EmptyDirVolumeSource, self).__init__()

        self._medium = None

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def _build_with_model(self, model=None):
        if 'medium' in model:
            self.medium = model['medium']

    # ------------------------------------------------------------------------------------- medium

    @property
    def medium(self):
        return self._medium

    @medium.setter
    def medium(self, medium=None):
        if medium is None or medium not in EmptyDirVolumeSource.VALID_MEDIA:
            raise SyntaxError('EmptyDirVolumeSource: medium: [ {0} ] is invalid.'.format(medium))
        self._medium = medium

    # ------------------------------------------------------------------------------------- medium

    def serialize(self):
        data = {}
        if self.medium is not None:
            data['medium'] = self.medium
        return data

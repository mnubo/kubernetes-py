#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1 import (
    ObjectMeta,
    PodSpec
)


class PodTemplateSpec(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_podtemplatespec
    """

    def __init__(self):
        super(PodTemplateSpec, self).__init__()

        self._metadata = None
        self._spec = None

    # ------------------------------------------------------------------------------------- metadata

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, metadata=None):
        if not isinstance(metadata, ObjectMeta):
            raise SyntaxError('PodTemplateSpec: metadata: [ {0} ] is invalid'.format(metadata))
        self._metadata = metadata

    # ------------------------------------------------------------------------------------- spec

    @property
    def spec(self):
        return self._spec

    @spec.setter
    def spec(self, spec=None):
        if not isinstance(spec, PodSpec):
            raise SyntaxError('PodTemplateSpec: spec: [ {0} ] is invalid'.format(spec))
        self._spec = spec

    # ------------------------------------------------------------------------------------- serialize

    def json(self):
        data = {}
        if self.metadata is not None:
            data['metadata'] = self.metadata.json()
        if self.spec is not None:
            data['spec'] = self.spec.json()
        return data

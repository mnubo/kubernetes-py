#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.JobSpec import JobSpec
from kubernetes.models.v1.ObjectMeta import ObjectMeta


class CronJobTemplate(object):

    def __init__(self, model=None):
        super(CronJobTemplate, self).__init__()

        self._metadata = ObjectMeta()
        self._spec = JobSpec()

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'metadata' in model:
            self.metadata = ObjectMeta(model['metadata'])
        if 'spec' in model:
            self.spec = JobSpec(model['spec'])

    # ------------------------------------------------------------------------------------- metadata

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, meta=None):
        if not isinstance(meta, ObjectMeta):
            raise SyntaxError('CronJobTemplate: metadata: [ {} ] is invalid.'.format(meta))
        self._metadata = meta

    # ------------------------------------------------------------------------------------- spec

    @property
    def spec(self):
        return self._spec

    @spec.setter
    def spec(self, spec=None):
        if not isinstance(spec, JobSpec):
            raise SyntaxError('CronJobTemplate: spec: [ {} ] is invalid.'.format(spec))
        self._spec = spec

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.metadata is not None:
            data['metadata'] = self.metadata.serialize()
        if self.spec is not None:
            data['spec'] = self.spec.serialize()
        return data

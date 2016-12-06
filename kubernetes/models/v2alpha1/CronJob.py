#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.ObjectMeta import ObjectMeta
from kubernetes.models.v2alpha1.CronJobSpec import CronJobSpec
from kubernetes.models.v2alpha1.CronJobStatus import CronJobStatus
from kubernetes.utils import is_valid_string


class CronJob(object):
    """
    http://kubernetes.io/docs/user-guide/cron-jobs/#creating-a-cron-job
    """

    def __init__(self, model=None):
        super(CronJob, self).__init__()

        self._kind = 'CronJob'
        self._api_version = "batch/v2alpha1"
        self._metadata = None
        self._spec = None
        self._status = None

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'apiVersion' in model:
            self.api_version = model['apiVersion']
        if 'kind' in model:
            self.kind = model['kind']
        if 'metadata' in model:
            self.metadata = ObjectMeta(model=model['metadata'])
        if 'spec' in model:
            self.spec = CronJobSpec(model=model['spec'])
        if 'status' in model:
            self.status = CronJobStatus(model=model['status'])

    # ------------------------------------------------------------------------------------- apiVersion

    @property
    def api_version(self):
        return self._api_version

    @api_version.setter
    def api_version(self, v=None):
        if not is_valid_string(v):
            raise SyntaxError('CronJob: api_version: [ {} ] is invalid.'.format(v))
        self._api_version = v

    # ------------------------------------------------------------------------------------- kind

    @property
    def kind(self):
        return self._kind

    @kind.setter
    def kind(self, k=None):
        if not is_valid_string(k):
            raise SyntaxError('CronJob: kind: [ {} ] is invalid.'.format(k))
        self._kind = k

    # ------------------------------------------------------------------------------------- metadata

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, meta=None):
        if not isinstance(meta, ObjectMeta):
            raise SyntaxError('CronJob: metadata: [ {} ] is invalid.'.format(meta))
        self._metadata = meta

    # ------------------------------------------------------------------------------------- spec

    @property
    def spec(self):
        return self._spec

    @spec.setter
    def spec(self, spec=None):
        if not isinstance(spec, CronJobSpec):
            raise SyntaxError('CronJob: spec: [ {} ] is invalid.'.format(spec))
        self._spec = spec

    # ------------------------------------------------------------------------------------- status

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status=None):
        if not isinstance(status, CronJobStatus):
            raise SyntaxError('CronJob: status: [ {} ] is invalid.'.format(status))
        self._status = status

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.api_version is not None:
            data['apiVersion'] = self.api_version
        if self.kind is not None:
            data['kind'] = self.kind
        if self.metadata is not None:
            data['metadata'] = self.metadata.serialize()
        if self.spec is not None:
            data['spec'] = self.spec.serialize()
        if self.status is not None:
            data['status'] = self.status.serialize()
        return data

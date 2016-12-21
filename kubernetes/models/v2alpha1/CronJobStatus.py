#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.ObjectReference import ObjectReference
from kubernetes.utils import is_valid_list, is_valid_string


class CronJobStatus(object):

    def __init__(self, model=None):
        super(CronJobStatus, self).__init__()

        self._active = []
        self._successful = None
        self._failed = None
        self._last_schedule_time = None

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'active' in model:
            refs = []
            for j in model['active']:
                ref = ObjectReference(j)
                refs.append(ref)
            self.active = refs
        if 'successful' in model:
            self.successful = model['successful']
        if 'failed' in model:
            self.failed = model['failed']
        if 'lastScheduleTime' in model:
            self.last_schedule_time = model['lastScheduleTime']

    # -------------------------------------------------------------------------------------  active

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, _list=None):
        if not is_valid_list(_list, ObjectReference):
            raise SyntaxError('CronJobStatus: active: [ {} ] is invalid.'.format(_list))
        self._active = _list

    # -------------------------------------------------------------------------------------  successful

    @property
    def successful(self):
        return self._successful

    @successful.setter
    def successful(self, s=None):
        if not isinstance(s, bool):
            raise SyntaxError('CronJobStatus: successful: [ {} ] is invalid.'.format(s))
        self._successful = s

    # -------------------------------------------------------------------------------------  failed

    @property
    def failed(self):
        return self._failed

    @failed.setter
    def failed(self, f=None):
        if not isinstance(f, bool):
            raise SyntaxError('CronJobStatus: failed: [ {} ] is invalid.'.format(f))
        self._failed = f

    # -------------------------------------------------------------------------------------  lastScheduleTime

    @property
    def last_schedule_time(self):
        return self._last_schedule_time

    @last_schedule_time.setter
    def last_schedule_time(self, t=None):
        if not is_valid_string(t):
            raise SyntaxError('CronJobStatus: last_schedule_time: [ {} ] is invalid.'.format(t))
        self._last_schedule_time = t

    # -------------------------------------------------------------------------------------  serialize

    def serialize(self):
        data = {}
        if self.active is not None:
            data['active'] = [x.serialize() for x in self.active]
        if self.successful is not None:
            data['successful'] = self.successful
        if self.failed is not None:
            data['failed'] = self.failed
        if self.last_schedule_time is not None:
            data['lastScheduleTime'] = self.last_schedule_time
        return data

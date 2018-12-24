#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#


class DaemonSetStatus(object):

    def __init__(self, model=None):
        super(DaemonSetStatus, self).__init__()

        self._current_number_scheduled = None
        self._number_misscheduled = None
        self._desired_number_scheduled = None

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'currentNumberScheduled' in model:
            self.current_number_scheduled = model['currentNumberScheduled']
        if 'numberMisscheduled' in model:
            self.number_misscheduled = model['numberMisscheduled']
        if 'desiredNumberScheduled' in model:
            self.desired_number_scheduled = model['desiredNumberScheduled']

    # ------------------------------------------------------------------------------------- currentNumberScheduled

    @property
    def current_number_scheduled(self):
        return self._current_number_scheduled

    @current_number_scheduled.setter
    def current_number_scheduled(self, n=None):
        if not isinstance(n, int):
            raise SyntaxError('DaemonSetStatus: current_number_scheduled: [ {} ] is invalid.'.format(n))
        self._current_number_scheduled = n

    # ------------------------------------------------------------------------------------- numberMisscheduled

    @property
    def number_misscheduled(self):
        return self._number_misscheduled

    @number_misscheduled.setter
    def number_misscheduled(self, n=None):
        if not isinstance(n, int):
            raise SyntaxError('DaemonSetStatus: number_misscheduled: [ {} ] is invalid.'.format(n))
        self._number_misscheduled = n

    # ------------------------------------------------------------------------------------- desiredNumberScheduled

    @property
    def desired_number_scheduled(self):
        return self._desired_number_scheduled

    @desired_number_scheduled.setter
    def desired_number_scheduled(self, n=None):
        if not isinstance(n, int):
            raise SyntaxError('DaemonSetStatus: desired_number_scheduled: [ {} ] is invalid.'.format(n))
        self._desired_number_scheduled = n

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.current_number_scheduled is not None:
            data['currentNumberScheduled'] = self.current_number_scheduled
        if self.number_misscheduled is not None:
            data['numberMisscheduled'] = self.number_misscheduled
        if self.desired_number_scheduled is not None:
            data['desiredNumberScheduled'] = self.desired_number_scheduled
        return data

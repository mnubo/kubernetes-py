#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.utils import is_valid_string, filter_model


class ContainerStateTerminated(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_containerstateterminated
    """

    def __init__(self, model=None):
        super(ContainerStateTerminated, self).__init__()

        self._exit_code = None
        self._signal = None
        self._reason = None
        self._message = None
        self._started_at = None
        self._finished_at = None
        self._container_id = None

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def _build_with_model(self, model=None):
        if 'exitCode' in model:
            self.exit_code = model['exitCode']
        if 'signal' in model:
            self.signal = model['signal']
        if 'reason' in model:
            self.reason = model['reason']
        if 'message' in model:
            self.message = model['message']
        if 'startedAt' in model:
            self.started_at = model['startedAt']
        if 'finishedAt' in model:
            self.finished_at = model['finishedAt']
        if 'containerID' in model:
            self.container_id = model['containerID']

    # ------------------------------------------------------------------------------------- exit code

    @property
    def exit_code(self):
        return self._exit_code

    @exit_code.setter
    def exit_code(self, code=None):
        if not isinstance(code, int):
            raise SyntaxError('ContainerStateTerminated: exit_code: [ {0} ] is invalid.'.format(code))
        self._exit_code = code

    # ------------------------------------------------------------------------------------- signal

    @property
    def signal(self):
        return self._signal

    @signal.setter
    def signal(self, signal=None):
        if not isinstance(signal, int):
            raise SyntaxError('ContainerStateTerminated: signal: [ {0} ] is invalid.'.format(signal))
        self._signal = signal

    # ------------------------------------------------------------------------------------- reason

    @property
    def reason(self):
        return self._reason

    @reason.setter
    def reason(self, msg=None):
        if not is_valid_string(msg):
            raise SyntaxError('ContainerStateTerminated: reason: [ {0} ] is invalid.'.format(msg))
        self._reason = msg

    # ------------------------------------------------------------------------------------- message

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, msg=None):
        if not is_valid_string(msg):
            raise SyntaxError('ContainerStateTerminated: message: [ {0} ] is invalid.'.format(msg))
        self._message = msg

    # ------------------------------------------------------------------------------------- started at

    @property
    def started_at(self):
        return self._started_at

    @started_at.setter
    def started_at(self, time=None):
        if not is_valid_string(time):
            raise SyntaxError('ContainerStateTerminated: started_at: [ {0} ] is invalid.'.format(time))
        self._started_at = time

    # ------------------------------------------------------------------------------------- finished at

    @property
    def finished_at(self):
        return self._finished_at

    @finished_at.setter
    def finished_at(self, time=None):
        if not is_valid_string(time):
            raise SyntaxError('ContainerStateTerminated: finished_at: [ {0} ] is invalid.'.format(time))
        self._finished_at = time

    # ------------------------------------------------------------------------------------- containerID

    @property
    def container_id(self):
        return self._container_id

    @container_id.setter
    def container_id(self, cid=None):
        if not is_valid_string(cid):
            raise SyntaxError('ContainerStateTerminated: container_id: [ {0} ] is invalid.'.format(cid))
        self._container_id = cid

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.exit_code is not None:
            data['exitCode'] = self.exit_code
        if self.signal is not None:
            data['signal'] = self.signal
        if self.reason is not None:
            data['reason'] = self.reason
        if self.message is not None:
            data['message'] = self.message
        if self.started_at is not None:
            data['startedAt'] = self.started_at
        if self.finished_at is not None:
            data['finishedAt'] = self.finished_at
        if self.container_id is not None:
            data['containerID'] = self.container_id
        return data

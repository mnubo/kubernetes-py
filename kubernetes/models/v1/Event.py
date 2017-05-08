#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.unversioned.BaseModel import BaseModel
from kubernetes.models.v1.EventSource import EventSource
from kubernetes.models.v1.ObjectReference import ObjectReference
from kubernetes.utils import is_valid_date_time, is_valid_string


class Event(BaseModel):
    """
    https://kubernetes.io/docs/api-reference/v1.5/#event-v1
    """

    def __init__(self, model=None):
        super(Event, self).__init__(model=model)

        self._count = None
        self._first_timestamp = None
        self._involved_object = ObjectReference()
        self._last_timestamp = None
        self._message = None
        self._reason = None
        self._source = EventSource()
        self._type = None

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        super(Event, self).build_with_model(model)

        if 'count' in model:
            self.count = model['count']
        if 'firstTimestamp' in model:
            self.first_timestamp = model['firstTimestamp']
        if 'involvedObject' in model:
            self.involved_object = ObjectReference(model['involvedObject'])
        if 'lastTimestamp' in model:
            self.last_timestamp = model['lastTimestamp']
        if 'message' in model:
            self.message = model['message']
        if 'reason' in model:
            self.reason = model['reason']
        if 'source' in model:
            self.source = EventSource(model['source'])
        if 'type' in model:
            self.type = model['type']

    # ------------------------------------------------------------------------------------- count

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, c=None):
        if not isinstance(c, int):
            raise SyntaxError("Event: count: [ {} ] is invalid.".format(c))
        self._count = c

    # ------------------------------------------------------------------------------------- firstTimestamp

    @property
    def first_timestamp(self):
        return self._first_timestamp

    @first_timestamp.setter
    def first_timestamp(self, t=None):
        if not is_valid_date_time(t):
            raise SyntaxError("Event: first_timestamp: [ {} ] is invalid.".format(t))
        self._first_timestamp = t

    # ------------------------------------------------------------------------------------- involvedObject

    @property
    def involved_object(self):
        return self._involved_object

    @involved_object.setter
    def involved_object(self, o=None):
        if not isinstance(o, ObjectReference):
            raise SyntaxError("Event: involved_object: [ {} ] is invalid.".format(o))
        self._involved_object = o

    # ------------------------------------------------------------------------------------- lastTimestamp

    @property
    def last_timestamp(self):
        return self._last_timestamp

    @last_timestamp.setter
    def last_timestamp(self, t=None):
        if not is_valid_date_time(t):
            raise SyntaxError("Event: last_timestamp: [ {} ] is invalid.".format(t))
        self._last_timestamp = t

    # ------------------------------------------------------------------------------------- message

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, m=None):
        if not is_valid_string(m):
            raise SyntaxError("Event: message: [ {} ] is invalid.".format(m))
        self._message = m

    # ------------------------------------------------------------------------------------- reason

    @property
    def reason(self):
        return self._reason

    @reason.setter
    def reason(self, r=None):
        if not is_valid_string(r):
            raise SyntaxError("Event: reason: [ {} ] is invalid.".format(r))
        self._reason = r

    # ------------------------------------------------------------------------------------- source

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, s=None):
        if not isinstance(s, EventSource):
            raise SyntaxError("Event: source: [ {} ] is invalid.".format(s))
        self._source = s

    # ------------------------------------------------------------------------------------- type

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, t=None):
        if not is_valid_string(t):
            raise SyntaxError("Event: type: [ {} ] is invalid.".format(t))
        self._type = t

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = super(Event, self).serialize()

        if self.count is not None:
            data['count'] = self.count
        if self.first_timestamp is not None:
            data['firstTimestamp'] = self.first_timestamp
        if self.involved_object is not None:
            data['involvedObject'] = self.involved_object.serialize()
        if self.last_timestamp is not None:
            data['lastTimestamp'] = self.last_timestamp
        if self.message is not None:
            data['message'] = self.message
        if self.reason is not None:
            data['reason'] = self.reason
        if self.source is not None:
            data['source'] = self.source.serialize()
        if self.type is not None:
            data['type'] = self.type
        return data

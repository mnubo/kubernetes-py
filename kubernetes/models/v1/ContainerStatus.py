#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.utils import is_valid_string, filter_model
from kubernetes.models.v1.ContainerState import ContainerState


class ContainerStatus(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_containerstatus
    """

    def __init__(self, model=None):
        super(ContainerStatus, self).__init__()

        self._name = None
        self._state = None
        self._last_state = None
        self._ready = None
        self._restart_count = None
        self._image = None
        self._image_id = None
        self._container_id = None

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def _build_with_model(self, model=None):
        if 'name' in model:
            self.name = model['name']
        if 'state' in model:
            self.state = ContainerState(model['state'])
        if 'lastState' in model:
            self.last_state = ContainerState(model['state'])
        if 'ready' in model:
            self.ready = model['ready']
        if 'restartCount' in model:
            self.restart_count = model['restartCount']
        if 'image' in model:
            self.image = model['image']
        if 'imageID' in model:
            self.image_id = model['imageID']
        if 'containerID' in model:
            self.container_id = model['containerID']

    # ------------------------------------------------------------------------------------- name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name=None):
        if not is_valid_string(name):
            raise SyntaxError('ContainerStatus: name: [ {0} ] is invalid'.format(name))
        self._name = name

    # ------------------------------------------------------------------------------------- state

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state=None):
        if not isinstance(state, ContainerState):
            raise SyntaxError('ContainerStatus: state: [ {0} ] is invalid'.format(state))
        self._state = state

    # ------------------------------------------------------------------------------------- lastState

    @property
    def last_state(self):
        return self._last_state

    @last_state.setter
    def last_state(self, state=None):
        if not isinstance(state, ContainerState):
            raise SyntaxError('ContainerStatus: last_state: [ {0} ] is invalid'.format(state))
        self._last_state = state

    # ------------------------------------------------------------------------------------- ready

    @property
    def ready(self):
        return self._ready

    @ready.setter
    def ready(self, ready=None):
        if not isinstance(ready, bool):
            raise SyntaxError('ContainerStatus: ready: [ {0} ] is invalid'.format(ready))
        self._ready = ready

    # ------------------------------------------------------------------------------------- restartCount

    @property
    def restart_count(self):
        return self._restart_count

    @restart_count.setter
    def restart_count(self, count=None):
        if not isinstance(count, int):
            raise SyntaxError('ContainerStatus: restart_count: [ {0} ] is invalid'.format(count))
        self._restart_count = count

    # ------------------------------------------------------------------------------------- image

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, image=None):
        if not is_valid_string(image):
            raise SyntaxError('ContainerStatus: image: [ {0} ] is invalid'.format(image))
        self._image = image

    # ------------------------------------------------------------------------------------- imageID

    @property
    def image_id(self):
        return self._image_id

    @image_id.setter
    def image_id(self, iid=None):
        if not is_valid_string(iid):
            raise SyntaxError('ContainerStatus: image_id: [ {0} ] is invalid'.format(iid))
        self._image_id = iid

    # ------------------------------------------------------------------------------------- containerID

    @property
    def container_id(self):
        return self._container_id

    @container_id.setter
    def container_id(self, cid=None):
        if not is_valid_string(cid):
            raise SyntaxError('ContainerStatus: container_id: [ {0} ] is invalid'.format(cid))
        self._container_id = cid

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.name is not None:
            data['name'] = self.name
        if self.state is not None:
            data['state'] = self.state.serialize()
        if self.last_state is not None:
            data['lastState'] = self.last_state.serialize()
        if self.ready is not None:
            data['ready'] = self.ready
        if self.restart_count is not None:
            data['restartCount'] = self.restart_count
        if self.image is not None:
            data['image'] = self.image
        if self.image_id is not None:
            data['imageID'] = self.image_id
        if self.container_id is not None:
            data['containerID'] = self.container_id
        return data

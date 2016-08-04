#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.BaseModel import BaseModel


class ContainerStatus(BaseModel):
    def __init__(self, model=None):
        BaseModel.__init__(self)
        if model is not None:
            assert isinstance(model, dict)
            self.model = model

    def get_name(self):
        return self.model.get('name', '')

    def get_state(self):
        return self.model.get('state', dict())

    def get_last_state(self):
        return self.model.get('lastState', dict())

    def get_restart_count(self):
        return self.model.get('restartCount', -1)

    def get_image(self):
        return self.model.get('image', None)

    def get_image_id(self):
        return self.model.get('imageID', None)

    def get_container_id(self):
        return self.model.get('containerID', None)

    def is_ready(self):
        return self.model.get('ready', False)


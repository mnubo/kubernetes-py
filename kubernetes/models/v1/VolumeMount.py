#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1 import BaseModel


class VolumeMount(BaseModel):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_volumemount
    """

    def __init__(self, name=None, mount_path=None, read_only=False, sub_path=None):
        super(VolumeMount, self).__init__()
        self.name = name
        self.read_only = read_only
        self.mount_path = mount_path
        self.sub_path = sub_path

    # ------------------------------------------------------------------------------------- serialize

    def json(self):
        data = {}
        if self.name:
            data['name'] = self.name
        if self.read_only:
            data['readOnly'] = self.read_only
        if self.mount_path:
            data['mountPath'] = self.mount_path
        if self.sub_path:
            data['subPath'] = self.sub_path
        return data
#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import json

import yaml

from kubernetes.models.v1.VolumeMount import VolumeMount


class K8sVolumeMount(object):
    def __init__(self, name=None, mount_path=None, read_only=False, sub_path=None):
        super(K8sVolumeMount, self).__init__()

        self.model = VolumeMount()

        if name is not None:
            self.name = name
        if mount_path is not None:
            self.mount_path = mount_path
        if read_only is not None:
            self.read_only = read_only
        if sub_path is not None:
            self.sub_path = sub_path

    # ------------------------------------------------------------------------------------- name

    @property
    def name(self):
        return self.model.name

    @name.setter
    def name(self, name=None):
        self.model.name = name

    # ------------------------------------------------------------------------------------- mount_path

    @property
    def mount_path(self):
        return self.model.mount_path

    @mount_path.setter
    def mount_path(self, mp=None):
        self.model.mount_path = mp

    # ------------------------------------------------------------------------------------- read_only

    @property
    def read_only(self):
        return self.model.read_only

    @read_only.setter
    def read_only(self, ro=None):
        self.model.read_only = ro

    # ------------------------------------------------------------------------------------- sub_path

    @property
    def sub_path(self):
        return self.model.sub_path

    @sub_path.setter
    def sub_path(self, sp=None):
        self.model.sub_path = sp

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        return self.model.serialize()

    def as_json(self):
        data = self.serialize()
        dump = json.dumps(data, indent=4)
        return dump

    def as_yaml(self):
        data = self.serialize()
        dump = yaml.dump(data, default_flow_style=False)
        return dump

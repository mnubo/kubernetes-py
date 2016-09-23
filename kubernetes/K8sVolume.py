#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.Volume import Volume
from kubernetes.K8sObject import K8sObject


class K8sVolume(K8sObject):

    def __init__(self, config=None, model=None, name=None, type=None, mount_path=None, read_only=False):

        super(K8sVolume, self).__init__(config=config, name=name, obj_type='Volume')

        if model is None:
            self.model = Volume(name=name, type=type, mount_path=mount_path, read_only=read_only)
            self.type = type

        if model is not None:
            if not isinstance(model, Volume):
                raise SyntaxError('K8sVolume: model: [ {0} ] must be a Volume.'.format(model.__class__.__name__))
            self.model = model
            self.type = self.model.type

    # -------------------------------------------------------------------------------------  emptyDir

    def set_medium(self, medium=None):
        self.model.set_medium(medium)
        return self

    # -------------------------------------------------------------------------------------  hostPath

    def set_host_path(self, path=None):
        self.model.set_host_path(path)
        return self

    # -------------------------------------------------------------------------------------  secret

    def set_secret_name(self, secret=None):
        self.model.set_secret_name(secret)
        return self

    # -------------------------------------------------------------------------------------  awsElasticBlockStore

    def set_volume_id(self, volume_id=None):
        self.model.set_volume_id(volume_id)
        return self

    # -------------------------------------------------------------------------------------  gcePersistentDisk

    def set_pd_name(self, pd_name=None):
        self.model.set_pd_name(pd_name)
        return self

    # -------------------------------------------------------------------------------------  aws & gce - fs type

    def set_fs_type(self, fs_type=None):
        self.model.set_fs_type(fs_type)
        return self

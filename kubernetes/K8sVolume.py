#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.K8sObject import K8sObject
from kubernetes.K8sSecret import K8sSecret

VALID_VOLUME_TYPES = [
    'emptyDir',
    'hostPath',
    # 'gcePersistentDisk',          .2
    # 'awsElasticBlockStore',       .1
    # 'nfs',                        .3
    # 'iscsi',
    # 'flocker',
    # 'glusterfs',
    # 'rbd',
    # 'cephfs',
    # 'gitRepo',                    .4
    'secret',
    # 'persistentVolumeClaim',      .5
    # 'downwardAPI',
    # 'azureFileVolume',
    # 'vsphereVolume',
]

VALID_EMPTYDIR_MEDIA = [
    '',
    'Memory'
]


class K8sVolume(K8sObject):

    def __init__(self, name=None, type=None, mount_path=None, read_only=False):
        if name is None:
            raise SyntaxError('K8sVolume: name: [ {0} ] cannot be None.'.format(name))
        if not isinstance(name, str):
            raise SyntaxError('K8sVolume: name: [ {0} ] must be a string.'.format(name.__class__.__name__))

        if type is None:
            type = 'emptyDir'
        if type is not None and type not in VALID_VOLUME_TYPES:
            raise SyntaxError('K8sVolume: volume_type: [ {0} ] is invalid. Must be in: [ {1} ]'.format(type, VALID_VOLUME_TYPES))

        if mount_path is None:
            raise SyntaxError('K8sVolume: mount_path: [ {0} ] cannot be None.'.format(mount_path))
        if not isinstance(mount_path, str):
            raise SyntaxError('K8sVolume: mount_path: [ {0} ] must be a string.'.format(mount_path))
        if not self._is_valid_path(mount_path):
            raise SyntaxError("K8sVolume: mount_path: [ {0} ] is not a valid path.".format(mount_path))

        if not isinstance(read_only, bool):
            raise SyntaxError('K8sVolume: read_only: [ {0} ] must be a boolean.'.format(read_only.__class__.__name__))

        super(K8sVolume, self).__init__(name=name, obj_type='Volume')

        self.host_path = None  # used with type 'hostPath'
        self.medium = ''  # used with type 'emptyDir'
        self.mount_path = mount_path
        self.read_only = read_only
        self.secret_name = None  # used with type 'secret'
        self.type = type

    @staticmethod
    def _is_valid_path(path):
        # Ugh. What a PITA. # TODO: validate path for unix and windows.
        #
        # re_match = re.match(r'^(([a-zA-Z]:)|((\\|/){1,2}\w+)\$?)((\\|/)(\w[\w ]*.*))+\.([a-zA-Z0-9]+)$', path)
        # if re_match is None:
        #     return False
        return True

    # -------------------------------------------------------------------------------------  emptyDir

    def set_medium(self, medium=None):
        if medium is None:
            medium = ''
        if medium is not None and self.type != 'emptyDir':
            raise SyntaxError('K8sVolume: medium: [ {0} ] can only be used with type [ emptyDir ]'. format(medium))
        if medium not in VALID_EMPTYDIR_MEDIA:
            raise SyntaxError('K8sVolume: medium: [ {0} ] is invalid. Must be in: [ {1} ] '.format(medium, VALID_EMPTYDIR_MEDIA))

        self.medium = medium
        return self

    # -------------------------------------------------------------------------------------  hostPath

    def set_host_path(self, path=None):
        if path is None:
            raise SyntaxError("K8sVolume: path: [ {0} ] cannot be None.".format(path))
        if path is not None and self.type != 'hostPath':
            raise SyntaxError('K8sVolume: path: [ {0} ] can only be used with type [ hostPath ]'.format(path))
        if not self._is_valid_path(path):
            raise SyntaxError("K8sVolume: path: [ {0} ] is not a valid path.".format(path))

        self.host_path = path
        return self

    # -------------------------------------------------------------------------------------  secret

    def set_secret_name(self, secret=None):
        if not isinstance(secret, K8sSecret):
            raise SyntaxError('K8sVolume: secret: [ {0} ] must be a K8sSecret.'.format(secret.__class__.__name__))
        if secret is not None and self.type != 'secret':
            raise SyntaxError('K8sVolume: secret: [ {0} ] can only be used with type [ secret ]'.format(secret.name))

        self.secret_name = secret.name
        return self

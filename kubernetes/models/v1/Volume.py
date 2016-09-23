#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.K8sSecret import K8sSecret
from kubernetes.models.v1 import BaseModel


class Volume(BaseModel):
    VALID_VOLUME_TYPES = [
        'emptyDir',
        'hostPath',
        'gcePersistentDisk',
        'awsElasticBlockStore',
        'nfs',
        # 'iscsi',
        # 'flocker',
        # 'glusterfs',
        # 'rbd',
        # 'cephfs',
        # 'gitRepo',
        'secret',
        # 'persistentVolumeClaim',
        # 'downwardAPI',
        # 'azureFileVolume',
        # 'vsphereVolume',
    ]

    VALID_EMPTYDIR_MEDIA = [
        '',
        'Memory'
    ]

    def __init__(self, name=None, type=None, mount_path=None, read_only=False):

        super(Volume, self).__init__()

        if name is None:
            raise SyntaxError('Volume: name: [ {0} ] cannot be None.'.format(name))
        if not isinstance(name, str):
            raise SyntaxError('Volume: name: [ {0} ] must be a string.'.format(name.__class__.__name__))

        if type not in Volume.VALID_VOLUME_TYPES:
            raise SyntaxError('Volume: type: [ {0} ] is invalid.'.format(type))

        if not Volume._is_valid_path(mount_path):
            raise SyntaxError('Volume: mount_path: [ {0} ] is invalid.'.format(mount_path))

        if not isinstance(read_only, bool):
            raise SyntaxError('Volume: read_only: [ {0} ] must be a boolean.'.format(read_only.__class__.__name__))

        self.aws_volume_id = None  # used with type 'awsElasticBlockStore'
        self.fs_type = 'ext4'  # used with types 'awsElasticBlockStore' and 'gcePersistentDisk'
        self.gce_pd_name = None  # used with type 'gcePersistentDisk'
        self.path = None  # used with type 'hostPath' and 'nfs'
        self.medium = ''  # used with type 'emptyDir'
        self.mount_path = mount_path
        self.name = name
        self.read_only = read_only
        self.secret_name = None  # used with type 'secret'
        self.server = None  # used with type 'nfs
        self.type = type
        self._update_model()

    # -------------------------------------------------------------------------------------  utils

    @staticmethod
    def _is_valid_path(path=None):
        # Ugh. What a PITA. # TODO: validate path for unix and windows.
        #
        # re_match = re.match(r'^(([a-zA-Z]:)|((\\|/){1,2}\w+)\$?)((\\|/)(\w[\w ]*.*))+\.([a-zA-Z0-9]+)$', path)
        # if re_match is None:
        #     return False
        if not isinstance(path, str):
            return False
        return True

    def _update_model(self):

        self.model = {
            'volumeMount': {
                'name': self.name,
                'mountPath': self.mount_path,
            },
            'volume': {
                'name': self.name,
                self.type: {}
            }
        }

        if self.read_only is True:
            self.model['volumeMount']['readOnly'] = True
        if self.type == 'emptyDir' and self.medium != '':
            self.model['volume'][self.type]['medium'] = self.medium
        if self.type == 'hostPath':
            self.model['volume'][self.type]['path'] = self.path
        if self.type == 'secret':
            self.model['volume'][self.type]['secretName'] = self.secret_name
        if self.type == 'awsElasticBlockStore':
            self.model['volume'][self.type]['volumeID'] = self.aws_volume_id
            self.model['volume'][self.type]['fsType'] = self.fs_type
        if self.type == 'gcePersistentDisk':
            self.model['volume'][self.type]['pdName'] = self.gce_pd_name
            self.model['volume'][self.type]['fsType'] = self.fs_type
        if self.type == 'nfs':
            self.model['volume'][self.type]['server'] = self.server
            self.model['volume'][self.type]['path'] = self.path

    # -------------------------------------------------------------------------------------  emptyDir

    def set_medium(self, medium=None):
        if medium is None:
            medium = ''
        if medium not in Volume.VALID_EMPTYDIR_MEDIA:
            raise SyntaxError(
                'Volume: medium: [ {0} ] is invalid. Must be in: [ {1} ] '.format(medium, Volume.VALID_EMPTYDIR_MEDIA))
        if medium is not None and self.type != 'emptyDir':
            raise SyntaxError('Volume: medium: [ {0} ] can only be used with type [ emptyDir ]'.format(medium))
        self.medium = medium
        self._update_model()
        return self

    # -------------------------------------------------------------------------------------  hostPath & nfs - path

    def set_path(self, path=None):
        if path is None:
            raise SyntaxError("Volume: path: [ {0} ] cannot be None.".format(path))
        if not self._is_valid_path(path):
            raise SyntaxError("Volume: path: [ {0} ] is invalid.".format(path))
        if path is not None and self.type not in ['hostPath', 'nfs']:
            raise SyntaxError(
                'Volume: path: [ {0} ] can only be used with types [ \'hostPath\', \'nfs\' ]'.format(path))
        self.path = path
        self._update_model()
        return self

    # -------------------------------------------------------------------------------------  secret

    def set_secret_name(self, secret=None):
        if not isinstance(secret, K8sSecret):
            raise SyntaxError('Volume: secret: [ {0} ] must be a K8sSecret.'.format(secret.__class__.__name__))
        if secret is not None and self.type != 'secret':
            raise SyntaxError('Volume: secret: [ {0} ] can only be used with type [ secret ]'.format(secret.name))
        self.secret_name = secret.name
        self._update_model()
        return self

    # -------------------------------------------------------------------------------------  awsElasticBlockStore

    def set_volume_id(self, volume_id=None):
        if not isinstance(volume_id, str):
            raise SyntaxError('Volume: volume_id: [ {0} ] must be a string.'.format(volume_id.__class__.__name__))
        if volume_id is not None and self.type != 'awsElasticBlockStore':
            raise SyntaxError('Volume: volume_id: [ {0} ] can only be used with '
                              'type [ awsElasticBlockStore ]'.format(volume_id))
        self.aws_volume_id = volume_id
        self._update_model()
        return self

    # -------------------------------------------------------------------------------------  gcePersistentDisk

    def set_pd_name(self, pd_name=None):
        if not isinstance(pd_name, str):
            raise SyntaxError('Volume: pd_name: [ {0} ] must be a string.'.format(pd_name.__class__.__name__))
        if pd_name is not None and self.type != 'gcePersistentDisk':
            raise SyntaxError('Volume: pd_name: [ {0} ] can only be used with '
                              'type [ gcePersistentDisk ]'.format(pd_name))
        self.gce_pd_name = pd_name
        self._update_model()
        return self

    # -------------------------------------------------------------------------------------  aws & gce - fs type

    def set_fs_type(self, fs_type=None):
        if not isinstance(fs_type, str):
            raise SyntaxError('Volume: fs_type: [ {0} ] must be a string.'.format(fs_type.__class__.__name__))
        if fs_type is not None and not (self.type == 'awsElasticBlockStore' or self.type == 'gcePersistentDisk'):
            raise SyntaxError('Volume: fs_type: [ {0} ] can only be used with type [ awsElasticBlockStore ] '
                              'or [ gcePersistentDisk ]'.format(fs_type))
        self.fs_type = fs_type
        self._update_model()
        return self

    # -------------------------------------------------------------------------------------  nfs

    def set_server(self, server=None):
        if not isinstance(server, str):
            raise SyntaxError('Volume: server: [ {0} ] must be a string.'.format(server.__class__.__name__))
        if server is not None and not (self.type == 'nfs'):
            raise SyntaxError('Volume: server: [ {0} ] can only be used with type [ nfs ]'.format(server))
        self.server = server
        self._update_model()
        return self

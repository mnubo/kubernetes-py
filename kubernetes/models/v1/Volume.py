#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.utils import is_valid_string, filter_model
from kubernetes.models.v1.AWSElasticBlockStoreVolumeSource import AWSElasticBlockStoreVolumeSource
from kubernetes.models.v1.EmptyDirVolumeSource import EmptyDirVolumeSource
from kubernetes.models.v1.GCEPersistentDiskVolumeSource import GCEPersistentDiskVolumeSource
from kubernetes.models.v1.GitRepoVolumeSource import GitRepoVolumeSource
from kubernetes.models.v1.HostPathVolumeSource import HostPathVolumeSource
from kubernetes.models.v1.NFSVolumeSource import NFSVolumeSource
from kubernetes.models.v1.SecretVolumeSource import SecretVolumeSource


class Volume(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_volume
    """

    VALID_VOLUME_TYPES = [
        'awsElasticBlockStore',
        'emptyDir',
        'gcePersistentDisk',
        'gitRepo',
        'hostPath',
        'nfs',
        'secret',
    ]

    def __init__(self, model=None):

        # TODO(froch): add support for the below
        # self._iscsi = None
        # self._glusterfs = None
        # self._persistent_volume_claim = None
        # self._rbd = None
        # self._flex_volume = None
        # self._cinder = None
        # self._cephfs = None
        # self._flocker = None
        # self._downward_api = None
        # self._fc = None
        # self._azure_file = None
        # self._config_map = None
        # self._vsphere_volume
        # self._quobyte = None
        # self._azuredisk = None

        self._aws_elastic_block_store = None
        self._empty_dir = None
        self._gce_persistent_disk = None
        self._git_repo = None
        self._host_path = None
        self._name = None
        self._nfs = None
        self._secret = None

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def __eq__(self, other):
        # see https://github.com/kubernetes/kubernetes/blob/release-1.3/docs/design/identifiers.md
        if isinstance(other, self.__class__):
            # Uniquely name (via a name) an object across space.
            return self.name == other.name
        return NotImplemented

    def _build_with_model(self, model=None):
        if 'awsElasticBlockStore' in model:
            self.aws_elastic_block_store = AWSElasticBlockStoreVolumeSource(model=model['awsElasticBlockStore'])
        if 'emptyDir' in model:
            self.empty_dir = EmptyDirVolumeSource(model=model['emptyDir'])
        if 'gcePersistentDisk' in model:
            self.gce_persistent_disk = GCEPersistentDiskVolumeSource(model=model['gcePersistentDisk'])
        if 'gitRepo' in model:
            self.git_repo = GitRepoVolumeSource(model=model['gitRepo'])
        if 'hostPath' in model:
            self.host_path = HostPathVolumeSource(model=model['hostPath'])
        if 'name' in model:
            self.name = model['name']
        if 'nfs' in model:
            self.nfs = NFSVolumeSource(model=model['nfs'])
        if 'secret' in model:
            self.secret = SecretVolumeSource(model=model['secret'])

    # ------------------------------------------------------------------------------------- aws ebs

    @property
    def aws_elastic_block_store(self):
        return self._aws_elastic_block_store

    @aws_elastic_block_store.setter
    def aws_elastic_block_store(self, ebs=None):
        if not isinstance(ebs, AWSElasticBlockStoreVolumeSource):
            raise SyntaxError('Volume: aws_elastic_block_store: [ {0} ] is invalid.'.format(ebs))
        self._aws_elastic_block_store = ebs

    # ------------------------------------------------------------------------------------- emptyDir

    @property
    def empty_dir(self):
        return self._empty_dir

    @empty_dir.setter
    def empty_dir(self, edir=None):
        if not isinstance(edir, EmptyDirVolumeSource):
            raise SyntaxError('Volume: empty_dir: [ {0} ] is invalid.'.format(edir))
        self._empty_dir = edir

    # ------------------------------------------------------------------------------------- gce pd

    @property
    def gce_persistent_disk(self):
        return self._gce_persistent_disk

    @gce_persistent_disk.setter
    def gce_persistent_disk(self, pd=None):
        if not isinstance(pd, GCEPersistentDiskVolumeSource):
            raise SyntaxError('Volume: gce_persistent_disk: [ {0} ] is invalid.'.format(pd))
        self._gce_persistent_disk = pd

    # ------------------------------------------------------------------------------------- gitRepo

    @property
    def git_repo(self):
        return self._git_repo

    @git_repo.setter
    def git_repo(self, repo=None):
        if not isinstance(repo, GitRepoVolumeSource):
            raise SyntaxError('Volume: git_repo: [ {0} ] is invalid.'.format(repo))
        self._git_repo = repo

    # ------------------------------------------------------------------------------------- hostPath

    @property
    def host_path(self):
        return self._host_path

    @host_path.setter
    def host_path(self, hp=None):
        if not isinstance(hp, HostPathVolumeSource):
            raise SyntaxError('Volume: host_path: [ {0} ] is invalid.'.format(hp))
        self._host_path = hp

    # ------------------------------------------------------------------------------------- nfs

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name=None):
        if not is_valid_string(name):
            raise SyntaxError('Volume: name: [ {0} ] is invalid.'.format(name))
        self._name = name

    # ------------------------------------------------------------------------------------- nfs

    @property
    def nfs(self):
        return self._nfs

    @nfs.setter
    def nfs(self, nfs=None):
        if not isinstance(nfs, NFSVolumeSource):
            raise SyntaxError('Volume: nfs: [ {0} ] is invalid.'.format(nfs))
        self._nfs = nfs

    # ------------------------------------------------------------------------------------- secret

    @property
    def secret(self):
        return self._secret

    @secret.setter
    def secret(self, secret=None):
        if not isinstance(secret, SecretVolumeSource):
            raise SyntaxError('Volume: secret: [ {0} ] is invalid.'.format(secret))
        self._secret = secret

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.aws_elastic_block_store is not None:
            data['awsElasticBlockStore'] = self.aws_elastic_block_store.serialize()
        if self.empty_dir is not None:
            data['emptyDir'] = self.empty_dir.serialize()
        if self.gce_persistent_disk is not None:
            data['gcePersistentDisk'] = self.gce_persistent_disk.serialize()
        if self.git_repo is not None:
            data['gitRepo'] = self.git_repo.serialize()
        if self.host_path is not None:
            data['hostPath'] = self.host_path.serialize()
        if self.name is not None:
            data['name'] = self.name
        if self.nfs is not None:
            data['nfs'] = self.nfs.serialize()
        if self.secret is not None:
            data['secret'] = self.secret.serialize()
        return data

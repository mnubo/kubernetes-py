#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.AWSElasticBlockStoreVolumeSource import AWSElasticBlockStoreVolumeSource
from kubernetes.models.v1.EmptyDirVolumeSource import EmptyDirVolumeSource
from kubernetes.models.v1.GCEPersistentDiskVolumeSource import GCEPersistentDiskVolumeSource
from kubernetes.models.v1.GitRepoVolumeSource import GitRepoVolumeSource
from kubernetes.models.v1.HostPathVolumeSource import HostPathVolumeSource
from kubernetes.models.v1.NFSVolumeSource import NFSVolumeSource
from kubernetes.models.v1.SecretVolumeSource import SecretVolumeSource
from kubernetes.models.v1.PersistentVolumeClaimVolumeSource import PersistentVolumeClaimVolumeSource
from kubernetes.utils import is_valid_string, filter_model


class Volume(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_volume
    """

    VOLUME_TYPES_TO_SOURCE_MAP = {
        'awsElasticBlockStore': AWSElasticBlockStoreVolumeSource,
        'emptyDir': EmptyDirVolumeSource,
        'gcePersistentDisk': GCEPersistentDiskVolumeSource,
        'gitRepo': GitRepoVolumeSource,
        'hostPath': HostPathVolumeSource,
        'nfs': NFSVolumeSource,
        'secret': SecretVolumeSource,
        'persistentVolumeClaim': PersistentVolumeClaimVolumeSource,
    }

    def __init__(self, model=None):

        # TODO(froch): add support for the below
        # self._iscsi = None
        # self._glusterfs = None
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

        self._awsElasticBlockStore = None
        self._emptyDir = None
        self._gcePersistentDisk = None
        self._gitRepo = None
        self._hostPath = None
        self._name = None
        self._nfs = None
        self._persistentVolumeClaim = None
        self._secret = None

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def __eq__(self, other):
        # see https://github.com/kubernetes/kubernetes/blob/master/docs/design/identifiers.md
        if isinstance(other, self.__class__):
            return self.name == other.name
        return NotImplemented

    def _build_with_model(self, model=None):
        if 'awsElasticBlockStore' in model:
            self.awsElasticBlockStore = AWSElasticBlockStoreVolumeSource(model['awsElasticBlockStore'])
        if 'emptyDir' in model:
            self.emptyDir = EmptyDirVolumeSource(model['emptyDir'])
        if 'gcePersistentDisk' in model:
            self.gcePersistentDisk = GCEPersistentDiskVolumeSource(model['gcePersistentDisk'])
        if 'gitRepo' in model:
            self.gitRepo = GitRepoVolumeSource(model['gitRepo'])
        if 'hostPath' in model:
            self.hostPath = HostPathVolumeSource(model['hostPath'])
        if 'name' in model:
            self.name = model['name']
        if 'nfs' in model:
            self.nfs = NFSVolumeSource(model['nfs'])
        if 'secret' in model:
            self.secret = SecretVolumeSource(model['secret'])
        if 'persistentVolumeClaim' in model:
            self.persistentVolumeClaim = PersistentVolumeClaimVolumeSource(model['persistentVolumeClaim'])

    @staticmethod
    def vol_type_to_source(vol_type=None):
        return Volume.VOLUME_TYPES_TO_SOURCE_MAP[vol_type]()

    # ------------------------------------------------------------------------------------- aws ebs

    @property
    def awsElasticBlockStore(self):
        return self._awsElasticBlockStore

    @awsElasticBlockStore.setter
    def awsElasticBlockStore(self, ebs=None):
        if not isinstance(ebs, AWSElasticBlockStoreVolumeSource):
            raise SyntaxError('Volume: aws_elastic_block_store: [ {0} ] is invalid.'.format(ebs))
        self._awsElasticBlockStore = ebs

    # ------------------------------------------------------------------------------------- emptyDir

    @property
    def emptyDir(self):
        return self._emptyDir

    @emptyDir.setter
    def emptyDir(self, edir=None):
        if not isinstance(edir, EmptyDirVolumeSource):
            raise SyntaxError('Volume: empty_dir: [ {0} ] is invalid.'.format(edir))
        self._emptyDir = edir

    # ------------------------------------------------------------------------------------- gce pd

    @property
    def gcePersistentDisk(self):
        return self._gcePersistentDisk

    @gcePersistentDisk.setter
    def gcePersistentDisk(self, pd=None):
        if not isinstance(pd, GCEPersistentDiskVolumeSource):
            raise SyntaxError('Volume: gce_persistent_disk: [ {0} ] is invalid.'.format(pd))
        self._gcePersistentDisk = pd

    # ------------------------------------------------------------------------------------- gitRepo

    @property
    def gitRepo(self):
        return self._gitRepo

    @gitRepo.setter
    def gitRepo(self, repo=None):
        if not isinstance(repo, GitRepoVolumeSource):
            raise SyntaxError('Volume: git_repo: [ {0} ] is invalid.'.format(repo))
        self._gitRepo = repo

    # ------------------------------------------------------------------------------------- hostPath

    @property
    def hostPath(self):
        return self._hostPath

    @hostPath.setter
    def hostPath(self, hp=None):
        if not isinstance(hp, HostPathVolumeSource):
            raise SyntaxError('Volume: host_path: [ {0} ] is invalid.'.format(hp))
        self._hostPath = hp

    # ------------------------------------------------------------------------------------- name

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

    # ------------------------------------------------------------------------------------- persistentVolumeClaim

    @property
    def persistentVolumeClaim(self):
        return self._persistentVolumeClaim

    @persistentVolumeClaim.setter
    def persistentVolumeClaim(self, pvc=None):
        if not isinstance(pvc, PersistentVolumeClaimVolumeSource):
            raise SyntaxError('Volume: persistentVolumeClaim: [ {0} ] is invalid.'.format(pvc))
        self._persistentVolumeClaim = pvc

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.awsElasticBlockStore is not None:
            data['awsElasticBlockStore'] = self.awsElasticBlockStore.serialize()
        if self.emptyDir is not None:
            data['emptyDir'] = self.emptyDir.serialize()
        if self.gcePersistentDisk is not None:
            data['gcePersistentDisk'] = self.gcePersistentDisk.serialize()
        if self.gitRepo is not None:
            data['gitRepo'] = self.gitRepo.serialize()
        if self.hostPath is not None:
            data['hostPath'] = self.hostPath.serialize()
        if self.name is not None:
            data['name'] = self.name
        if self.nfs is not None:
            data['nfs'] = self.nfs.serialize()
        if self.secret is not None:
            data['secret'] = self.secret.serialize()
        if self.persistentVolumeClaim is not None:
            data['persistentVolumeClaim'] = self.persistentVolumeClaim.serialize()
        return data

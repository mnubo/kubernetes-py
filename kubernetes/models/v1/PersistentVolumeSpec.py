#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.ObjectReference import ObjectReference
from kubernetes.models.v1.AWSElasticBlockStoreVolumeSource import AWSElasticBlockStoreVolumeSource
from kubernetes.models.v1.EmptyDirVolumeSource import EmptyDirVolumeSource
from kubernetes.models.v1.GCEPersistentDiskVolumeSource import GCEPersistentDiskVolumeSource
from kubernetes.models.v1.GitRepoVolumeSource import GitRepoVolumeSource
from kubernetes.models.v1.HostPathVolumeSource import HostPathVolumeSource
from kubernetes.models.v1.NFSVolumeSource import NFSVolumeSource
from kubernetes.models.v1.SecretVolumeSource import SecretVolumeSource
from kubernetes.models.v1.PersistentVolumeClaimVolumeSource import PersistentVolumeClaimVolumeSource
from kubernetes.utils import is_valid_string, is_valid_dict, is_valid_list


class PersistentVolumeSpec(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_persistentvolumespec
    """

    VALID_CAPACITY_PARAMS = ['storage']
    VALID_ACCESS_MODES = ['ReadWriteOnce', 'ReadOnlyMany', 'ReadWriteMany']
    VALID_RECLAIM_POLICIES = ['Retain', 'Recycle', 'Delete']

    VOLUME_TYPES_TO_SOURCE_MAP = {
        'awsElasticBlockStore': AWSElasticBlockStoreVolumeSource,
        'emptyDir': EmptyDirVolumeSource,
        'gcePersistentDisk': GCEPersistentDiskVolumeSource,
        'gitRepo': GitRepoVolumeSource,
        'hostPath': HostPathVolumeSource,
        'nfs': NFSVolumeSource,
        'secret': SecretVolumeSource
    }

    def __init__(self, model=None):
        super(PersistentVolumeSpec, self).__init__()

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

        self._capacity = {'storage': '10Gi'}
        self._access_modes = ['ReadWriteOnce']
        self._claim_ref = None
        self._reclaim_policy = 'Retain'

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'awsElasticBlockStore' in model:
            self.awsElasticBlockStore = AWSElasticBlockStoreVolumeSource(model['awsElasticBlockStore'])
        if 'gcePersistentDisk' in model:
            self.gcePersistentDisk = GCEPersistentDiskVolumeSource(model['gcePersistentDisk'])
        if 'hostPath' in model:
            self.hostPath = HostPathVolumeSource(model['hostPath'])
        if 'name' in model:
            self.name = model['name']
        if 'nfs' in model:
            self.nfs = NFSVolumeSource(model['nfs'])
        if 'secret' in model:
            self.secret = SecretVolumeSource(model['secret'])
        if 'capacity' in model:
            self.capacity = model['capacity']
        if 'accessModes' in model:
            self.access_modes = model['accessModes']
        if 'claimRef' in model:
            self.claim_ref = ObjectReference(model['claimRef'])
        if 'persistentVolumeReclaimPolicy' in model:
            self.reclaim_policy = model['persistentVolumeReclaimPolicy']
        if 'persistentVolumeClaim' in model:
            self.persistentVolumeClaim = PersistentVolumeClaimVolumeSource(model['persistentVolumeClaim'])

    # ------------------------------------------------------------------------------------- aws ebs

    @property
    def awsElasticBlockStore(self):
        return self._awsElasticBlockStore

    @awsElasticBlockStore.setter
    def awsElasticBlockStore(self, ebs=None):
        if not isinstance(ebs, AWSElasticBlockStoreVolumeSource):
            raise SyntaxError('PersistentVolumeSpec: aws_elastic_block_store: [ {0} ] is invalid.'.format(ebs))
        self._awsElasticBlockStore = ebs

    # ------------------------------------------------------------------------------------- emptyDir

    @property
    def emptyDir(self):
        return self._emptyDir

    @emptyDir.setter
    def emptyDir(self, edir=None):
        if not isinstance(edir, EmptyDirVolumeSource):
            raise SyntaxError('PersistentVolumeSpec: empty_dir: [ {0} ] is invalid.'.format(edir))
        self._emptyDir = edir

    # ------------------------------------------------------------------------------------- gce pd

    @property
    def gcePersistentDisk(self):
        return self._gcePersistentDisk

    @gcePersistentDisk.setter
    def gcePersistentDisk(self, pd=None):
        if not isinstance(pd, GCEPersistentDiskVolumeSource):
            raise SyntaxError('PersistentVolumeSpec: gce_persistent_disk: [ {0} ] is invalid.'.format(pd))
        self._gcePersistentDisk = pd

    # ------------------------------------------------------------------------------------- gitRepo

    @property
    def gitRepo(self):
        return self._gitRepo

    @gitRepo.setter
    def gitRepo(self, repo=None):
        if not isinstance(repo, GitRepoVolumeSource):
            raise SyntaxError('PersistentVolumeSpec: git_repo: [ {0} ] is invalid.'.format(repo))
        self._gitRepo = repo

    # ------------------------------------------------------------------------------------- hostPath

    @property
    def hostPath(self):
        return self._hostPath

    @hostPath.setter
    def hostPath(self, hp=None):
        if not isinstance(hp, HostPathVolumeSource):
            raise SyntaxError('PersistentVolumeSpec: host_path: [ {0} ] is invalid.'.format(hp))
        self._hostPath = hp

    # ------------------------------------------------------------------------------------- name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name=None):
        if not is_valid_string(name):
            raise SyntaxError('PersistentVolumeSpec: name: [ {0} ] is invalid.'.format(name))
        self._name = name

    # ------------------------------------------------------------------------------------- nfs

    @property
    def nfs(self):
        return self._nfs

    @nfs.setter
    def nfs(self, nfs=None):
        if not isinstance(nfs, NFSVolumeSource):
            raise SyntaxError('PersistentVolumeSpec: nfs: [ {0} ] is invalid.'.format(nfs))
        self._nfs = nfs

    # ------------------------------------------------------------------------------------- secret

    @property
    def secret(self):
        return self._secret

    @secret.setter
    def secret(self, secret=None):
        if not isinstance(secret, SecretVolumeSource):
            raise SyntaxError('PersistentVolumeSpec: secret: [ {0} ] is invalid.'.format(secret))
        self._secret = secret

    # ------------------------------------------------------------------------------------- capacity

    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, c=None):
        if not is_valid_dict(c, PersistentVolumeSpec.VALID_CAPACITY_PARAMS):
            raise SyntaxError('PersistentVolumeSpec: capacity: [ {} ] is invalid.'.format(c))
        self._capacity = c

    # ------------------------------------------------------------------------------------- accessModes

    @property
    def access_modes(self):
        return self._access_modes

    @access_modes.setter
    def access_modes(self, modes=None):
        if not is_valid_list(modes, str):
            raise SyntaxError('PersistentVolumeSpec: access_modes: [ {} ] is invalid.'.format(modes))
        filtered = list(filter(lambda x: x in PersistentVolumeSpec.VALID_ACCESS_MODES, modes))
        self._access_modes = filtered

    # ------------------------------------------------------------------------------------- claimRef

    @property
    def claim_ref(self):
        return self._claim_ref

    @claim_ref.setter
    def claim_ref(self, ref=None):
        if not isinstance(ref, ObjectReference):
            raise SyntaxError('PersistentVolumeSpec: claim_ref: [ {} ] is invalid.'.format(ref))
        self._claim_ref = ref

    # ------------------------------------------------------------------------------------- reclaimPolicy

    @property
    def reclaim_policy(self):
        return self._reclaim_policy

    @reclaim_policy.setter
    def reclaim_policy(self, policy=None):
        if policy not in PersistentVolumeSpec.VALID_RECLAIM_POLICIES:
            raise SyntaxError('PersistentVolumeSpec: reclaim_policy: [ {} ] is invalid.'.format(policy))
        self._reclaim_policy = policy

    # ------------------------------------------------------------------------------------- persistentVolumeClaim

    @property
    def persistentVolumeClaim(self):
        return self._persistentVolumeClaim

    @persistentVolumeClaim.setter
    def persistentVolumeClaim(self, pvc=None):
        if not isinstance(pvc, PersistentVolumeClaimVolumeSource):
            raise SyntaxError('PersistentVolumeSpec: persistentVolumeClaim: [ {} ] is invalid.'.format(pvc))
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
        if self.capacity is not None:
            data['capacity'] = self.capacity
        if self.access_modes is not None:
            data['accessModes'] = self.access_modes
        if self.claim_ref is not None:
            data['claimRef'] = self.claim_ref.serialize()
        if self.reclaim_policy is not None:
            data['persistentVolumeReclaimPolicy'] = self.reclaim_policy
        if self.persistentVolumeClaim is not None:
            data['persistentVolumeClaim'] = self.reclaim_policy
        return data

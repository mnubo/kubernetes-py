#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import json

import yaml

from kubernetes.models.v1.Volume import Volume


class K8sVolume(object):
    VALID_VOLUME_TYPES = Volume.VOLUME_TYPES_TO_SOURCE_MAP.keys()

    def __init__(self, name=None, type=None):
        super(K8sVolume, self).__init__()
        self._type = None
        self.model = Volume()
        self.name = name
        self.type = type

    # ------------------------------------------------------------------------------------- name

    @property
    def name(self):
        return self.model.name

    @name.setter
    def name(self, name=None):
        self.model.name = name

    # ------------------------------------------------------------------------------------- type

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, t=None):
        if t not in self.VALID_VOLUME_TYPES:
            raise SyntaxError('K8sVolume: type: [ {} ] is invalid.'.format(t))
        self._type = t
        setattr(self.model, t, Volume.vol_type_to_source(t))

    # ------------------------------------------------------------------------------------- source

    @property
    def source(self):
        return getattr(self.model, self._type, None)

    @source.setter
    def source(self, s=None):
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------- medium (emptyDir)

    @property
    def medium(self):
        if not hasattr(self.source, 'medium'):
            raise NotImplementedError()
        return self.source.medium

    @medium.setter
    def medium(self, m=None):
        if not hasattr(self.source, 'medium'):
            raise NotImplementedError()
        self.source.medium = m

    # ------------------------------------------------------------------------------------- path (hostPath)

    @property
    def path(self):
        if not hasattr(self.source, 'path'):
            raise NotImplementedError()
        return self.source.path

    @path.setter
    def path(self, p=None):
        if not hasattr(self.source, 'path'):
            raise NotImplementedError()
        self.source.path = p

    # ------------------------------------------------------------------------------------- secret_name (secret)

    @property
    def secret_name(self):
        if not hasattr(self.source, 'secret_name'):
            raise NotImplementedError()
        return self.source.secret_name

    @secret_name.setter
    def secret_name(self, sn=None):
        if not hasattr(self.source, 'secret_name'):
            raise NotImplementedError()
        self.source.secret_name = sn

    # ------------------------------------------------------------------------------------- volume_id (AWS)

    # http://kubernetes.io/docs/user-guide/volumes/#awselasticblockstore
    # - the nodes on which pods are running must be AWS EC2 instances
    # - those instances need to be in the same region and availability-zone as the EBS volume
    # - EBS only supports a single EC2 instance mounting a volume

    # Pod creation will timeout waiting for readiness if not on AWS; unschedulable.

    @property
    def volume_id(self):
        if not hasattr(self.source, 'volume_id'):
            raise NotImplementedError()
        return self.source.volume_id

    @volume_id.setter
    def volume_id(self, vid=None):
        if not hasattr(self.source, 'volume_id'):
            raise NotImplementedError()
        self.source.volume_id = vid

    # ------------------------------------------------------------------------------------- pd_name (GCE)

    # http://kubernetes.io/docs/user-guide/volumes/#gcepersistentdisk
    # - the nodes on which pods are running must be GCE VMs
    # - those VMs need to be in the same GCE project and zone as the PD

    # Pod creation will timeout waiting for readiness if not on GCE; unschedulable.

    @property
    def pd_name(self):
        if not hasattr(self.source, 'pd_name'):
            raise NotImplementedError()
        return self.source.pd_name

    @pd_name.setter
    def pd_name(self, pd=None):
        if not hasattr(self.source, 'pd_name'):
            raise NotImplementedError()
        self.source.pd_name = pd

    # ------------------------------------------------------------------------------------- read_only (GCE)

    # HTTP 422: GCE PD can only be mounted on multiple machines if it is read-only

    @property
    def read_only(self):
        if not hasattr(self.source, 'read_only'):
            raise NotImplementedError()
        return self.source.read_only

    @read_only.setter
    def read_only(self, ro=None):
        if not hasattr(self.source, 'read_only'):
            raise NotImplementedError()
        self.source.read_only = ro

    # ------------------------------------------------------------------------------------- fs_type (AWS, GCE)

    @property
    def fs_type(self):
        if not hasattr(self.source, 'fs_type'):
            raise NotImplementedError()
        return self.source.fs_type

    @fs_type.setter
    def fs_type(self, t=None):
        if not hasattr(self.source, 'fs_type'):
            raise NotImplementedError()
        self.source.fs_type = t

    # ------------------------------------------------------------------------------------- nfs_server

    @property
    def nfs_server(self):
        if not hasattr(self.source, 'server'):
            raise NotImplementedError()
        return self.source.server

    @nfs_server.setter
    def nfs_server(self, s=None):
        if not hasattr(self.source, 'server'):
            raise NotImplementedError()
        self.source.server = s

    # ------------------------------------------------------------------------------------- nfs_path

    @property
    def nfs_path(self):
        if not hasattr(self.source, 'path'):
            raise NotImplementedError()
        return self.source.path

    @nfs_path.setter
    def nfs_path(self, p=None):
        if not hasattr(self.source, 'path'):
            raise NotImplementedError()
        self.source.path = p

    # ------------------------------------------------------------------------------------- git_repository

    @property
    def git_repository(self):
        if not hasattr(self.source, 'repository'):
            raise NotImplementedError()
        return self.source.repository

    @git_repository.setter
    def git_repository(self, repo=None):
        if not hasattr(self.source, 'repository'):
            raise NotImplementedError()
        self.source.repository = repo

    # ------------------------------------------------------------------------------------- git_revision

    @property
    def git_revision(self):
        if not hasattr(self.source, 'revision'):
            raise NotImplementedError()
        return self.source.revision

    @git_revision.setter
    def git_revision(self, rev=None):
        if not hasattr(self.source, 'revision'):
            raise NotImplementedError()
        self.source.revision = rev

    # ------------------------------------------------------------------------------------- claimName

    @property
    def claim_name(self):
        if not hasattr(self.source, 'claim_name'):
            raise NotImplementedError()
        return self.source.claim_name

    @claim_name.setter
    def claim_name(self, name=None):
        if not hasattr(self.source, 'claim_name'):
            raise NotImplementedError()
        self.source.claim_name = name

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

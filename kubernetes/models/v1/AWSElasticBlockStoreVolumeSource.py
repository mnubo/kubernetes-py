#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.utils import is_valid_string, filter_model


class AWSElasticBlockStoreVolumeSource(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_awselasticblockstorevolumesource

    An AWS EBS disk with the specified volume-id must exist before mounting to a container.
    """

    def __init__(self, model=None):
        super(AWSElasticBlockStoreVolumeSource, self).__init__()

        self._fs_type = None
        self._partition = None
        self._read_only = None
        self._volume_id = None

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def _build_with_model(self, model=None):
        if 'fsType' in model:
            self.fs_type = model['fsType']
        if 'partition' in model:
            self.partition = model['partition']
        if 'readOnly' in model:
            self.read_only = model['readOnly']
        if 'volumeID' in model:
            self.volume_id = model['volumeID']

    # ------------------------------------------------------------------------------------- fs type

    @property
    def fs_type(self):
        return self._fs_type

    @fs_type.setter
    def fs_type(self, fs=None):
        if not is_valid_string(fs):
            raise SyntaxError('AWSElasticBlockStoreVolumeSource: fs_type: [ {0} ] is invalid.'.format(fs))
        self._fs_type = fs

    # ------------------------------------------------------------------------------------- partition

    @property
    def partition(self):
        return self._partition

    @partition.setter
    def partition(self, partition=None):
        if not isinstance(partition, int):
            raise SyntaxError('AWSElasticBlockStoreVolumeSource: partition: [ {0} ] is invalid.'.format(partition))
        self._partition = partition

    # ------------------------------------------------------------------------------------- read only

    @property
    def read_only(self):
        return self._read_only

    @read_only.setter
    def read_only(self, ro=None):
        if not isinstance(ro, bool):
            raise SyntaxError('AWSElasticBlockStoreVolumeSource: read_only: [ {0} ] is invalid.'.format(ro))
        self._read_only = ro

    # ------------------------------------------------------------------------------------- volume id

    @property
    def volume_id(self):
        return self._volume_id

    @volume_id.setter
    def volume_id(self, vid=None):
        if not is_valid_string(vid):
            raise SyntaxError('AWSElasticBlockStoreVolumeSource: volume_id: [ {0} ] is invalid.'.format(vid))
        self._volume_id = vid

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.fs_type is not None:
            data['fsType'] = self.fs_type
        if self.partition is not None:
            data['partition'] = self.partition
        if self.read_only is not None:
            data['readOnly'] = self.read_only
        if self.volume_id is not None:
            data['volumeID'] = self.volume_id
        return data

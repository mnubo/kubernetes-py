#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.PersistentVolumeSpec import PersistentVolumeSpec
from kubernetes.models.v1.ResourceRequirements import ResourceRequirements
from kubernetes.models.v1beta1.LabelSelector import LabelSelector
from kubernetes.utils import is_valid_list, is_valid_string


class PersistentVolumeClaimSpec(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_persistentvolumeclaimspec
    """

    VALID_RESOURCES = ['storage']

    def __init__(self, model=None):
        super(PersistentVolumeClaimSpec, self).__init__()

        self._access_modes = []
        self._selector = LabelSelector()
        self._resources = ResourceRequirements()
        self._volume_name = None

        self.access_modes = ['ReadWriteOnce']
        self.resources.requests = {'storage': '10Gi'}

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'accessModes' in model:
            self.access_modes = model['accessModes']
        if 'selector' in model:
            self.selector = LabelSelector(model['selector'])
        if 'resources' in model:
            self.resources = ResourceRequirements(model['resources'])
        if 'volumeName' in model:
            self.volume_name = model['volumeName']

    # ------------------------------------------------------------------------------------- accessModes

    @property
    def access_modes(self):
        return self._access_modes

    @access_modes.setter
    def access_modes(self, modes=None):
        if not is_valid_list(modes, str):
            raise SyntaxError('PersistentVolumeClaimSpec: access_modes: [ {} ] is invalid.'.format(modes))
        filtered = list(filter(lambda x: x in PersistentVolumeSpec.VALID_ACCESS_MODES, modes))
        self._access_modes = filtered

    # ------------------------------------------------------------------------------------- selector

    @property
    def selector(self):
        return self._selector

    @selector.setter
    def selector(self, sel=None):
        if not isinstance(sel, LabelSelector):
            raise SyntaxError('PersistentVolumeClaimSpec: selector: [ {} ] is invalid.'.format(sel))
        self._selector = sel

    # ------------------------------------------------------------------------------------- resources

    @property
    def resources(self):
        return self._resources

    @resources.setter
    def resources(self, res=None):
        if not isinstance(res, ResourceRequirements):
            raise SyntaxError('PersistentVolumeClaimSpec: resources: [ {} ] is invalid.'.format(res))
        self._resources = res

    # ------------------------------------------------------------------------------------- volumeName

    @property
    def volume_name(self):
        return self._volume_name

    @volume_name.setter
    def volume_name(self, name=None):
        if not is_valid_string(name):
            raise SyntaxError('PersistentVolumeClaimSpec: volume_name: [ {} ] is invalid.'.format(name))
        self._volume_name = name

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.access_modes is not None:
            data['accessModes'] = self.access_modes
        if self.selector is not None:
            data['selector'] = self.selector.serialize()
        if self.resources is not None:
            data['resources'] = self.resources.serialize()
        if self.volume_name is not None:
            data['volumeName'] = self.volume_name
        return data
#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#
from kubernetes.utils import filter_model


class NodeSystemInfo(object):
    """
    https://kubernetes.io/docs/api-reference/v1/definitions/#_v1_nodesysteminfo
    """

    def __init__(self, model=None):
        super(NodeSystemInfo, self).__init__()

        self._machine_id = None
        self._system_uuid = None
        self._boot_id = None
        self._kernel_version = None
        self._os_image = None
        self._container_runtime_version = None
        self._kubelet_version = None
        self._kube_proxy_version = None
        self._operating_system = None
        self._architecture = None

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def _build_with_model(self, model=None):
        if 'machineID' in model:
            self.machine_id = model['machineID']
        if 'systemUUID' in model:
            self.system_uuid = model['systemUUID']
        if 'bootID' in model:
            self.boot_id = model['bootID']
        if 'kernelVersion' in model:
            self.kernel_version = model['kernelVersion']
        if 'osImage' in model:
            self.os_image = model['osImage']
        if 'containerRuntimeVersion' in model:
            self.container_runtime_version = model['containerRuntimeVersion']
        if 'kubeletVersion' in model:
            self.kubelet_version = model['kubeletVersion']
        if 'kubeProxyVersion' in model:
            self.kube_proxy_version = model['kubeProxyVersion']
        if 'operatingSystem' in model:
            self.operating_system = model['operatingSystem']
        if 'architecture' in model:
            self.architecture = model['architecture']

    # ------------------------------------------------------------------------------------- machine_id

    @property
    def machine_id(self):
        return self._machine_id

    @machine_id.setter
    def machine_id(self, v):
        if not isinstance(v, str):
            raise SyntaxError('NodeSystemInfo: machine_id: [ {0} ] is invalid.'.format(v))
        self._machine_id = v

    # ------------------------------------------------------------------------------------- machine_id

    @property
    def system_uuid(self):
        return self._system_uuid

    @system_uuid.setter
    def system_uuid(self, v):
        if not isinstance(v, str):
            raise SyntaxError('NodeSystemInfo: system_uuid: [ {0} ] is invalid.'.format(v))
        self._system_uuid = v

    # ------------------------------------------------------------------------------------- boot_id

    @property
    def boot_id(self):
        return self._boot_id

    @boot_id.setter
    def boot_id(self, v):
        if not isinstance(v, str):
            raise SyntaxError('NodeSystemInfo: boot_id: [ {0} ] is invalid.'.format(v))
        self._boot_id = v

    # ------------------------------------------------------------------------------------- kernel_version

    @property
    def kernel_version(self):
        return self._kernel_version

    @kernel_version.setter
    def kernel_version(self, v):
        if not isinstance(v, str):
            raise SyntaxError('NodeSystemInfo: kernel_version: [ {0} ] is invalid.'.format(v))
        self._kernel_version = v

    # ------------------------------------------------------------------------------------- os_image

    @property
    def os_image(self):
        return self._os_image

    @os_image.setter
    def os_image(self, v):
        if not isinstance(v, str):
            raise SyntaxError('NodeSystemInfo: os_image: [ {0} ] is invalid.'.format(v))
        self._os_image = v

    # ------------------------------------------------------------------------------------- container_runtime_version

    @property
    def container_runtime_version(self):
        return self._container_runtime_version

    @container_runtime_version.setter
    def container_runtime_version(self, v):
        if not isinstance(v, str):
            raise SyntaxError('NodeSystemInfo: container_runtime_version: [ {0} ] is invalid.'.format(v))
        self._container_runtime_version = v

    # ------------------------------------------------------------------------------------- kubelet_version

    @property
    def kubelet_version(self):
        return self._kubelet_version

    @kubelet_version.setter
    def kubelet_version(self, v):
        if not isinstance(v, str):
            raise SyntaxError('NodeSystemInfo: kubelet_version: [ {0} ] is invalid.'.format(v))
        self._kubelet_version = v

    # ------------------------------------------------------------------------------------- kube_proxy_version

    @property
    def kube_proxy_version(self):
        return self._kube_proxy_version

    @kube_proxy_version.setter
    def kube_proxy_version(self, v):
        if not isinstance(v, str):
            raise SyntaxError('NodeSystemInfo: kube_proxy_version: [ {0} ] is invalid.'.format(v))
        self._kube_proxy_version = v

    # ------------------------------------------------------------------------------------- operating_system

    @property
    def operating_system(self):
        return self._operating_system

    @operating_system.setter
    def operating_system(self, v):
        if not isinstance(v, str):
            raise SyntaxError('NodeSystemInfo: operating_system: [ {0} ] is invalid.'.format(v))
        self._operating_system = v

    # ------------------------------------------------------------------------------------- architecture

    @property
    def architecture(self):
        return self._architecture

    @architecture.setter
    def architecture(self, v):
        if not isinstance(v, str):
            raise SyntaxError('NodeSystemInfo: architecture: [ {0} ] is invalid.'.format(v))
        self._architecture = v

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.machine_id:
            data['machineID'] = self.machine_id
        if self.system_uuid:
            data['systemUUID'] = self.system_uuid
        if self.boot_id:
            data['bootID'] = self.boot_id
        if self.kernel_version:
            data['kernelVersion'] = self.kernel_version
        if self.os_image:
            data['osImage'] = self.os_image
        if self.container_runtime_version:
            data['containerRuntimeVersion'] = self.container_runtime_version
        if self.kubelet_version:
            data['kubeletVersion'] = self.kubelet_version
        if self.kube_proxy_version:
            data['kubeProxyVersion'] = self.kube_proxy_version
        if self.operating_system:
            data['operatingSystem'] = self.operating_system
        if self.architecture:
            data['architecture'] = self.architecture
        return data

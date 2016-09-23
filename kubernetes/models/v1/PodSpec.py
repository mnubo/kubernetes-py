#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.K8sVolume import K8sVolume
from kubernetes.K8sExceptions import AlreadyExistsException, UnprocessableEntityException
from kubernetes.models.v1.BaseModel import BaseModel
from kubernetes.models.v1.Container import Container


class PodSpec(BaseModel):
    def __init__(self, name=None, image=None, model=None, pull_secret=None):
        BaseModel.__init__(self)
        self.containers = list()

        if model is not None:
            if not isinstance(model, dict):
                raise SyntaxError('PodSpec: model: [ {0} ] must be a dict.'.format(model.__class__.__name__))

            if 'status' in self.model:
                self.model.pop('status', None)

            self.model = model

            for c in self.model['containers']:
                self.containers.append(Container(model=c))
            if 'volumes' not in self.model:
                self.model['volumes'] = []

        else:
            self.model = {
                "containers": [],
                "dnsPolicy": "Default",
                "volumes": []
            }

            if name is not None and not isinstance(name, str):
                raise SyntaxError('PodSpec: name: [ {0} ] must be a string.'.format(name.__class__.__name__))
            if image is not None and not isinstance(image, str):
                self.containers.append(Container(name=name, image=image))

            if pull_secret is not None:
                if not isinstance(pull_secret, str):
                    raise SyntaxError('PodSpec: pull_secret: [ {0} ] must be a string.'.format(pull_secret.__class__.__name__))
                self.add_image_pull_secrets(name=pull_secret)

            self._update_model()

    # ------------------------------------------------------------------------------------- private methods

    def _update_model(self):
        self.model['containers'] = []
        for c in self.containers:
            assert isinstance(c, Container)
            self.model['containers'].append(c.get())

    # ------------------------------------------------------------------------------------- add

    def add_container(self, container=None):
        if container is None or not isinstance(container, Container):
            raise SyntaxError('PodSpec: container should be a container object.')
        else:
            self.containers.append(container)
            self._update_model()
        return self

    def add_volume(self, volume=None):
        if volume is None:
            raise SyntaxError('PodSpec: volume: [ {0} ] cannot be None.'.format(volume))
        if not isinstance(volume, K8sVolume):
            raise SyntaxError('PodSpec: volume: [ {0} ] must be a K8sVolume'.format(volume))

        volnames = [x['name'] for x in self.model['volumes']]
        if volume.name in volnames:
            raise AlreadyExistsException('PodSpec: volume: [ {0} ] already exists.'.format(volume.name))

        if volume.type == "hostPath" and volume.host_path is None:
            msg = 'PodSpec: volume: [ {0} ] cannot be added; please set a hostPath.'.format(volume.name)
            raise UnprocessableEntityException(msg)

        vol = {
            'name': volume.name,
            '{0}'.format(volume.type): {}
        }

        if volume.type == 'emptyDir' and volume.medium != '':
            vol[volume.type]['medium'] = volume.medium
        if volume.type == 'hostPath':
            vol[volume.type]['path'] = volume.host_path
        if volume.type == 'secret':
            vol[volume.type]['secretName'] = volume.secret_name
        if volume.type == 'awsElasticBlockStore':
            vol[volume.type]['volumeID'] = volume.aws_volume_id
            vol[volume.type]['fsType'] = volume.fs_type
        if volume.type == 'gcePersistentDisk':
            vol[volume.type]['pdName'] = volume.gce_pd_name
            vol[volume.type]['fsType'] = volume.fs_type
        if volume.read_only is True:
            vol[volume.type]['readOnly'] = True

        self.model['volumes'].append(vol)

    def add_image_pull_secrets(self, name=None):
        if name is None:
            raise SyntaxError('PodSpec: name: [ {0} ] cannot be None.'.format(name))
        if name is None or not isinstance(name, str):
            raise SyntaxError('PodSpec: name: [ {0} ] should be a string.'.format(name))
        if 'imagePullSecrets' not in self.model:
            self.model['imagePullSecrets'] = list()
        self.model['imagePullSecrets'].append(dict(name=name))
        return self

    # ------------------------------------------------------------------------------------- del

    def del_node_name(self):
        self.model.pop('nodeName', None)
        return self

    # ------------------------------------------------------------------------------------- get

    def get_containers(self):
        return self.containers

    def get_node_name(self):
        return self.model.get('nodeName', None)

    def get_node_selector(self):
        return self.model.get('nodeSelector', None)

    def get_restart_policy(self):
        return self.model.get('restartPolicy', None)

    def get_service_account(self):
        return self.model.get('serviceAccountName', None)

    def get_termination_grace_period(self):
        return self.model.get('terminationGracePeriodSeconds', None)

    # ------------------------------------------------------------------------------------- set

    def set_active_deadline(self, seconds=None):
        if seconds is None:
            raise SyntaxError('PodSpec: seconds: [ {0} ] cannot be None.'.format(seconds))
        if not isinstance(seconds, int) or seconds < 0:
            raise SyntaxError('PodSpec: seconds: [ {0} ] should be a positive integer.'.format(seconds))

        self.model['activeDeadlineSeconds'] = seconds
        return self

    def set_container_image(self, name=None, image=None):
        if image is None or not isinstance(image, str):
            raise SyntaxError('PodSpec: image should be a string.')
        if name is None or not isinstance(name, str):
            raise SyntaxError('PodSpec: name should be a string.')
        for c in self.containers:
            assert isinstance(c, Container)
            if c.get_name() == name:
                c.set_image(image=image)
                break
        return self

    def set_dns_policy(self, policy='Default'):
        if policy in ['Default', 'ClusterFirst']:
            self.model['dnsPolicy'] = policy
        else:
            raise SyntaxError('PodSpec: policy should be one of: Default, ClusterFirst')
        return self

    def set_node_selector(self, dico=None):
        if dico is None:
            raise SyntaxError('PodSpec: Node selector: [ {0} ] cannot be None.'.format(dico))
        if not isinstance(dico, dict):
            raise SyntaxError('PodSpec: Node selector: [ {0} ] must be a dict.'.format(dico))

        self.model['nodeSelector'] = dico
        return self

    def set_restart_policy(self, policy=None):
        if policy is None:
            raise SyntaxError('PodSpec: policy: [ {0} ] cannot be None.'.format(policy))
        if not isinstance(policy, str):
            raise SyntaxError('PodSpec: policy: [ {0} ] must be a string.'.format(policy))
        if policy not in ['Always', 'OnFailure', 'Never']:
            raise SyntaxError('PodSpec: policy: [ {0} ] must be in: [ \'Always\', \'OnFailure\', \'Never\' ]')

        self.model['restartPolicy'] = policy
        return self

    def set_service_account(self, name=None):
        if name is None or not isinstance(name, str):
            raise SyntaxError('PodSpec: name: [ {0} ] cannot be None.'.format(name))
        if not isinstance(name, str):
            raise SyntaxError('PodSpec: name: [ {0} ] must be a string.'.format(name))

        self.model['serviceAccountName'] = name
        return self

    def set_node_name(self, name=None):
        if name is None:
            raise SyntaxError('PodSpec: name: [ {0} ] cannot be None.'.format(name))
        if not isinstance(name, str):
            raise SyntaxError('PodSpec: name: [ {0} ] must be a string.'.format(name))

        self.model['nodeName'] = name
        return self

    def set_termination_grace_period(self, seconds=None):
        if seconds is None:
            raise SyntaxError('PodSpec: seconds: [ {0} ] cannot be None.'.format(seconds))
        if not isinstance(seconds, int) or not seconds > 0:
            raise SyntaxError('PodSpec: seconds: [ {0} ] must be a positive integer.'.format(seconds))

        self.model['terminationGracePeriodSeconds'] = seconds
        return self

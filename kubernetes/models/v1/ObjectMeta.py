#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1.OwnerReference import OwnerReference
from kubernetes.utils import is_valid_string, filter_model, is_valid_list, is_valid_dict


class ObjectMeta(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_objectmeta
    """

    def __init__(self, model=None):
        super(ObjectMeta, self).__init__()

        self._name = None
        self._generate_name = None
        self._namespace = None
        self._self_link = None
        self._uid = None
        self._resource_version = None
        self._generation = None
        self._creation_timestamp = None
        self._deletion_timestamp = None
        self._deletion_grace_period_seconds = None
        self._labels = {}
        self._annotations = {}
        self._owner_references = None
        self._finalizers = None
        self._cluster_name = None

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def _build_with_model(self, model=None):
        if 'name' in model:
            self.name = model['name']
        if 'generateName' in model:
            self.generate_name = model['generateName']
        if 'namespace' in model:
            self.namespace = model['namespace']
        if 'selfLink' in model:
            self.self_link = model['selfLink']
        if 'uid' in model:
            self.uid = model['uid']
        if 'resourceVersion' in model:
            self.resource_version = model['resourceVersion']
        if 'generation' in model:
            self.generation = model['generation']
        if 'creationTimestamp' in model:
            self.creation_timestamp = model['creationTimestamp']
        if 'deletionTimestamp' in model:
            self.deletion_timestamp = model['deletionTimestamp']
        if 'deletionGracePeriodSeconds' in model:
            self.deletion_grace_period_seconds = model['deletionGracePeriodSeconds']
        if 'labels' in model:
            self.labels = model['labels']
        if 'annotations' in model:
            self.annotations = model['annotations']
        if 'ownerReferences' in model:
            refs = []
            for o in model['ownerReferences']:
                ref = OwnerReference(o)
                refs.append(ref)
            self.owner_references = refs
        if 'finalizers' in model:
            self.finalizers = model['finalizers']
        if 'clusterName' in model:
            self.cluster_name = model['clusterName']

    # ------------------------------------------------------------------------------------- name

    def strip(self, kind=None):
        # self._name = None
        self._generate_name = None
        # self._namespace = None
        self._self_link = None
        self._uid = None
        if kind != 'Service':
            self._resource_version = None
        self._generation = None
        self._creation_timestamp = None
        self._deletion_timestamp = None
        self._deletion_grace_period_seconds = None
        # self._labels = {}
        # self._annotations = {}
        self._owner_references = None
        self._finalizers = None
        self._cluster_name = None

    # ------------------------------------------------------------------------------------- name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name=None):
        if not is_valid_string(name):
            raise SyntaxError('ObjectMeta: name: [ {0} ] is invalid.'.format(name))
        self._name = name

    # ------------------------------------------------------------------------------------- generate name

    @property
    def generate_name(self):
        return self._generate_name

    @generate_name.setter
    def generate_name(self, name=None):
        if not is_valid_string(name):
            raise SyntaxError('ObjectMeta: generate_name: [ {0} ] is invalid.'.format(name))
        self._generate_name = name

    # ------------------------------------------------------------------------------------- namespace

    @property
    def namespace(self):
        return self._namespace

    @namespace.setter
    def namespace(self, namespace=None):
        if not is_valid_string(namespace):
            raise SyntaxError('ObjectMeta: namespace: [ {0} ] is invalid.'.format(namespace))
        self._namespace = namespace

    # ------------------------------------------------------------------------------------- selfLink

    @property
    def self_link(self):
        return self._self_link

    @self_link.setter
    def self_link(self, link=None):
        if not is_valid_string(link):
            raise SyntaxError('ObjectMeta: self_link: [ {0} ] is invalid.'.format(link))
        self._self_link = link

    # ------------------------------------------------------------------------------------- uid

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, uid=None):
        if uid is not None:
            if not is_valid_string(uid):
                raise SyntaxError('ObjectMeta: uid: [ {0} ] is invalid.'.format(uid))
        self._uid = uid

    # ------------------------------------------------------------------------------------- resourceVersion

    @property
    def resource_version(self):
        return self._resource_version

    @resource_version.setter
    def resource_version(self, v=None):
        if v is not None:
            if not isinstance(v, str):
                raise SyntaxError('ObjectMeta: resource_version: [ {0} ] is invalid.'.format(v))
        self._resource_version = v

    # ------------------------------------------------------------------------------------- generation

    @property
    def generation(self):
        return self._generation

    @generation.setter
    def generation(self, gen=None):
        if not isinstance(gen, int):
            raise SyntaxError('ObjectMeta: generation: [ {0} ] is invalid.'.format(gen))
        self._generation = gen

    # ------------------------------------------------------------------------------------- creationTimestamp

    @property
    def creation_timestamp(self):
        return self._creation_timestamp

    @creation_timestamp.setter
    def creation_timestamp(self, time=None):
        if not is_valid_string(time):
            raise SyntaxError('ObjectMeta: creation_timestamp: [ {0} ] is invalid.'.format(time))
        self._creation_timestamp = time

    # ------------------------------------------------------------------------------------- deletionTimestamp

    @property
    def deletion_timestamp(self):
        return self._deletion_timestamp

    @deletion_timestamp.setter
    def deletion_timestamp(self, time=None):
        if not is_valid_string(time):
            raise SyntaxError('ObjectMeta: deletion_timestamp: [ {0} ] is invalid.'.format(time))
        self._deletion_timestamp = time

    # ------------------------------------------------------------------------------------- deletionGracePeriodSeconds

    @property
    def deletion_grace_period_seconds(self):
        return self._deletion_grace_period_seconds

    @deletion_grace_period_seconds.setter
    def deletion_grace_period_seconds(self, secs=None):
        if not isinstance(secs, int):
            raise SyntaxError('ObjectMeta: deletion_grace_period_seconds: [ {0} ] is invalid.'.format(secs))
        self._deletion_grace_period_seconds = secs

    # ------------------------------------------------------------------------------------- labels

    @property
    def labels(self):
        return self._labels

    @labels.setter
    def labels(self, labels=None):
        if not is_valid_dict(labels, type=str):
            raise SyntaxError('ObjectMeta: labels: [ {0} ] is invalid.'.format(labels))
        self._labels = labels

    # ------------------------------------------------------------------------------------- annotations

    @property
    def annotations(self):
        return self._annotations

    @annotations.setter
    def annotations(self, anns=None):
        if not is_valid_dict(anns, str):
            raise SyntaxError('ObjectMeta: annotations: [ {0} ] is invalid.'.format(anns))
        self._annotations = anns

    # ------------------------------------------------------------------------------------- ownerReferences

    @property
    def owner_references(self):
        return self._owner_references

    @owner_references.setter
    def owner_references(self, refs=None):
        if not is_valid_list(refs, OwnerReference):
            raise SyntaxError('ObjectMeta: owner_references: [ {0} ] is invalid.'.format(refs))
        self._owner_references = refs

    # ------------------------------------------------------------------------------------- finalizers

    @property
    def finalizers(self):
        return self._finalizers

    @finalizers.setter
    def finalizers(self, f=None):
        if not is_valid_list(f, str):
            raise SyntaxError('ObjectMeta: finalizers: [ {0} ] is invalid.'.format(f))
        self._finalizers = f

    # ------------------------------------------------------------------------------------- clusterName

    @property
    def cluster_name(self):
        return self._cluster_name

    @cluster_name.setter
    def cluster_name(self, name=None):
        if not is_valid_string(name):
            raise SyntaxError('ObjectMeta: cluster_name: [ {0} ] is invalid.'.format(name))
        self._cluster_name = name

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.name:
            data['name'] = self.name
        if self.generate_name:
            data['generateName'] = self.generate_name
        if self.namespace:
            data['namespace'] = self.namespace
        if self.self_link:
            data['selfLink'] = self.self_link
        if self.uid:
            data['uid'] = self.uid
        if self.resource_version:
            data['resourceVersion'] = self.resource_version
        if self.generation:
            data['generation'] = self.generation
        if self.creation_timestamp:
            data['creationTimestamp'] = self.creation_timestamp
        if self.deletion_timestamp:
            data['deletionTimestamp'] = self.deletion_timestamp
        if self.deletion_grace_period_seconds:
            data['deletionGracePeriodSeconds'] = self.deletion_grace_period_seconds
        if self.labels:
            data['labels'] = self.labels
        if self.annotations:
            data['annotations'] = self.annotations
        if self.owner_references:
            data['ownerReferences'] = self.owner_references
        if self.finalizers:
            data['finalizers'] = self.finalizers
        if self.cluster_name:
            data['clusterName'] = self.cluster_name
        return data

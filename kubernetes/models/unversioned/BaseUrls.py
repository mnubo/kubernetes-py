#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#


class BaseUrls(object):
    """
    Wrapper around a map of URL endpoints for each K8sObject type.

    """

    default_api_version = 'v1'
    default_apps_version = 'v1alpha1'
    default_batch_version = 'v1'
    default_extensions_version = 'v1beta1'
    default_cron_version = 'v2alpha1'

    def __init__(self, namespace='default', api=None, apps=None, extensions=None, batch=None, cron=None):

        if api is None:
            api = self.default_api_version
        if apps is None:
            apps = self.default_apps_version
        if batch is None:
            batch = self.default_batch_version
        if extensions is None:
            extensions = self.default_extensions_version
        if cron is None:
            cron = self.default_cron_version

        self.urls = dict()

        # api
        self.urls['Pod'] = '/api/{0}/namespaces/{1}/pods'.format(api, namespace)
        self.urls['PersistentVolume'] = '/api/{0}/persistentvolumes'.format(api)
        self.urls['PersistentVolumeClaim'] = '/api/{0}/namespaces/{1}/persistentvolumeclaims'.format(api, namespace)
        self.urls['ReplicationController'] = '/api/{0}/namespaces/{1}/replicationcontrollers'.format(api, namespace)
        self.urls['Service'] = '/api/{0}/namespaces/{1}/services'.format(api, namespace)
        self.urls['Secret'] = '/api/{0}/namespaces/{1}/secrets'.format(api, namespace)

        # apps
        self.urls['PetSet'] = '/apis/apps/{0}/namespaces/{1}/petsets'.format(apps, namespace)

        # batch
        self.urls['Job'] = '/apis/batch/{0}/namespaces/{1}/jobs'.format(batch, namespace)
        self.urls['CronJob'] = '/apis/batch/{0}/namespaces/{1}/scheduledjobs'.format(cron, namespace)

        # extensions
        self.urls['DaemonSet'] = '/apis/extensions/{0}/namespaces/{1}/daemonsets'.format(extensions, namespace)
        self.urls['Deployment'] = '/apis/extensions/{0}/namespaces/{1}/deployments'.format(extensions, namespace)
        self.urls['ReplicaSet'] = '/apis/extensions/{0}/namespaces/{1}/replicasets'.format(extensions, namespace)

        # other
        self.urls['Volume'] = None

    def get_base_url(self, object_type=None):
        if object_type is None \
                or not isinstance(object_type, str) \
                or object_type not in self.urls.keys():
            types = ', '.join(self.urls.keys())
            raise SyntaxError('BaseUrls: object_type: [ {0} ] must be in: [ {1} ]'.format(object_type, types))
        return self.urls[object_type]

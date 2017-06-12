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
    default_autoscaling_version = 'v1'
    default_batch_version = 'v1'
    default_extensions_version = 'v1beta1'
    default_cron_version = 'v2alpha1'

    def __init__(self, namespace='default', api=None, apps=None, autoscaling=None, extensions=None, batch=None, cron=None):

        if api is None:
            api = self.default_api_version
        if apps is None:
            apps = self.default_apps_version
        if autoscaling is None:
            autoscaling = self.default_autoscaling_version
        if batch is None:
            batch = self.default_batch_version
        if extensions is None:
            extensions = self.default_extensions_version
        if cron is None:
            cron = self.default_cron_version

        self.urls = dict()

        # api
        self.urls['ComponentStatus'] = '/api/{0}/componentstatuses'.format(api)
        self.urls['Event'] = '/api/{0}/events'.format(api)
        self.urls['Namespace'] = '/api/{0}/namespaces'.format(api)
        self.urls['Node'] = '/api/{0}/nodes'.format(api)
        self.urls['Pod'] = '/api/{0}/namespaces/{1}/pods'.format(api, namespace)
        self.urls['PersistentVolume'] = '/api/{0}/persistentvolumes'.format(api)
        self.urls['PersistentVolumeClaim'] = '/api/{0}/namespaces/{1}/persistentvolumeclaims'.format(api, namespace)
        self.urls['ReplicationController'] = '/api/{0}/namespaces/{1}/replicationcontrollers'.format(api, namespace)
        self.urls['Service'] = '/api/{0}/namespaces/{1}/services'.format(api, namespace)
        self.urls['ServiceAccount'] = '/api/{0}/namespaces/{1}/serviceaccounts'.format(api, namespace)
        self.urls['Secret'] = '/api/{0}/namespaces/{1}/secrets'.format(api, namespace)
        self.urls['StorageClass'] = '/apis/storage.k8s.io/v1beta1/storageclasses'

        # autoscaling
        self.urls['HorizontalPodAutoscaler'] = '/apis/autoscaling/{0}/namespaces/{1}/horizontalpodautoscalers'.format(autoscaling, namespace)

        # apps
        self.urls['PetSet'] = '/apis/apps/v1alpha1/namespaces/{}/petsets'.format(namespace)
        self.urls['StatefulSet'] = '/apis/apps/v1beta1/namespaces/{}/statefulsets'.format(namespace)

        # batch
        self.urls['Job'] = '/apis/batch/{0}/namespaces/{1}/jobs'.format(batch, namespace)
        self.urls['ScheduledJob'] = '/apis/batch/{0}/namespaces/{1}/scheduledjobs'.format(cron, namespace)
        self.urls['CronJob'] = '/apis/batch/{0}/namespaces/{1}/cronjobs'.format(cron, namespace)

        # extensions
        self.urls['DaemonSet'] = '/apis/extensions/{0}/namespaces/{1}/daemonsets'.format(extensions, namespace)
        self.urls['Deployment'] = '/apis/extensions/{0}/namespaces/{1}/deployments'.format(extensions, namespace)
        self.urls['ReplicaSet'] = '/apis/extensions/{0}/namespaces/{1}/replicasets'.format(extensions, namespace)

        # other
        self.urls['Volume'] = None

    def get_base_url(self, object_type=None):
        if object_type is None or object_type not in self.urls.keys():
            types = ', '.join(self.urls.keys())
            raise SyntaxError('BaseUrls: object_type: [ {0} ] must be in: [ {1} ]'.format(object_type, types))
        return self.urls[object_type]

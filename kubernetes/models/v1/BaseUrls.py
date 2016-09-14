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

    def __init__(self, namespace='default', api_version='v1', extensions_api_version='v1beta1'):
        self.urls = dict()
        self.urls['Deployment'] = '/apis/extensions/{0}/namespaces/{1}/deployments'.format(extensions_api_version, namespace)
        self.urls['Pod'] = '/api/{0}/namespaces/{1}/pods'.format(api_version, namespace)
        self.urls['Namespace'] = '/api/{0}/namespaces'.format(api_version)
        self.urls['ReplicaSet'] = '/apis/extensions/{0}/namespaces/{1}/replicasets'.format(extensions_api_version, namespace)
        self.urls['ReplicationController'] = '/api/{0}/namespaces/{1}/replicationcontrollers'.format(api_version, namespace)
        self.urls['Service'] = '/api/{0}/namespaces/{1}/services'.format(api_version, namespace)
        self.urls['Secret'] = '/api/{0}/namespaces/{1}/secrets'.format(api_version, namespace)
        self.urls['Volume'] = None

    def get_base_url(self, object_type=None):
        if object_type is None or not isinstance(object_type, str) or object_type not in self.urls.keys():
            types = ', '.join(self.urls.keys())
            raise SyntaxError('object_type: [ {0} ] must be in: [ {1} ]'.format(object_type, types))
        return self.urls[object_type]

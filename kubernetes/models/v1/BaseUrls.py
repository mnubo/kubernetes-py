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

    def __init__(self, namespace='default', version='v1'):
        self.urls = dict()
        self.urls['Pod'] = '/api/{0}/namespaces/{1}/pods'.format(version, namespace)
        self.urls['ReplicationController'] = '/api/{0}/namespaces/{1}/replicationcontrollers'.format(version, namespace)
        self.urls['Service'] = '/api/{0}/namespaces/{1}/services'.format(version, namespace)
        self.urls['Secret'] = '/api/{0}/namespaces/{1}/secrets'.format(version, namespace)

    def get_base_url(self, object_type=None):
        if object_type is None or not isinstance(object_type, str) or object_type not in self.urls.keys():
            types = ', '.join(self.urls.keys())
            raise SyntaxError('Please specify object_type: [ {0} ] in: [ {1} ]'.format(object_type, types))
        return self.urls[object_type]

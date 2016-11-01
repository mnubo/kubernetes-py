#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#


class LoadBalancerIngress(object):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_loadbalanceringress
    """

    def __init__(self):
        super(LoadBalancerIngress, self).__init__()
        self.ip = None
        self.hostname = None

    # ------------------------------------------------------------------------------------- serialize

    def json(self):
        data = {}
        if self.ip is not None:
            data['ip'] = self.ip
        if self.hostname is not None:
            data['hostname'] = self.hostname
        return data

#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import socket
from kubernetes.models.v1.BaseModel import BaseModel
from kubernetes.models.v1.ObjectMeta import ObjectMeta


class Service(BaseModel):
    def __init__(self, name=None, namespace='default', port_name=None, port=0,
                 target_port=None, selector=None, session_affinity='None', model=None):
        BaseModel.__init__(self)

        if model is not None:
            assert isinstance(model, dict)
            self.model = model
            if 'status' in self.model:
                self.model.pop('status', None)
            self.svc_metadata = ObjectMeta(model=self.model['metadata'], del_server_attr=False)

        else:
            self.model = dict(kind='Service', apiVersion='v1')
            self.svc_metadata = ObjectMeta(name=name, namespace=namespace)
            self.model['spec'] = dict(ports=[], selector=dict(), sessionAffinity=session_affinity, type='ClusterIP')
            if port_name is not None and port > 0 and target_port is not None:
                self.add_port(port=port, target_port=target_port, name=port_name)
            if selector is not None:
                self.add_selector(selector=selector)
            self._update_model()

    def _update_model(self):
        self.model['metadata'] = self.svc_metadata.get()
        return self

    # ------------------------------------------------------------------------------------- add

    def add_label(self, k, v):
        self.svc_metadata.add_label(k=k, v=v)
        return self

    def add_annotation(self, k, v):
        self.svc_metadata.add_annotation(k=k, v=v)
        return self

    def add_port(self, port=None, name=None, target_port=None, protocol=None, node_port=None):
        if port is not None:
            if not isinstance(port, int) or not 0 < port < 65536:
                raise SyntaxError('Service: port: [ {0} ] must be a positive integer.'.format(port))
        if name is not None:
            if not isinstance(name, str):
                raise SyntaxError('Service: name: [ {0} ] must be a string.'.format(name))
        if target_port is not None:
            if (not isinstance(target_port, str) and not isinstance(target_port, int)) or not 0 < target_port < 65536:
                raise SyntaxError('Service: target_port: [ {0} ] must be either a string or a positive integer.'.format(target_port))
        if protocol is not None:
            if not isinstance(protocol, str):
                raise SyntaxError('Service: protocol: [ {0} ] must be a string.'.format(protocol.__class__.__name__))
            if protocol.upper() not in ['TCP', 'UDP']:
                raise SyntaxError('Service: protocol: [ {0} ] must be either: [ \'TCP\', \'UDP\' ]'.format(protocol))
        if node_port is not None:
            if not isinstance(node_port, int) or not 0 < node_port < 65536:
                raise SyntaxError('Service: node_port: [ {0} ] should be a positive integer.'.format(node_port))

        my_port = dict()
        if port:
            my_port['port'] = port
        if name:
            my_port['name'] = name
        if protocol:
            my_port['protocol'] = protocol.upper()
        if target_port:
            my_port['targetPort'] = target_port
        if node_port:
            my_port['nodePort'] = node_port

        if len(my_port) > 0:
            self.model['spec']['ports'].append(my_port)

        return self

    def add_selector(self, selector=None):
        if selector is None:
            raise SyntaxError('Service: selector: [ {0} ] cannot be None.'.format(selector))
        if not isinstance(selector, dict):
            raise SyntaxError('Service: selector: [ {0} ] must be a dict.')
        for k, v in selector.iteritems():
            if not isinstance(k, str) or not isinstance(v, str):
                raise SyntaxError("Service: selector: [ {0} ] must be a dict of str to str.".format(selector))

        if 'selector' not in self.model['spec']:
            self.model['spec']['selector'] = dict()

        self.model['spec']['selector'].update(selector)
        return self

    # ------------------------------------------------------------------------------------- del

    def del_annotation(self, k):
        self.svc_metadata.del_annotation(k=k)
        return self

    def del_label(self, k):
        self.svc_metadata.del_label(k=k)
        return self

    def del_meta_creation_timestamp(self):
        self.svc_metadata.del_creation_timestamp()
        return self

    def del_meta_generation(self):
        self.svc_metadata.del_generation()
        return self

    def del_meta_resource_version(self):
        self.svc_metadata.del_resource_version()
        return self

    def del_meta_self_link(self):
        self.svc_metadata.del_self_link()
        return self

    def del_meta_uid(self):
        self.svc_metadata.del_uid()
        return self

    def del_server_generated_meta_attr(self):
        self.svc_metadata.del_server_generated_meta_attr()
        return self

    # ------------------------------------------------------------------------------------- get

    def get_annotation(self, k=None):
        return self.svc_metadata.get_annotation(k=k)

    def get_annotations(self):
        return self.svc_metadata.get_annotations()

    def get_cluster_ip(self):
        if 'clusterIP' in self.model['spec']:
            return self.model['spec']['clusterIP']
        return None

    def get_external_ips(self):
        if 'externalIPs' in self.model['spec']:
            return self.model['spec']['externalIPs']
        return None

    def get_label(self, k=None):
        return self.svc_metadata.get_label(k=k)

    def get_labels(self):
        return self.svc_metadata.get_labels()

    def get_name(self):
        return self.svc_metadata.get_name()

    def get_namespace(self):
        return self.svc_metadata.get_namespace()

    def get_meta_creation_timestamp(self):
        return self.svc_metadata.get_creation_timestamp()

    def get_meta_generation(self):
        return self.svc_metadata.get_generation()

    def get_meta_resource_version(self):
        return self.svc_metadata.get_resource_version()

    def get_meta_self_link(self):
        return self.svc_metadata.get_self_link()

    def get_meta_uid(self):
        return self.svc_metadata.get_uid()

    # ------------------------------------------------------------------------------------- set

    def set_annotations(self, dico):
        self.svc_metadata.set_annotations(dico=dico)
        return self

    def set_cluster_ip(self, ip=None):
        if ip is None:
            raise SyntaxError('Service: clusterIP: [ {0} ] cannot be None.'.format(ip))
        if not isinstance(ip, str):
            raise SyntaxError('Service: clusterIP: [ {0} ] must be a string.'.format(ip))

        try:
            socket.inet_aton(ip)
        except socket.error:
            raise SyntaxError('Service: clusterIP: [ {0} ] is not a valid IP address.'.format(ip))

        self.model['spec']['clusterIP'] = ip
        return self

    def set_external_ips(self, ips=None):
        if ips is None:
            raise SyntaxError('Service: ips: [ {0} ] cannot be None.'.format(ips))
        if not isinstance(ips, list):
            raise SyntaxError('Service: ips: [ {0} ] must be a list of IP addresses.'.format(ips.__class__.__name__))

        for ip in ips:
            if not isinstance(ip, str):
                raise SyntaxError('Service: ips: [ {0} ] contains an element which isn\'t a string.'.format(ips))
            try:
                socket.inet_aton(ip)
            except socket.error:
                raise SyntaxError('Service: ips: [ {0} ] contains an invalid IP address.'.format(ips))

        self.model['spec']['externalIPs'] = ips
        return self

    def set_labels(self, dico):
        self.svc_metadata.set_labels(dico=dico)
        return self

    def set_load_balancer_ip(self, ip=None):
        if ip is None:
            raise SyntaxError('Service: loadBalancerIP: [ {0} ] cannot be None.'.format(ip))
        if not isinstance(ip, str):
            raise SyntaxError('Service: loadBalancerIP: [ {0} ] must be a string.'.format(ip))

        try:
            socket.inet_aton(ip)
        except socket.error:
            raise SyntaxError('Service: loadBalancerIP: [ {0} ] is not a valid IP address.'.format(ip))

        self.model['spec']['loadBalancerIP'] = ip
        return self

    def set_meta_creation_timestamp(self, ts=None):
        return self.svc_metadata.set_creation_timestamp(ts=ts)

    def set_meta_generation(self, gen=None):
        return self.svc_metadata.set_generation(gen=gen)

    def set_meta_resource_version(self, ver):
        return self.svc_metadata.set_resource_version(ver=ver)

    def set_meta_self_link(self, link):
        return self.svc_metadata.set_self_link(link=link)

    def set_meta_uid(self, uid):
        return self.svc_metadata.set_uid(uid=uid)

    def set_name(self, name):
        assert isinstance(name, str)
        self.svc_metadata.set_name(name=name)
        return self

    def set_namespace(self, name):
        self.svc_metadata.set_namespace(name=name)
        return self

    def set_session_affinity(self, affinity_type=None):
        if affinity_type is None:
            raise SyntaxError('Service: affinity_type: [ {0} ] cannot be None.'.format(affinity_type))
        if affinity_type not in ['None', 'ClientIP']:
            raise SyntaxError('Service: affinity_type: [ {0} ] must be in: [ \'None\', \'ClientIP\' ]')
        self.model['spec']['sessionAffinity'] = affinity_type
        return self

    def set_service_type(self, service_type=None):
        if service_type is None:
            raise SyntaxError('Service: service_type: [ {0} ] cannot be None.'.format(service_type))
        if service_type not in ['ClusterIP', 'NodePort', 'LoadBalancer']:
            raise SyntaxError('Service: service_type: [ {0} ] must be in: [ \'ClusterIP\', \'NodePort\', \'LoadBalancer\' ]')
        self.model['spec']['type'] = service_type
        return self

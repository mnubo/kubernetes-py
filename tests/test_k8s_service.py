#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import time
import uuid

from tests import _utils
from tests.BaseTest import BaseTest
from kubernetes import K8sService, K8sConfig
from kubernetes.K8sExceptions import *
from kubernetes.models.v1.ObjectMeta import ObjectMeta
from kubernetes.models.v1.Service import Service
from kubernetes.models.v1.ServiceSpec import ServiceSpec
from kubernetes.models.v1.ServiceStatus import ServiceStatus


class K8sServiceTest(BaseTest):

    def setUp(self):
        _utils.cleanup_services()

    def tearDown(self):
        _utils.cleanup_services()

    # --------------------------------------------------------------------------------- init

    def test_init_no_args(self):
        try:
            K8sService()
            self.fail("Should not fail.")
        except SyntaxError:
            pass
        except IOError:
            pass
        except Exception as err:
            self.fail("Unhandled exception: [ {0} ]".format(err.__class__.__name__))

    def test_init_with_invalid_config(self):
        config = object()
        with self.assertRaises(SyntaxError):
            K8sService(config=config)

    def test_init_with_invalid_name(self):
        name = object()
        with self.assertRaises(SyntaxError):
            _utils.create_service(name=name)

    def test_init_with_name(self):
        name = "yoname"
        svc = _utils.create_service(name=name)
        self.assertIsNotNone(svc)
        self.assertIsInstance(svc, K8sService)
        self.assertEqual('Service', svc.obj_type)
        self.assertEqual(svc.name, name)
        self.assertIsInstance(svc.config, K8sConfig)

    def test_init_with_name_and_config(self):
        nspace = "yonamespace"
        config = K8sConfig(kubeconfig=_utils.kubeconfig_fallback, namespace=nspace)
        name = "yoname"
        svc = _utils.create_service(config=config, name=name)
        self.assertIsNotNone(svc)
        self.assertIsInstance(svc, K8sService)
        self.assertEqual(svc.name, name)
        self.assertEqual('Service', svc.obj_type)
        self.assertIsInstance(svc.config, K8sConfig)
        self.assertEqual(nspace, svc.config.namespace)

    # --------------------------------------------------------------------------------- struct

    def test_struct_k8s_service(self):
        name = "yoname"
        svc = _utils.create_service(name=name)
        self.assertIsInstance(svc, K8sService)
        self.assertIsInstance(svc.base_url, str)
        self.assertIsInstance(svc.config, K8sConfig)
        self.assertIsInstance(svc.model, Service)
        self.assertIsInstance(svc.name, str)
        self.assertIsInstance(svc.obj_type, str)

    def test_struct_service(self):
        name = "yoname"
        svc = _utils.create_service(name=name)
        self.assertIsInstance(svc, K8sService)
        self.assertIsInstance(svc.model, Service)
        self.assertIsInstance(svc.model.metadata, ObjectMeta)
        self.assertIsInstance(svc.model.spec, ServiceSpec)
        self.assertIsInstance(svc.model.status, ServiceStatus)

    # --------------------------------------------------------------------------------- add annotation

    def test_add_annotation_none_args(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        try:
            svc.add_annotation()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_add_annotation_invalid_args(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        k = object()
        v = object()
        try:
            svc.add_annotation(k, v)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_add_annotation(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        k = "yokey"
        v = "yovalue"
        svc.add_annotation(k, v)
        self.assertIn(k, svc.annotations)
        self.assertEqual(v, svc.annotations[k])

    # --------------------------------------------------------------------------------- add label

    def test_add_label_none_args(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        with self.assertRaises(SyntaxError):
            svc.add_label()

    def test_add_label_invalid_args(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        k = object()
        v = object()
        with self.assertRaises(SyntaxError):
            svc.add_label(k, v)

    def test_add_label(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        k = "yokey"
        v = "yovalue"
        svc.add_label(k, v)
        self.assertIn(k, svc.labels)
        self.assertEqual(v, svc.labels[k])

    # --------------------------------------------------------------------------------- add port

    def test_add_port_none_args(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        with self.assertRaises(SyntaxError):
            svc.add_port()

    def test_add_port_invalid_name(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        name = object()
        with self.assertRaises(SyntaxError):
            svc.add_port(name=name)

    def test_add_port_invalid_port(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        port = object()
        with self.assertRaises(SyntaxError):
            svc.add_port(name=name, port=port)

    def test_add_port_invalid_target_port(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        target_port = object()
        with self.assertRaises(SyntaxError):
            svc.add_port(name=name, target_port=target_port)

    def test_add_port_invalid_protocol(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        protocol = object()
        with self.assertRaises(SyntaxError):
            svc.add_port(name=name, protocol=protocol)

    def test_add_port_invalid_node_port(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        node_port = object()
        with self.assertRaises(SyntaxError):
            svc.add_port(name=name, node_port=node_port)

    def test_add_port_with_all_args(self):
        svc_name = "yoservice"
        svc = _utils.create_service(name=svc_name)
        port = 666
        port_name = "yoport"
        target_port = 666
        protocol = 'TCP'
        node_port = 666
        svc.add_port(
            port=port,
            name=port_name,
            target_port=target_port,
            protocol=protocol,
            node_port=node_port
        )
        self.assertEqual(1, len(svc.ports))
        self.assertEqual(port_name, svc.ports[0].name)
        self.assertEqual(port, svc.ports[0].port)
        self.assertEqual(target_port, svc.ports[0].target_port)
        self.assertEqual(protocol, svc.ports[0].protocol)
        self.assertEqual(node_port, svc.ports[0].node_port)

    # --------------------------------------------------------------------------------- add selector

    def test_add_selector_none_arg(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        with self.assertRaises(SyntaxError):
            svc.add_selector()

    def test_add_selector_invalid_arg(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        sel = object()
        with self.assertRaises(SyntaxError):
            svc.add_selector(sel)

    def test_add_selector(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        sel = {'abc': 'def'}
        svc.add_selector(selector=sel)
        self.assertEqual(sel, svc.selector)

    # --------------------------------------------------------------------------------- get

    def test_get_nonexistent(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        if _utils.is_reachable(svc.config):
            with self.assertRaises(NotFoundException):
                svc.get()

    def test_get(self):
        name = "yo-{0}".format(str(uuid.uuid4().hex[:16]))
        svc = _utils.create_service(name=name)
        svc.add_port(name="redis", port=5432, target_port=5432, protocol="tcp")
        if _utils.is_reachable(svc.config):
            svc.create()
            from_get = svc.get()
            self.assertIsInstance(from_get, K8sService)
            self.assertEqual(svc, from_get)

    # --------------------------------------------------------------------------------- get annotation

    def test_get_annotation_none_arg(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        ann = svc.get_annotation()
        self.assertIsNone(ann)

    def test_get_annotation_invalid_arg(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        k = object()
        ann = svc.get_annotation(k)
        self.assertIsNone(ann)

    def test_get_annotation_doesnt_exist(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        k = "yokey"
        v = svc.get_annotation(k)
        self.assertIsNone(v)

    def test_get_annotation(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        k = "yokey"
        v_in = "yovalue"
        svc.add_annotation(k, v_in)
        v_out = svc.get_annotation(k)
        self.assertEqual(v_in, v_out)

    # --------------------------------------------------------------------------------- get annotations

    def test_get_annotations_doesnt_exist(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        self.assertEqual({}, svc.annotations)

    def test_get_annotations(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        count = 4
        for i in range(0, count):
            k = "yokey_{0}".format(i)
            v = "yovalue_{0}".format(i)
            svc.add_annotation(k, v)
        self.assertEqual(count, len(svc.annotations))
        for i in range(0, count):
            k = "yokey_{0}".format(i)
            v = "yovalue_{0}".format(i)
            self.assertIn(k, svc.annotations)
            self.assertEqual(v, svc.annotations[k])

    # --------------------------------------------------------------------------------- get cluster ip

    def test_get_cluster_ip_doesnt_exist(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        self.assertIsNone(svc.cluster_ip)

    def test_get_cluster_ip(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        ip = "192.168.99.100"
        svc.cluster_ip = ip
        self.assertEqual(ip, svc.cluster_ip)

    # --------------------------------------------------------------------------------- get external ip

    def test_get_external_ips(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        eips = ["192.168.99.100"]
        svc.external_ips = eips
        self.assertEqual(eips, svc.external_ips)

    def test_get_external_ips_doesnt_exist(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        self.assertEqual([], svc.external_ips)

    # --------------------------------------------------------------------------------- get label

    def test_get_label_none_arg(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        self.assertIsNone(svc.get_label())

    def test_get_label_invalid_arg(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        k = object()
        self.assertIsNone(svc.get_label(k))

    def test_get_label_doesnt_exist(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        k = "yokey"
        self.assertIsNone(svc.get_label(k))

    def test_get_label(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        k = "yokey"
        v = "yovalue"
        svc.add_label(k, v)
        self.assertEqual(v, svc.get_label(k))

    # --------------------------------------------------------------------------------- get labels

    def test_get_labels_doesnt_exist(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        self.assertIsNotNone(svc.labels)  # 'name' is already a label
        self.assertIn('name', svc.labels)

    def test_get_labels(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        labels = {'yokey': 'yovalue'}
        svc.labels = labels
        self.assertEqual(labels, svc.labels)

    # --------------------------------------------------------------------------------- set annotations

    def test_set_annotations_none_arg(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        with self.assertRaises(SyntaxError):
            svc.annotations = None

    def test_set_annotations_invalid_arg(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        labels = object()
        with self.assertRaises(SyntaxError):
            svc.annotations = labels

    def test_set_annotations_str_int(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        labels = {'yokey': 1234}
        svc.annotations = labels
        self.assertEqual(svc.annotations, labels)

    def test_set_annotations(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        anns = {'yokey': 'yovalue'}
        svc.annotations = anns
        self.assertEqual(anns, svc.annotations)

    # --------------------------------------------------------------------------------- set cluster ip

    def test_set_cluster_ip_none_arg(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        with self.assertRaises(SyntaxError):
            svc.cluster_ip = None

    def test_set_cluster_ip_invalid_arg(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        ip = object()
        with self.assertRaises(SyntaxError):
            svc.cluster_ip = ip

    def test_set_cluster_ip_invalid_ip_address(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        svc.add_port('http', 80, 80, 'TCP')
        if _utils.is_reachable(svc.config):
            svc.create()
            ip = "192.168.00000.1234345"
            svc.cluster_ip = ip
            with self.assertRaises(UnprocessableEntityException):
                svc.update()

    def test_set_cluster_ip(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        cip = "192.168.99.100"
        svc.cluster_ip = cip
        self.assertEqual(cip, svc.cluster_ip)

    # --------------------------------------------------------------------------------- set external ips

    def test_set_external_ips_none_arg(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        with self.assertRaises(SyntaxError):
            svc.external_ips = None

    def test_set_external_ips_invalid_arg(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        eips = object()
        with self.assertRaises(SyntaxError):
            svc.external_ips = eips

    def test_set_external_ips_invalid_ip_address(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        eips = ["192.168.00000.1234345"]
        with self.assertRaises(SyntaxError):
            svc.external_ips = eips

    def test_set_external_ip(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        eips = ["192.168.99.100"]
        svc.external_ips = eips
        self.assertEqual(eips, svc.external_ips)

    # --------------------------------------------------------------------------------- set labels

    def test_set_labels_none_arg(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        with self.assertRaises(SyntaxError):
            svc.labels = None

    def test_set_labels_invalid_arg(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        labels = object()
        with self.assertRaises(SyntaxError):
            svc.labels = labels

    def test_set_labels_invalid_dict(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        labels = {'yokey': 1234}
        with self.assertRaises(SyntaxError):
            svc.labels = labels

    def test_set_labels(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        labels = {'yokey': 'yovalue'}
        svc.labels = labels
        self.assertEqual(labels, svc.labels)

    # --------------------------------------------------------------------------------- set load balancer ip

    def test_set_load_balancer_ip_none_arg(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        with self.assertRaises(SyntaxError):
            svc.load_balancer_ip = None

    def test_set_load_balancer_ip_invalid_arg(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        ip = object()
        with self.assertRaises(SyntaxError):
            svc.load_balancer_ip = ip

    def test_set_load_balancer_ip_invalid_ip_address(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        ip = "192.168.00000.1234345"
        with self.assertRaises(SyntaxError):
            svc.load_balancer_ip = ip

    def test_set_load_balancer_ip(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        ip = "192.168.99.100"
        svc.load_balancer_ip = ip
        self.assertEqual(ip, svc.load_balancer_ip)

    # --------------------------------------------------------------------------------- set namespace

    def test_set_namespace_none_arg(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        with self.assertRaises(SyntaxError):
            svc.namespace = None

    def test_set_namespace_invalid_arg(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        nspace = object()
        with self.assertRaises(SyntaxError):
            svc.namespace = nspace

    def test_set_namespace(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        nspace = "yonamespace"
        svc.namespace = nspace
        self.assertEqual(nspace, svc.namespace)

    # --------------------------------------------------------------------------------- set session affinity

    def test_set_session_affinity_none_arg(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        with self.assertRaises(SyntaxError):
            svc.session_affinity = None

    def test_set_session_affinity_invalid_arg(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        aff = object()
        with self.assertRaises(SyntaxError):
            svc.session_affinity = aff

    def test_set_session_affinity_invalid_string(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        aff = 'yoaffinity'
        with self.assertRaises(SyntaxError):
            svc.session_affinity = aff

    def test_set_session_affinity(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        for i in ['None', 'ClientIP']:
            svc.session_affinity = i
            self.assertEqual(i, svc.session_affinity)

    # --------------------------------------------------------------------------------- set service type

    def test_set_service_type_none_arg(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        with self.assertRaises(SyntaxError):
            svc.type = None

    def test_set_service_type_invalid_arg(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        stype = object()
        with self.assertRaises(SyntaxError):
            svc.type = stype

    def test_set_service_type_invalid_string(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        stype = "yoservicetype"
        with self.assertRaises(SyntaxError):
            svc.type = stype

    def test_set_service_type(self):
        name = "yoservice"
        svc = _utils.create_service(name=name)
        for i in ['ClusterIP', 'NodePort', 'LoadBalancer']:
            svc.type = i
            self.assertEqual(i, svc.type)

    # --------------------------------------------------------------------------------- api - get by name

    def test_get_by_name_nonexistent(self):
        name = "yo-{0}".format(str(uuid.uuid4().hex[:16]))
        svc = _utils.create_service(name=name)
        svc.add_port(name="redis", port=5432, target_port=5432, protocol="tcp")
        if _utils.is_reachable(svc.config):
            _list = K8sService.get_by_name(config=svc.config, name=name)
            self.assertIsInstance(_list, list)
            self.assertEqual(0, len(_list))

    def test_get_by_name(self):
        name = "yo-{0}".format(str(uuid.uuid4().hex[:16]))
        svc = _utils.create_service(name=name)
        svc.add_port(name="redis", port=5432, target_port=5432, protocol="tcp")
        if _utils.is_reachable(svc.config):
            svc.create()
            _list = K8sService.get_by_name(config=svc.config, name=name)
            self.assertIsInstance(_list, list)
            self.assertEqual(1, len(_list))
            from_get = _list[0]
            self.assertIsInstance(from_get, K8sService)
            self.assertEqual(from_get, svc)

    # --------------------------------------------------------------------------------- api - list

    def test_list_without_create(self):
        name = "yo-{0}".format(str(uuid.uuid4().hex[:16]))
        svc = _utils.create_service(name=name)
        svc.add_port(name="redis", port=5432, target_port=5432, protocol="tcp")
        if _utils.is_reachable(svc.config):
            _list = svc.list()

    def test_list(self):
        name = "yo-{0}".format(str(uuid.uuid4().hex[:16]))
        svc = _utils.create_service(name=name)
        svc.add_port(name="redis", port=5432, target_port=5432, protocol="tcp")
        if _utils.is_reachable(svc.config):
            svc.create()
            _list = svc.list()
            for x in _list:
                self.assertIsInstance(x, K8sService)
            self.assertIsInstance(_list, list)
            self.assertEqual(2, len(_list))  # api server exists already
            from_query = _list[1]
            self.assertEqual(name, from_query.name)

    # --------------------------------------------------------------------------------- api - create

    def test_create(self):
        name = "yo-{0}".format(str(uuid.uuid4().hex[:16]))
        svc = _utils.create_service(name=name)
        svc.add_port(name="redis", port=5432, target_port=5432, protocol="tcp")
        if _utils.is_reachable(svc.config):
            svc.create()
            from_get = svc.get()
            self.assertEqual(svc, from_get)

    def test_create_already_exists(self):
        name = "yo-{0}".format(str(uuid.uuid4().hex[:16]))
        svc = _utils.create_service(name=name)
        svc.add_port(name="redis", port=5432, target_port=5432, protocol="tcp")
        if _utils.is_reachable(svc.config):
            svc.create()
            with self.assertRaises(UnprocessableEntityException):
                svc.create()

    # --------------------------------------------------------------------------------- api - update

    def test_update_nonexistent(self):
        name = "yo-{0}".format(str(uuid.uuid4().hex[:16]))
        svc = _utils.create_service(name=name)
        svc.add_port(name="redis", port=5432, target_port=5432, protocol="tcp")
        if _utils.is_reachable(svc.config):
            with self.assertRaises(NotFoundException):
                svc.update()

    def test_update_nothing_changed(self):
        name = "yo-{0}".format(str(uuid.uuid4().hex[:16]))
        svc = _utils.create_service(name=name)
        svc.add_port(name="redis", port=5432, target_port=5432, protocol="tcp")
        if _utils.is_reachable(svc.config):
            from_create = svc.create()
            from_update = svc.update()
            self.assertEqual(from_create, from_update)

    def test_update_set_cluster_ip_fails(self):
        name = "yo-{0}".format(str(uuid.uuid4().hex[:16]))
        svc = _utils.create_service(name=name)
        svc.add_port(name="redis", port=5432, target_port=5432, protocol="tcp")
        if _utils.is_reachable(svc.config):
            svc.create()
            svc.cluster_ip = "192.168.123.123"
            with self.assertRaises(UnprocessableEntityException):
                svc.update()

    def test_update_set_external_ips(self):
        name = "yo-{0}".format(str(uuid.uuid4().hex[:16]))
        svc = _utils.create_service(name=name)
        svc.add_port(name="redis", port=5432, target_port=5432, protocol="tcp")
        ip = '192.168.123.123'
        if _utils.is_reachable(svc.config):
            svc.create()
            svc.external_ips = [ip]
            svc.update()
            self.assertIn(ip, svc.external_ips)

    def test_update_with_full_model(self):
        data = {
            "kind": "Service",
            "apiVersion": "v1",
            "metadata": {
                "name": "frontend",
                "namespace": "default",
                "labels": {
                    "name": "frontend"
                }
            },
            "spec": {
                "ports": [
                    {
                        "protocol": "TCP",
                        "port": 8082,
                        "targetPort": "feport",
                        "nodePort": 8082
                    }
                ],
                "selector": {
                    "name": "frontend"
                },
                "clusterIP": "10.250.1.27",
                "type": "NodePort",
                "sessionAffinity": "None"
            },
            "status": {
                "loadBalancer": {}
            }
        }

        svc = Service(data)
        k8s_service = _utils.create_service(name=svc.name)
        k8s_service.model = svc

        k8s_service.add_port(
            name="frontend",
            port=8082,
            target_port="feport",
            node_port=8082,
            protocol='tcp'
        )

        self.assertEqual(1, len(k8s_service.ports))

    # --------------------------------------------------------------------------------- api - delete

    def test_delete_nonexistent(self):
        name = "yo-{0}".format(str(uuid.uuid4().hex[:16]))
        svc = _utils.create_service(name=name)
        svc.add_port(name="redis", port=5432, target_port=5432, protocol="tcp")
        if _utils.is_reachable(svc.config):
            with self.assertRaises(NotFoundException):
                svc.delete()

    def test_delete(self):
        name = "yo-{0}".format(str(uuid.uuid4().hex[:16]))
        svc = _utils.create_service(name=name)
        svc.add_port(name="redis", port=5432, target_port=5432, protocol="tcp")
        if _utils.is_reachable(svc.config):
            svc.create()
            from_get = K8sService.get_by_name(svc.config, svc.name)
            self.assertIsInstance(from_get, list)
            self.assertIn(svc, from_get)
            svc.delete()
            from_get = K8sService.get_by_name(svc.config, svc.name)
            self.assertNotIn(svc, from_get)

    # --------------------------------------------------------------------------------- api - system

    def test_system_service(self):
        config = _utils.create_config()
        config.namespace = 'kube-system'

        service = _utils.create_service(config, name="my-kubernetes-dashboard")
        service.type = 'ClusterIP'
        service.add_port(
            port=80,
            target_port="k8s-dashport",
            name="kubernetes-dashboard",
            protocol="TCP"
        )
        service.selector = {'k8s-app': "kubernetes-dashboard"}
        service.labels = {
            'k8s-app': "kubernetes-dashboard",
            'kubernetes.io/cluster-service': 'true'
        }

        service2 = _utils.create_service(config, name="my-kubernetes-dashboard")
        service2.type = 'ClusterIP'
        service2.add_port(
            port=80,
            target_port="k8s-dashport",
            name="kubernetes-dashboard",
            protocol="TCP"
        )
        service2.selector = {'k8s-app': "kubernetes-dashboard"}
        service2.labels = {
            'k8s-app': "kubernetes-dashboard",
            'kubernetes.io/cluster-service': 'true'
        }

        if _utils.is_reachable(service.config):
            service.create()
            time.sleep(0.2)
            with self.assertRaises(AlreadyExistsException):
                service2.create()
            service.update()
            service.delete()

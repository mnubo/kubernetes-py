#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import unittest
import uuid
from kubernetes import K8sService, K8sConfig
from kubernetes.models.v1 import Service, ObjectMeta
from kubernetes.K8sExceptions import *
from tests import utils


class K8sServiceTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        utils.cleanup_objects()

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
        try:
            K8sService(config=config)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_init_with_invalid_name(self):
        name = object()
        try:
            utils.create_service(name=name)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_init_with_name(self):
        name = "yoname"
        svc = utils.create_service(name=name)
        self.assertIsNotNone(svc)
        self.assertIsInstance(svc, K8sService)
        self.assertEqual('Service', svc.obj_type)
        self.assertEqual(svc.name, name)
        self.assertIsInstance(svc.config, K8sConfig)

    def test_init_with_name_and_config(self):
        nspace = "yonamespace"
        config = K8sConfig(kubeconfig=utils.kubeconfig_fallback, namespace=nspace)
        name = "yoname"
        svc = utils.create_service(config=config, name=name)
        self.assertIsNotNone(svc)
        self.assertIsInstance(svc, K8sService)
        self.assertEqual(svc.name, name)
        self.assertEqual('Service', svc.obj_type)
        self.assertIsInstance(svc.config, K8sConfig)
        self.assertEqual(nspace, svc.config.namespace)

    # --------------------------------------------------------------------------------- struct

    def test_struct_k8s_service(self):
        name = "yoname"
        svc = utils.create_service(name=name)
        self.assertIsInstance(svc, K8sService)
        self.assertIsInstance(svc.base_url, str)
        self.assertIsInstance(svc.config, K8sConfig)
        self.assertIsInstance(svc.model, Service)
        self.assertIsInstance(svc.name, str)
        self.assertIsInstance(svc.obj_type, str)

    def test_struct_service(self):
        name = "yoname"
        svc = utils.create_service(name=name)
        self.assertIsInstance(svc, K8sService)
        self.assertIsInstance(svc.model, Service)
        self.assertIsInstance(svc.model.model, dict)
        self.assertIsInstance(svc.model.svc_metadata, ObjectMeta)

    def test_struct_service_model(self):
        name = "yoname"
        svc = utils.create_service(name=name)
        model = svc.model.model
        self.assertIsInstance(model, dict)
        self.assertEqual(4, len(model))
        for i in ['apiVersion', 'kind', 'metadata', 'spec']:
            self.assertIn(i, model)
        for i in ['apiVersion', 'kind']:
            self.assertIsInstance(model[i], str)
        for i in ['metadata', 'spec']:
            self.assertIsInstance(model[i], dict)
        self.assertEqual(3, len(model['metadata']))
        for i in ['labels', 'name', 'namespace']:
            self.assertIn(i, model['metadata'])
        self.assertIsInstance(model['metadata']['labels'], dict)
        for i in ['name', 'namespace']:
            self.assertIsInstance(model['metadata'][i], str)
        self.assertEqual(4, len(model['spec']))
        for i in ['ports', 'selector', 'sessionAffinity', 'type']:
            self.assertIn(i, model['spec'])
        self.assertIsInstance(model['spec']['ports'], list)
        self.assertIsInstance(model['spec']['selector'], dict)
        for i in ['sessionAffinity', 'type']:
            self.assertIsInstance(model['spec'][i], str)

    # --------------------------------------------------------------------------------- add annotation

    def test_add_annotation_none_args(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        try:
            svc.add_annotation()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_add_annotation_invalid_args(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        k = object()
        v = object()
        try:
            svc.add_annotation(k, v)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_add_annotation(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        k = "yokey"
        v = "yovalue"
        svc.add_annotation(k, v)
        self.assertIn('annotations', svc.model.model['metadata'])
        self.assertIn(k, svc.model.model['metadata']['annotations'])
        self.assertEqual(svc.model.model['metadata']['annotations']['yokey'], v)
        self.assertIn('annotations', svc.model.svc_metadata.model)
        self.assertIn(k, svc.model.svc_metadata.model['annotations'])
        self.assertEqual(svc.model.svc_metadata.model['annotations']['yokey'], v)

    # --------------------------------------------------------------------------------- add label

    def test_add_label_none_args(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        try:
            svc.add_label()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_add_label_invalid_args(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        k = object()
        v = object()
        try:
            svc.add_label(k, v)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_add_label(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        k = "yokey"
        v = "yovalue"
        svc.add_label(k, v)
        self.assertIn('labels', svc.model.model['metadata'])
        self.assertIn(k, svc.model.model['metadata']['labels'])
        self.assertEqual(svc.model.model['metadata']['labels']['yokey'], v)
        self.assertIn('labels', svc.model.svc_metadata.model)
        self.assertIn(k, svc.model.svc_metadata.model['labels'])

    # --------------------------------------------------------------------------------- add port

    def test_add_port_none_args(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        svc.add_port()
        self.assertEqual(0, len(svc.model.model['spec']['ports']))

    def test_add_port_invalid_port(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        port = object()
        try:
            svc.add_port(port=port)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_add_port_invalid_name(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        name = object()
        try:
            svc.add_port(name=name)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_add_port_invalid_target_port(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        target_port = object()
        try:
            svc.add_port(target_port=target_port)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_add_port_invalid_protocol(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        protocol = object()
        try:
            svc.add_port(protocol=protocol)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_add_port_invalid_node_port(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        node_port = object()
        try:
            svc.add_port(node_port=node_port)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_add_port_with_all_args(self):
        svc_name = "yoservice"
        svc = utils.create_service(name=svc_name)
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
        self.assertEqual(1, len(svc.model.model['spec']['ports']))
        port_spec = svc.model.model['spec']['ports'][0]
        for i in ['port', 'name', 'targetPort', 'protocol', 'nodePort']:
            self.assertIn(i, port_spec)
        self.assertEqual(port_spec['port'], port)
        self.assertEqual(port_spec['name'], port_name)
        self.assertEqual(port_spec['targetPort'], target_port)
        self.assertEqual(port_spec['protocol'], protocol)
        self.assertEqual(port_spec['nodePort'], node_port)

    # --------------------------------------------------------------------------------- add selector

    def test_add_selector_none_arg(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        try:
            svc.add_selector()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_add_selector_invalid_arg(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        sel = object()
        try:
            svc.add_selector(selector=sel)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_add_selector_dict_wrong_mapping(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        sel = {'abc': 1234}
        try:
            svc.add_selector(selector=sel)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_add_selector(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        sel = {'abc': 'def'}
        svc.add_selector(selector=sel)
        self.assertIn('selector', svc.model.model['spec'])
        self.assertEqual(sel, svc.model.model['spec']['selector'])

    # --------------------------------------------------------------------------------- del creation timestamp

    def test_del_meta_creation_timestamp_doesnt_exist(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        svc.del_meta_creation_timestamp()
        self.assertNotIn('creationTimestamp', svc.model.model['metadata'])
        self.assertNotIn('creationTimestamp', svc.model.svc_metadata.model)

    def test_del_meta_creation_timestamp_with_set(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        ts = "yotimestamp"
        svc.set_meta_creation_timestamp(ts)
        self.assertIn('creationTimestamp', svc.model.model['metadata'])
        self.assertIn('creationTimestamp', svc.model.svc_metadata.model)
        svc.del_meta_creation_timestamp()
        self.assertNotIn('creationTimestamp', svc.model.model['metadata'])
        self.assertNotIn('creationTimestamp', svc.model.svc_metadata.model)

    # --------------------------------------------------------------------------------- del meta generation

    def test_del_meta_generation_doesnt_exist(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        svc.del_meta_generation()
        self.assertNotIn('generation', svc.model.model['metadata'])
        self.assertNotIn('generation', svc.model.svc_metadata.model)

    def test_del_meta_generation_with_set(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        gen = 2
        svc.set_meta_generation(gen)
        self.assertIn('generation', svc.model.model['metadata'])
        self.assertIn('generation', svc.model.svc_metadata.model)
        svc.del_meta_generation()
        self.assertNotIn('generation', svc.model.model['metadata'])
        self.assertNotIn('generation', svc.model.svc_metadata.model)

    # --------------------------------------------------------------------------------- del meta resource version

    def test_del_meta_resource_version_doesnt_exist(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        svc.del_meta_resource_version()
        self.assertNotIn('resourceVersion', svc.model.model['metadata'])
        self.assertNotIn('resourceVersion', svc.model.svc_metadata.model)

    def test_del_meta_resource_version_with_set(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        ver = '2'
        svc.set_meta_resource_version(ver)
        self.assertIn('resourceVersion', svc.model.model['metadata'])
        self.assertIn('resourceVersion', svc.model.svc_metadata.model)
        svc.del_meta_resource_version()
        self.assertNotIn('resourceVersion', svc.model.model['metadata'])
        self.assertNotIn('resourceVersion', svc.model.svc_metadata.model)

    # --------------------------------------------------------------------------------- del meta self link

    def test_del_meta_self_link_doesnt_exist(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        svc.del_meta_self_link()
        self.assertNotIn('selfLink', svc.model.model['metadata'])
        self.assertNotIn('selfLink', svc.model.svc_metadata.model)

    def test_del_meta_self_link_with_set(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        link = 'yolink'
        svc.set_meta_self_link(link)
        self.assertIn('selfLink', svc.model.model['metadata'])
        self.assertIn('selfLink', svc.model.svc_metadata.model)
        svc.del_meta_self_link()
        self.assertNotIn('selfLink', svc.model.model['metadata'])
        self.assertNotIn('selfLink', svc.model.svc_metadata.model)

    # --------------------------------------------------------------------------------- del meta uid

    def test_del_meta_uid_doesnt_exist(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        svc.del_meta_uid()
        self.assertNotIn('uid', svc.model.model['metadata'])
        self.assertNotIn('uid', svc.model.svc_metadata.model)

    def test_del_meta_uid_with_set(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        uid = 'youid'
        svc.set_meta_uid(uid)
        self.assertIn('uid', svc.model.model['metadata'])
        self.assertIn('uid', svc.model.svc_metadata.model)
        svc.del_meta_uid()
        self.assertNotIn('uid', svc.model.model['metadata'])
        self.assertNotIn('uid', svc.model.svc_metadata.model)

    # --------------------------------------------------------------------------------- del server generated meta

    def test_del_server_generated_meta_doesnt_exist(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        svc.del_server_generated_meta_attr()
        for i in ['generation', 'resourceVersion', 'creationTimestamp',
                  'deletionTimestamp', 'deletionGracePeriodSeconds', 'status', 'selfLink', 'uid']:
            self.assertNotIn(i, svc.model.model['metadata'])
            self.assertNotIn(i, svc.model.svc_metadata.model)

    def test_del_server_generated_meta_with_set(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        svc.set_meta_generation(2)
        svc.set_meta_resource_version('yoresourceversion')
        svc.set_meta_creation_timestamp('yotimestamp')
        svc.set_meta_self_link('yoselflink')
        svc.set_meta_uid('youid')

        # TODO: include set / delete methods for deletionTimestamp, deletionGracePeriodSeconds and status...
        for i in ['generation', 'resourceVersion', 'creationTimestamp', 'selfLink', 'uid']:
            self.assertIn(i, svc.model.model['metadata'])
            self.assertIn(i, svc.model.svc_metadata.model)

        svc.del_server_generated_meta_attr()
        for i in ['generation', 'resourceVersion', 'creationTimestamp',
                  'deletionTimestamp', 'deletionGracePeriodSeconds', 'status', 'selfLink', 'uid']:
            self.assertNotIn(i, svc.model.model['metadata'])
            self.assertNotIn(i, svc.model.svc_metadata.model)

    # --------------------------------------------------------------------------------- get

    def test_get_nonexistent(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        if utils.is_reachable(svc.config.api_host):
            try:
                svc.get()
            except Exception as err:
                self.assertIsInstance(err, NotFoundException)

    def test_get(self):
        name = "yo-{0}".format(unicode(uuid.uuid4().get_hex()[:16]))
        svc = utils.create_service(name=name)
        svc.add_port(name="redis", port=5432, target_port=5432, protocol="tcp")
        if utils.is_reachable(svc.config.api_host):
            svc.create()
            from_get = svc.get()
            self.assertIsInstance(from_get, K8sService)
            self.assertEqual(svc, from_get)

    # --------------------------------------------------------------------------------- get annotation

    def test_get_annotation_none_arg(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        try:
            svc.get_annotation()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_get_annotation_invalid_arg(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        k = object()
        try:
            svc.get_annotation(k)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_get_annotation_doesnt_exist(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        k = "yokey"
        v = svc.get_annotation(k)
        self.assertIsNone(v)

    def test_get_annotation(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        k = "yokey"
        v_in = "yovalue"
        svc.add_annotation(k, v_in)
        v_out = svc.get_annotation(k)
        self.assertEqual(v_in, v_out)

    # --------------------------------------------------------------------------------- get annotations

    def test_get_annotations_doesnt_exist(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        anns = svc.get_annotations()
        self.assertIsNone(anns)

    def test_get_annotations(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        count = 4
        for i in range(0, count):
            k = "yokey_{0}".format(i)
            v = "yovalue_{0}".format(i)
            svc.add_annotation(k, v)
        anns = svc.get_annotations()
        self.assertEqual(count, len(anns))
        for i in range(0, count):
            k = "yokey_{0}".format(i)
            v = "yovalue_{0}".format(i)
            self.assertIn(k, anns)
            self.assertEqual(v, anns[k])

    # --------------------------------------------------------------------------------- get cluster ip

    def test_get_cluster_ip_doesnt_exist(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        cip = svc.get_cluster_ip()
        self.assertIsNone(cip)

    def test_get_cluster_ip(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        cip_in = "192.168.99.100"
        svc.set_cluster_ip(cip_in)
        cip_out = svc.get_cluster_ip()
        self.assertEqual(cip_in, cip_out)

    # --------------------------------------------------------------------------------- get external ip

    def test_get_external_ips_doesnt_exist(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        eips = svc.get_external_ips()
        self.assertIsNone(eips)

    def test_get_external_ips(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        eips_in = ["192.168.99.100"]
        svc.set_external_ips(eips_in)
        eips_out = svc.get_external_ips()
        self.assertEqual(eips_in, eips_out)

    # --------------------------------------------------------------------------------- get label

    def test_get_label_none_arg(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        try:
            svc.get_label()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_get_label_invalid_arg(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        k = object()
        try:
            svc.get_label(k)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_get_label_doesnt_exist(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        k = "yokey"
        v = svc.get_label(k)
        self.assertIsNone(v)

    def test_get_label(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        k = "yokey"
        v_in = "yovalue"
        svc.add_label(k, v_in)
        v_out = svc.get_label(k)
        self.assertEqual(v_in, v_out)

    # --------------------------------------------------------------------------------- get labels

    def test_get_labels_doesnt_exist(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        labels = svc.get_labels()
        self.assertIsNotNone(labels)  # 'name' is already a label
        self.assertIn('name', labels)

    def test_get_labels(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        labels_in = {'yokey': 'yovalue'}
        svc.set_labels(labels_in)
        labels_out = svc.get_labels()
        self.assertEqual(labels_in, labels_out)

    # --------------------------------------------------------------------------------- get meta creation timestamp

    def test_get_meta_creation_timestamp_doesnt_exist(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        tstamp = svc.get_meta_creation_timestamp()
        self.assertIsNone(tstamp)

    def test_get_meta_creation_timestamp(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        tstamp_in = "yotimestamp"
        svc.set_meta_creation_timestamp(tstamp_in)
        tstamp_out = svc.get_meta_creation_timestamp()
        self.assertEqual(tstamp_in, tstamp_out)

    # --------------------------------------------------------------------------------- get meta generation

    def test_get_meta_generation_doesnt_exist(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        gen = svc.get_meta_generation()
        self.assertIsNone(gen)

    def test_get_meta_generation(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        gen_in = 2
        svc.set_meta_generation(gen_in)
        gen_out = svc.get_meta_generation()
        self.assertEqual(gen_in, gen_out)

    # --------------------------------------------------------------------------------- get meta resource version

    def test_get_meta_resource_version_doesnt_exist(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        ver = svc.get_meta_resource_version()
        self.assertIsNone(ver)

    def test_get_meta_resource_version(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        ver_in = "yoversion"
        svc.set_meta_resource_version(ver_in)
        ver_out = svc.get_meta_resource_version()
        self.assertEqual(ver_in, ver_out)

    # --------------------------------------------------------------------------------- get meta self link

    def test_get_meta_self_link_doesnt_exist(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        slink = svc.get_meta_self_link()
        self.assertIsNone(slink)

    def test_get_meta_self_link(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        slink_in = "yoselflink"
        svc.set_meta_self_link(slink_in)
        slink_out = svc.get_meta_self_link()
        self.assertEqual(slink_in, slink_out)

    # --------------------------------------------------------------------------------- get meta uid

    def test_get_meta_uid_doesnt_exist(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        uid = svc.get_meta_uid()
        self.assertIsNone(uid)

    def test_get_meta_uid(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        uid_in = "yoselflink"
        svc.set_meta_uid(uid_in)
        uid_out = svc.get_meta_uid()
        self.assertEqual(uid_in, uid_out)

    # --------------------------------------------------------------------------------- set annotations

    def test_set_annotations_none_arg(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        try:
            svc.set_annotations()
            self.fail('Should not fail.')
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_annotations_invalid_arg(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        labels = object()
        try:
            svc.set_annotations(labels)
            self.fail('Should not fail.')
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_annotations_invalid_dict(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        labels = {'yokey': 1234}
        try:
            svc.set_annotations(labels)
            self.fail('Should not fail.')
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_annotations(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        anns = {'yokey': 'yovalue'}
        svc.set_annotations(anns)
        self.assertIn('annotations', svc.model.model['metadata'])
        self.assertEqual(anns, svc.model.model['metadata']['annotations'])

    # --------------------------------------------------------------------------------- set cluster ip

    def test_set_cluster_ip_none_arg(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        try:
            svc.set_cluster_ip()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_cluster_ip_invalid_arg(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        cip = object()
        try:
            svc.set_cluster_ip(cip)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_cluster_ip_invalid_ip_address(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        cip = "192.168.00000.1234345"
        try:
            svc.set_cluster_ip(cip)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_cluster_ip(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        cip = "192.168.99.100"
        svc.set_cluster_ip(cip)
        self.assertIn('clusterIP', svc.model.model['spec'])
        self.assertEqual(cip, svc.model.model['spec']['clusterIP'])

    # --------------------------------------------------------------------------------- set external ips

    def test_set_external_ips_none_arg(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        try:
            svc.set_external_ips()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_external_ips_invalid_arg(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        eips = object()
        try:
            svc.set_external_ips(eips)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_external_ips_invalid_ip_address(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        eips = ["192.168.00000.1234345"]
        try:
            svc.set_external_ips(eips)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_external_ip(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        eips = ["192.168.99.100"]
        svc.set_external_ips(eips)
        self.assertIn('externalIPs', svc.model.model['spec'])
        self.assertEqual(eips, svc.model.model['spec']['externalIPs'])

    # --------------------------------------------------------------------------------- set labels

    def test_set_labels_none_arg(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        try:
            svc.set_labels()
            self.fail('Should not fail.')
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_labels_invalid_arg(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        labels = object()
        try:
            svc.set_labels(labels)
            self.fail('Should not fail.')
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_labels_invalid_dict(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        labels = {'yokey': 1234}
        try:
            svc.set_labels(labels)
            self.fail('Should not fail.')
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_labels(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        labels = {'yokey': 'yovalue'}
        svc.set_labels(labels)
        self.assertIn('labels', svc.model.model['metadata'])
        self.assertEqual(labels, svc.model.model['metadata']['labels'])

    # --------------------------------------------------------------------------------- set load balancer ip

    def test_set_load_balancer_ip_none_arg(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        try:
            svc.set_load_balancer_ip()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_load_balancer_ip_invalid_arg(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        lbip = object()
        try:
            svc.set_load_balancer_ip(lbip)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_load_balancer_ip_invalid_ip_address(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        lbip = "192.168.00000.1234345"
        try:
            svc.set_load_balancer_ip(lbip)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_load_balancer_ip(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        lbip = "192.168.99.100"
        svc.set_load_balancer_ip(lbip)
        self.assertIn('loadBalancerIP', svc.model.model['spec'])
        self.assertEqual(lbip, svc.model.model['spec']['loadBalancerIP'])

    # --------------------------------------------------------------------------------- set namespace

    def test_set_namespace_none_arg(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        try:
            svc.set_namespace()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_namespace_invalid_arg(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        nspace = object()
        try:
            svc.set_namespace(nspace)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_namespace(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        nspace = "yonamespace"
        svc.set_namespace(nspace)
        self.assertIn('namespace', svc.model.model['metadata'])
        self.assertIn('namespace', svc.model.svc_metadata.model)
        self.assertEqual(nspace, svc.model.model['metadata']['namespace'])
        self.assertEqual(nspace, svc.model.svc_metadata.model['namespace'])

    # --------------------------------------------------------------------------------- set meta creation timestamp

    def test_set_meta_creation_timestamp_none_arg(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        try:
            svc.set_meta_creation_timestamp()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_meta_creation_timestamp_invalid_arg(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        ts = object()
        try:
            svc.set_meta_creation_timestamp(ts)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_meta_creation_timestamp(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        ts = "yotimestamp"
        svc.set_meta_creation_timestamp(ts)
        self.assertIn('creationTimestamp', svc.model.model['metadata'])
        self.assertIn('creationTimestamp', svc.model.svc_metadata.model)
        self.assertEqual(ts, svc.model.model['metadata']['creationTimestamp'])
        self.assertEqual(ts, svc.model.svc_metadata.model['creationTimestamp'])

    # --------------------------------------------------------------------------------- set meta generation

    def test_set_meta_generation_none_arg(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        try:
            svc.set_meta_generation()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_meta_generation_invalid_arg(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        gen = object()
        try:
            svc.set_meta_generation(gen)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_meta_generation(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        gen = 2
        svc.set_meta_generation(gen)
        self.assertIn('generation', svc.model.model['metadata'])
        self.assertIn('generation', svc.model.svc_metadata.model)
        self.assertEqual(gen, svc.model.model['metadata']['generation'])
        self.assertEqual(gen, svc.model.svc_metadata.model['generation'])

    # --------------------------------------------------------------------------------- set meta generation

    def test_set_meta_resource_version_none_arg(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        try:
            svc.set_meta_resource_version()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_meta_resource_version_invalid_arg(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        ver = object()
        try:
            svc.set_meta_resource_version(ver)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_meta_resource_version(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        ver = '2'
        svc.set_meta_resource_version(ver)
        self.assertIn('resourceVersion', svc.model.model['metadata'])
        self.assertIn('resourceVersion', svc.model.svc_metadata.model)
        self.assertEqual(ver, svc.model.model['metadata']['resourceVersion'])
        self.assertEqual(ver, svc.model.svc_metadata.model['resourceVersion'])

    # --------------------------------------------------------------------------------- set meta self link

    def test_set_meta_self_link_none_arg(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        try:
            svc.set_meta_self_link()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_meta_self_link_invalid_arg(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        link = object()
        try:
            svc.set_meta_self_link(link)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_meta_self_link(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        link = 'yolink'
        svc.set_meta_self_link(link)
        self.assertIn('selfLink', svc.model.model['metadata'])
        self.assertIn('selfLink', svc.model.svc_metadata.model)
        self.assertEqual(link, svc.model.model['metadata']['selfLink'])
        self.assertEqual(link, svc.model.svc_metadata.model['selfLink'])

    # --------------------------------------------------------------------------------- set meta uid

    def test_set_meta_uid_none_arg(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        try:
            svc.set_meta_uid()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_meta_uid_invalid_arg(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        uid = object()
        try:
            svc.set_meta_uid(uid)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_meta_uid(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        uid = 'youid'
        svc.set_meta_uid(uid)
        self.assertIn('uid', svc.model.model['metadata'])
        self.assertIn('uid', svc.model.svc_metadata.model)
        self.assertEqual(uid, svc.model.model['metadata']['uid'])
        self.assertEqual(uid, svc.model.svc_metadata.model['uid'])

    # --------------------------------------------------------------------------------- set session affinity

    def test_set_session_affinity_none_arg(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        try:
            svc.set_session_affinity()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_session_affinity_invalid_arg(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        aff = object()
        try:
            svc.set_session_affinity(aff)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_session_affinity_invalid_string(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        aff = 'yoaffinity'
        try:
            svc.set_session_affinity(aff)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_session_affinity(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        for i in ['None', 'ClientIP']:
            svc.set_session_affinity(i)
            self.assertIn('sessionAffinity', svc.model.model['spec'])
            self.assertEqual(i, svc.model.model['spec']['sessionAffinity'])

    # --------------------------------------------------------------------------------- set service type

    def test_set_service_type_none_arg(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        try:
            svc.set_service_type()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_service_type_invalid_arg(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        stype = object()
        try:
            svc.set_service_type(stype)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_service_type_invalid_string(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        stype = "yoservicetype"
        try:
            svc.set_service_type(stype)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_set_service_type(self):
        name = "yoservice"
        svc = utils.create_service(name=name)
        for i in ['ClusterIP', 'NodePort', 'LoadBalancer']:
            svc.set_service_type(i)
            self.assertIn('type', svc.model.model['spec'])
            self.assertEqual(i, svc.model.model['spec']['type'])

    # --------------------------------------------------------------------------------- api - get by name

    def test_get_by_name_nonexistent(self):
        name = "yo-{0}".format(unicode(uuid.uuid4().get_hex()[:16]))
        svc = utils.create_service(name=name)
        svc.add_port(name="redis", port=5432, target_port=5432, protocol="tcp")
        if utils.is_reachable(svc.config.api_host):
            _list = K8sService.get_by_name(config=svc.config, name=name)
            self.assertIsInstance(_list, list)
            self.assertEqual(0, len(_list))

    def test_get_by_name(self):
        name = "yo-{0}".format(unicode(uuid.uuid4().get_hex()[:16]))
        svc = utils.create_service(name=name)
        svc.add_port(name="redis", port=5432, target_port=5432, protocol="tcp")
        if utils.is_reachable(svc.config.api_host):
            svc.create()
            _list = K8sService.get_by_name(config=svc.config, name=name)
            self.assertIsInstance(_list, list)
            self.assertEqual(1, len(_list))
            from_get = _list[0]
            self.assertIsInstance(from_get, K8sService)
            self.assertEqual(from_get, svc)

    # --------------------------------------------------------------------------------- api - list

    def test_list_without_create(self):
        name = "yo-{0}".format(unicode(uuid.uuid4().get_hex()[:16]))
        svc = utils.create_service(name=name)
        svc.add_port(name="redis", port=5432, target_port=5432, protocol="tcp")
        if utils.is_reachable(svc.config.api_host):
            _list = svc.list()
            self.assertIsInstance(_list, list)
            self.assertEqual(1, len(_list))  # api server exists already
            self.assertIsInstance(_list[0], dict)

    def test_list(self):
        name = "yo-{0}".format(unicode(uuid.uuid4().get_hex()[:16]))
        svc = utils.create_service(name=name)
        svc.add_port(name="redis", port=5432, target_port=5432, protocol="tcp")
        if utils.is_reachable(svc.config.api_host):
            svc.create()
            _list = svc.list()
            self.assertIsInstance(_list, list)
            self.assertEqual(2, len(_list))  # api server exists already
            from_query = _list[1]
            self.assertIsInstance(from_query, dict)
            self.assertEqual(name, from_query['metadata']['name'])

    # --------------------------------------------------------------------------------- api - create

    def test_create_name_too_long(self):
        name = "yo-{0}".format(str(uuid.uuid4()))
        svc = utils.create_service(name=name)
        svc.add_port(name="redis", port=5432, target_port=5432, protocol="tcp")
        if utils.is_reachable(svc.config.api_host):
            try:
                svc.create()
                self.fail("Should not fail.")
            except Exception as err:
                self.assertIsInstance(err, UnprocessableEntityException)

    def test_create(self):
        name = "yo-{0}".format(unicode(uuid.uuid4().get_hex()[:16]))
        svc = utils.create_service(name=name)
        svc.add_port(name="redis", port=5432, target_port=5432, protocol="tcp")
        if utils.is_reachable(svc.config.api_host):
            svc.create()
            from_get = svc.get()
            self.assertEqual(svc, from_get)

    def test_create_already_exists(self):
        name = "yo-{0}".format(unicode(uuid.uuid4().get_hex()[:16]))
        svc = utils.create_service(name=name)
        svc.add_port(name="redis", port=5432, target_port=5432, protocol="tcp")
        if utils.is_reachable(svc.config.api_host):
            svc.create()
            try:
                svc.create()
                self.fail("Should not fail.")
            except Exception as err:
                self.assertIsInstance(err, UnprocessableEntityException)

    # --------------------------------------------------------------------------------- api - update

    def test_update_nonexistent(self):
        name = "yo-{0}".format(unicode(uuid.uuid4().get_hex()[:16]))
        svc = utils.create_service(name=name)
        svc.add_port(name="redis", port=5432, target_port=5432, protocol="tcp")
        if utils.is_reachable(svc.config.api_host):
            try:
                svc.update()
                self.fail("Should not fail.")
            except Exception as err:
                self.assertIsInstance(err, NotFoundException)

    def test_update_nothing_changed(self):
        name = "yo-{0}".format(unicode(uuid.uuid4().get_hex()[:16]))
        svc = utils.create_service(name=name)
        svc.add_port(name="redis", port=5432, target_port=5432, protocol="tcp")
        if utils.is_reachable(svc.config.api_host):
            from_create = svc.create()
            from_update = svc.update()
            self.assertEqual(from_create, from_update)

    def test_update_set_cluster_ip_fails(self):
        name = "yo-{0}".format(unicode(uuid.uuid4().get_hex()[:16]))
        svc = utils.create_service(name=name)
        svc.add_port(name="redis", port=5432, target_port=5432, protocol="tcp")
        if utils.is_reachable(svc.config.api_host):
            svc.create()
            svc.set_cluster_ip("192.168.123.123")
            svc.set_meta_resource_version(ver="1")
            try:
                svc.update()
                self.fail("Should not fail.")
            except Exception as err:
                self.assertIsInstance(err, UnprocessableEntityException)

    def test_update_set_external_ips(self):
        name = "yo-{0}".format(unicode(uuid.uuid4().get_hex()[:16]))
        svc = utils.create_service(name=name)
        svc.add_port(name="redis", port=5432, target_port=5432, protocol="tcp")
        ip = '192.168.123.123'
        if utils.is_reachable(svc.config.api_host):
            svc.create()
            svc.set_external_ips([ip])
            svc.update()
            self.assertIn(ip, svc.model.model['spec']['externalIPs'])

    # --------------------------------------------------------------------------------- api - delete

    def test_delete_nonexistent(self):
        name = "yo-{0}".format(unicode(uuid.uuid4().get_hex()[:16]))
        svc = utils.create_service(name=name)
        svc.add_port(name="redis", port=5432, target_port=5432, protocol="tcp")
        if utils.is_reachable(svc.config.api_host):
            try:
                svc.delete()
            except Exception as err:
                self.assertIsInstance(err, NotFoundException)

    def test_delete(self):
        name = "yo-{0}".format(unicode(uuid.uuid4().get_hex()[:16]))
        svc = utils.create_service(name=name)
        svc.add_port(name="redis", port=5432, target_port=5432, protocol="tcp")
        if utils.is_reachable(svc.config.api_host):
            svc.create()
            from_get = K8sService.get_by_name(svc.config, svc.name)
            self.assertIsInstance(from_get, list)
            self.assertIn(svc, from_get)
            svc.delete()
            from_get = K8sService.get_by_name(svc.config, svc.name)
            self.assertNotIn(svc, from_get)


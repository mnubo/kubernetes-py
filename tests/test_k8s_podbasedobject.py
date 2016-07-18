#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import unittest
from kubernetes import K8sPodBasedObject, K8sContainer
from kubernetes.models.v1 import Pod, ReplicationController, ObjectMeta, PodSpec


class K8sPodBasedObjectTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # --------------------------------------------------------------------------------- util

    def _create_pod(self, name='yopod'):
        obj = K8sPodBasedObject(obj_type='Pod', name=name)
        self.assertIsNotNone(obj)
        obj.model = Pod(name=name)
        self.assertIsInstance(obj.model, Pod)
        return obj

    def _create_rc(self, name='yorc'):
        obj = K8sPodBasedObject(obj_type='ReplicationController', name=name)
        self.assertIsNotNone(obj)
        obj.model = ReplicationController(name=name)
        self.assertIsInstance(obj.model, ReplicationController)
        return obj

    # --------------------------------------------------------------------------------- init

    def test_init_no_args(self):
        try:
            K8sPodBasedObject()
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_init_object_type_pod(self):
        ot = "Pod"
        name = "yopod"
        obj = K8sPodBasedObject(name=name, obj_type=ot)
        self.assertIsNotNone(obj)
        self.assertIsInstance(obj, K8sPodBasedObject)
        self.assertEqual(ot, obj.obj_type)
        self.assertEqual(name, obj.name)

    def test_init_object_type_rc(self):
        ot = "ReplicationController"
        name = "yorc"
        obj = K8sPodBasedObject(name=name, obj_type=ot)
        self.assertIsNotNone(obj)
        self.assertIsInstance(obj, K8sPodBasedObject)
        self.assertEqual(ot, obj.obj_type)
        self.assertEqual(name, obj.name)

    # --------------------------------------------------------------------------------- init

    def test_init_with_model_pod(self):
        obj = self._create_pod()
        self.assertIsInstance(obj.model, Pod)
        self.assertIsInstance(obj.model.model, dict)
        self.assertIsInstance(obj.model.pod_metadata, ObjectMeta)
        self.assertIsInstance(obj.model.pod_spec, PodSpec)
        self.assertIsNone(obj.model.pod_status)

    # --------------------------------------------------------------------------------- structure

    def test_struct_with_model_pod_check_podmeta(self):
        name = "yopod"
        obj = self._create_pod(name)
        meta = obj.model.pod_metadata
        self.assertIsNotNone(meta)
        self.assertIsInstance(meta, ObjectMeta)
        self.assertIsInstance(meta.model, dict)
        self.assertEqual(len(meta.model), 3)
        self.assertIn('labels', meta.model)
        self.assertIsInstance(meta.model['labels'], dict)
        self.assertIn('name', meta.model['labels'])
        self.assertEqual(meta.model['labels']['name'], name)
        self.assertIn('name', meta.model)
        self.assertIsInstance(meta.model['name'], str)
        self.assertEqual(meta.model['name'], name)
        self.assertIn('namespace', meta.model)
        self.assertIsInstance(meta.model['namespace'], str)

    def test_struct_with_model_pod_check_podspec(self):
        obj = self._create_pod()
        spec = obj.model.pod_spec
        self.assertIsNotNone(spec)
        self.assertIsInstance(spec, PodSpec)
        self.assertIsInstance(spec.containers, list)
        self.assertEqual(0, len(spec.containers))
        self.assertIsInstance(spec.model, dict)
        self.assertEqual(len(spec.model), 4)
        self.assertIn('containers', spec.model)
        self.assertIsInstance(spec.model['containers'], list)
        self.assertIn('dnsPolicy', spec.model)
        self.assertIsInstance(spec.model['dnsPolicy'], str)
        self.assertIn('restartPolicy', spec.model)
        self.assertIsInstance(spec.model['restartPolicy'], str)
        self.assertIn('volumes', spec.model)
        self.assertIsInstance(spec.model['volumes'], list)

    # --------------------------------------------------------------------------------- rc - init

    def test_init_with_model_rc(self):
        name = "yopod"
        obj = K8sPodBasedObject(obj_type='ReplicationController', name=name)
        self.assertIsNotNone(obj)
        obj.model = ReplicationController(name=name)
        self.assertIsInstance(obj.model, ReplicationController)
        self.assertIsInstance(obj.model.model, dict)
        self.assertIsInstance(obj.model.pod_metadata, ObjectMeta)
        self.assertIsInstance(obj.model.pod_spec, PodSpec)
        self.assertIsNone(obj.model.pod_status)
        self.assertIsInstance(obj.model.rc_metadata, ObjectMeta)

    # --------------------------------------------------------------------------------- rc - structure

    def test_struct_with_model_rc_check_podmeta(self):
        name = "yopod"
        obj = K8sPodBasedObject(obj_type='ReplicationController', name=name)
        self.assertIsNotNone(obj)
        obj.model = ReplicationController(name=name)
        meta = obj.model.pod_metadata
        self.assertIsNotNone(meta)
        self.assertIsInstance(meta, ObjectMeta)
        self.assertIsInstance(meta.model, dict)
        self.assertEqual(len(meta.model), 3)
        self.assertIn('labels', meta.model)
        self.assertIsInstance(meta.model['labels'], dict)
        self.assertIn('name', meta.model['labels'])
        self.assertEqual(meta.model['labels']['name'], name)
        self.assertIn('name', meta.model)
        self.assertIsInstance(meta.model['name'], str)
        self.assertEqual(meta.model['name'], name)
        self.assertIn('namespace', meta.model)
        self.assertIsInstance(meta.model['namespace'], str)

    def test_struct_with_model_rc_check_podspec(self):
        name = "yopod"
        obj = K8sPodBasedObject(obj_type='ReplicationController', name=name)
        self.assertIsNotNone(obj)
        obj.model = ReplicationController(name=name)
        spec = obj.model.pod_spec
        self.assertIsNotNone(spec)
        self.assertIsInstance(spec, PodSpec)
        self.assertIsInstance(spec.containers, list)
        self.assertEqual(0, len(spec.containers))
        self.assertIsInstance(spec.model, dict)
        self.assertEqual(len(spec.model), 4)
        self.assertIn('containers', spec.model)
        self.assertIsInstance(spec.model['containers'], list)
        self.assertIn('dnsPolicy', spec.model)
        self.assertIsInstance(spec.model['dnsPolicy'], str)
        self.assertIn('restartPolicy', spec.model)
        self.assertIsInstance(spec.model['restartPolicy'], str)
        self.assertIn('volumes', spec.model)
        self.assertIsInstance(spec.model['volumes'], list)

    def test_struct_with_model_rc_check_rcmeta(self):
        name = "yopod"
        obj = K8sPodBasedObject(obj_type='ReplicationController', name=name)
        self.assertIsNotNone(obj)
        obj.model = ReplicationController(name=name)
        meta = obj.model.rc_metadata
        self.assertIsNotNone(meta)
        self.assertIsInstance(meta, ObjectMeta)
        self.assertIsInstance(meta.model, dict)
        self.assertEqual(len(meta.model), 3)
        self.assertIn('labels', meta.model)
        self.assertIsInstance(meta.model['labels'], dict)
        self.assertIn('name', meta.model['labels'])
        self.assertEqual(meta.model['labels']['name'], name)
        self.assertIn('name', meta.model)
        self.assertIsInstance(meta.model['name'], str)
        self.assertEqual(meta.model['name'], name)
        self.assertIn('namespace', meta.model)
        self.assertIsInstance(meta.model['namespace'], str)

    # --------------------------------------------------------------------------------- add container

    def test_pod_add_container_invalid(self):
        obj = self._create_pod()
        c = object()
        try:
            obj.add_container(c)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, AssertionError)

    def test_pod_add_container(self):
        obj = self._create_pod()

        podspec = obj.model.model['spec']
        self.assertEqual(0, len(podspec['containers']))

        podspec = obj.model.pod_spec
        self.assertEqual(0, len(podspec.containers))
        self.assertEqual(0, len(podspec.model['containers']))

        name = "yopod"
        image = "busybox"
        c = K8sContainer(name=name, image=image)
        obj.add_container(c)

        podspec = obj.model.model['spec']
        self.assertEqual(1, len(podspec['containers']))

        podspec = obj.model.pod_spec
        self.assertEqual(1, len(podspec.containers))
        self.assertEqual(1, len(podspec.model['containers']))

    # --------------------------------------------------------------------------------- add host volume

    def test_pod_add_host_volume_none_args(self):
        obj = self._create_pod()
        volname = None
        volpath = None
        try:
            obj.add_host_volume(name=volname, path=volpath)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_add_host_volume_invalid_args(self):
        obj = self._create_pod()
        volname = 666
        volpath = 999
        try:
            obj.add_host_volume(name=volname, path=volpath)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_add_host_volume(self):
        obj = self._create_pod()
        volname = "devnull"
        volpath = "/dev/null"
        obj.add_host_volume(name=volname, path=volpath)

        podspec = obj.model.model['spec']
        self.assertEqual(1, len(podspec['volumes']))
        self.assertEqual(volname, podspec['volumes'][0]['name'])

        podspec = obj.model.pod_spec
        self.assertEqual(1, len(podspec.model['volumes']))
        self.assertEqual(volname, podspec.model['volumes'][0]['name'])

    # --------------------------------------------------------------------------------- add emptydir volume

    def test_pod_add_emptydir_volume_none_arg(self):
        obj = self._create_pod()
        volname = None
        try:
            obj.add_emptydir_volume(name=volname)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_add_emptydir_volume_invalid_arg(self):
        obj = self._create_pod()
        volname = 666
        try:
            obj.add_emptydir_volume(name=volname)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_add_emptydir_volume(self):
        obj = self._create_pod()
        volname = "emptydir"
        obj.add_emptydir_volume(name=volname)

        podspec = obj.model.model['spec']
        self.assertEqual(1, len(podspec['volumes']))
        self.assertEqual(volname, podspec['volumes'][0]['name'])

        podspec = obj.model.pod_spec
        self.assertEqual(volname, podspec.model['volumes'][0]['name'])

    # --------------------------------------------------------------------------------- add pull secret

    def test_pod_add_image_pull_secrets_none_arg(self):
        obj = self._create_pod()
        secretname = None
        try:
            obj.add_image_pull_secrets(name=secretname)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_add_image_pull_secrets_invalid_arg(self):
        obj = self._create_pod()
        secretname = 666
        try:
            obj.add_image_pull_secrets(name=secretname)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_add_image_pull_secrets(self):
        obj = self._create_pod()
        secretname = "yosecret"
        obj.add_image_pull_secrets(name=secretname)

        podspec = obj.model.model['spec']
        self.assertIn('imagePullSecrets', podspec)
        self.assertEqual(1, len(podspec['imagePullSecrets']))
        self.assertEqual(secretname, podspec['imagePullSecrets'][0]['name'])

        podspec = obj.model.pod_spec
        self.assertIn('imagePullSecrets', podspec.model)
        self.assertEqual(1, len(podspec.model['imagePullSecrets']))
        self.assertEqual(secretname, podspec.model['imagePullSecrets'][0]['name'])

    # --------------------------------------------------------------------------------- del pod node name

    def test_pod_del_pod_node_name(self):
        obj = self._create_pod()
        nodename = "yonodename"
        obj.set_pod_node_name(name=nodename)

        podspec = obj.model.model['spec']
        self.assertIn('nodeName', podspec)
        self.assertIsInstance(podspec['nodeName'], str)
        self.assertEqual(nodename, podspec['nodeName'])

        podspec = obj.model.pod_spec
        self.assertIn('nodeName', podspec.model)
        self.assertIsInstance(podspec.model['nodeName'], str)
        self.assertEqual(nodename, podspec.model['nodeName'])

        obj.del_pod_node_name()

        podspec = obj.model.model['spec']
        self.assertNotIn('nodeName', podspec)

        podspec = obj.model.pod_spec
        self.assertNotIn('nodeName', podspec.model)

    # --------------------------------------------------------------------------------- get pod containers

    def test_pod_get_pod_containers_empty(self):
        obj = self._create_pod()
        containers = obj.get_pod_containers()
        self.assertIsNotNone(containers)
        self.assertEqual(0, len(containers))

    def test_pod_get_pod_containers(self):
        obj = self._create_pod()
        count = 3
        for i in range(0, 3):
            name = "yocontainer_{0}".format(i)
            image = "busybox"
            c = K8sContainer(name=name, image=image)
            obj.add_container(c)

        containers = obj.get_pod_containers()
        self.assertIsNotNone(containers)
        self.assertEqual(count, len(containers))
        [self.assertIsInstance(x, dict) for x in containers]

    # --------------------------------------------------------------------------------- get pod node name

    def test_pod_get_pod_node_name_none(self):
        obj = self._create_pod()
        name = obj.get_pod_node_name()
        self.assertIsNone(name)

    def test_pod_get_pod_node_name(self):
        obj = self._create_pod()
        nodename = "yonodename"
        obj.set_pod_node_name(name=nodename)
        name = obj.get_pod_node_name()
        self.assertEqual(name, nodename)

    # --------------------------------------------------------------------------------- get pod node selector

    def test_pod_get_pod_node_selector_none(self):
        obj = self._create_pod()
        s = obj.get_pod_node_selector()
        self.assertIsNone(s)

    def test_pod_get_pod_node_selector(self):
        obj = self._create_pod()
        s_in = {"disktype": "ssd"}
        obj.set_pod_node_selector(new_dict=s_in)

        s_out = obj.get_pod_node_selector()
        self.assertEqual(s_in, s_out)

    # --------------------------------------------------------------------------------- get pod restart policy

    def test_pod_get_pod_restart_policy_none(self):
        obj = self._create_pod()
        rp = obj.get_pod_restart_policy()
        self.assertEqual('Always', rp)  # set to 'Always' by default

    def test_pod_get_pod_restart_policy(self):
        obj = self._create_pod()
        p_in = 'OnFailure'
        obj.set_pod_restart_policy(p_in)
        p_out = obj.get_pod_restart_policy()
        self.assertEqual(p_in, p_out)

    # --------------------------------------------------------------------------------- get service account

    def test_pod_get_service_account_none(self):
        obj = self._create_pod()
        acct = obj.get_service_account()
        self.assertIsNone(acct)

    def test_pod_get_service_account(self):
        obj = self._create_pod()
        name_in = "yoservice"
        obj.set_service_account(name_in)
        name_out = obj.get_service_account()
        self.assertEqual(name_in, name_out)

    # --------------------------------------------------------------------------------- set active deadline

    def test_pod_set_active_deadline_none_arg(self):
        obj = self._create_pod()
        d = None
        try:
            obj.set_active_deadline(d)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_set_active_deadline_invalid_arg(self):
        obj = self._create_pod()
        d = "yodeadline"
        try:
            obj.set_active_deadline(d)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_set_active_deadline(self):
        obj = self._create_pod()
        d = 600
        obj.set_active_deadline(d)

        podspec = obj.model.model['spec']
        self.assertIn('activeDeadlineSeconds', podspec)
        self.assertIsInstance(podspec['activeDeadlineSeconds'], int)
        self.assertEqual(d, podspec['activeDeadlineSeconds'])

        podspec = obj.model.pod_spec
        self.assertNotIn('nodeName', podspec.model)
        self.assertIn('activeDeadlineSeconds', podspec.model)
        self.assertIsInstance(podspec.model['activeDeadlineSeconds'], int)
        self.assertEqual(d, podspec.model['activeDeadlineSeconds'])

    # --------------------------------------------------------------------------------- set pod node name

    def test_pod_set_pod_node_name_none_arg(self):
        obj = self._create_pod()
        nodename = None
        try:
            obj.set_pod_node_name(name=nodename)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_set_pod_node_name_invalid_arg(self):
        obj = self._create_pod()
        nodename = 666
        try:
            obj.set_pod_node_name(name=nodename)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_set_pod_node_name(self):
        obj = self._create_pod()
        nodename = "yonodename"
        obj.set_pod_node_name(name=nodename)

        podspec = obj.model.model['spec']
        self.assertIn('nodeName', podspec)
        self.assertIsInstance(podspec['nodeName'], str)
        self.assertEqual(nodename, podspec['nodeName'])

        podspec = obj.model.pod_spec
        self.assertIn('nodeName', podspec.model)
        self.assertIsInstance(podspec.model['nodeName'], str)
        self.assertEqual(nodename, podspec.model['nodeName'])

    # --------------------------------------------------------------------------------- set pod node selector

    def test_pod_set_pod_node_selector_none_arg(self):
        obj = self._create_pod()
        s_in = None
        try:
            obj.set_pod_node_selector(new_dict=s_in)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_set_pod_node_selector_invalid_arg(self):
        obj = self._create_pod()
        s_in = "yoselector"
        try:
            obj.set_pod_node_selector(new_dict=s_in)
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_set_pod_node_selector(self):
        obj = self._create_pod()
        s = {"disktype": "ssd"}
        obj.set_pod_node_selector(new_dict=s)

        podspec = obj.model.model['spec']
        self.assertIn('nodeSelector', podspec)
        self.assertIsInstance(podspec['nodeSelector'], dict)
        self.assertEqual(s, podspec['nodeSelector'])

        podspec = obj.model.pod_spec
        self.assertIn('nodeSelector', podspec.model)
        self.assertIsInstance(podspec.model['nodeSelector'], dict)
        self.assertEqual(s, podspec.model['nodeSelector'])

    # --------------------------------------------------------------------------------- set pod restart policy

    def test_pod_set_pod_restart_policy_none_arg(self):
        obj = self._create_pod()
        try:
            obj.set_pod_restart_policy()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_set_pod_restart_policy_not_a_string(self):
        obj = self._create_pod()
        policy = 666
        try:
            obj.set_pod_restart_policy(policy=policy)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_set_pod_restart_policy_invalid_arg(self):
        obj = self._create_pod()
        policy = 'yopolicy'
        try:
            obj.set_pod_restart_policy(policy=policy)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_set_pod_restart_policy(self):
        obj = self._create_pod()
        policy = 'Always'
        obj.set_pod_restart_policy(policy=policy)
        p = obj.get_pod_restart_policy()
        self.assertEqual(policy, p)

    # --------------------------------------------------------------------------------- set pod service account

    def test_pod_set_service_account_none_arg(self):
        obj = self._create_pod()
        try:
            obj.set_service_account()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_set_service_account_invalid_arg(self):
        obj = self._create_pod()
        name = 666
        try:
            obj.set_service_account(name)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_set_service_account(self):
        obj = self._create_pod()
        name_in = "yoservice"
        obj.set_service_account(name_in)
        name_out = obj.get_service_account()
        self.assertEqual(name_in, name_out)

    # --------------------------------------------------------------------------------- set termination grace period

    def test_pod_set_termination_grace_period_none_arg(self):
        obj = self._create_pod()
        try:
            obj.set_termination_grace_period()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_set_termination_grace_period_invalid_arg(self):
        obj = self._create_pod()
        secs = -666
        try:
            obj.set_termination_grace_period(secs)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_pod_set_termination_grace_period(self):
        obj = self._create_pod()
        secs_in = 1234
        obj.set_termination_grace_period(secs_in)
        secs_out = obj.get_termination_grace_period()
        self.assertEqual(secs_in, secs_out)

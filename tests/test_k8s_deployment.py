#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import unittest
import utils
import uuid
from kubernetes import K8sDeployment, K8sConfig
from kubernetes.K8sExceptions import *


class K8sDeploymentTests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        utils.cleanup_objects()

    # --------------------------------------------------------------------------------- init

    def test_init_no_args(self):
        try:
            K8sDeployment()
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
            K8sDeployment(config=config)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_init_with_invalid_name(self):
        name = object()
        try:
            utils.create_rc(name=name)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_init_with_name(self):
        name = "yomama"
        rc = utils.create_rc(name=name)
        self.assertIsNotNone(rc)
        self.assertIsInstance(rc, K8sDeployment)
        self.assertEqual(rc.name, name)

    # ------------------------------------------x--------------------------------------- api - create

    def test_create_no_args(self):
        name = "yodep-{0}".format(unicode(uuid.uuid4()))
        dep = utils.create_deployment(name=name)
        if utils.is_reachable(dep.config.api_host):
            try:
                dep.create()
                self.fail("Should not fail.")
            except Exception as err:
                self.assertIsInstance(err, UnprocessableEntityException)

    def test_create_zero_replicas(self):
        name = "yodep-{0}".format(unicode(uuid.uuid4()))
        dep = utils.create_deployment(name=name)
        cont_name = "redis"
        cont_image = "redis:3.2.3"
        cont = utils.create_container(name=cont_name, image=cont_image)
        dep.add_container(container=cont)
        if utils.is_reachable(dep.config.api_host):
            d = dep.create()
            self.assertIsNotNone(d)
            self.assertIsInstance(d, K8sDeployment)
            self.assertEqual(d, dep)
            self.assertEqual(0, d.model.model['spec']['replicas'])
            self.assertNotIn('replicas', d.model.model['status'])
            self.assertNotIn('availableReplicas', d.model.model['status'])
            self.assertNotIn('updatedReplicas', d.model.model['status'])

    def test_create_one_replica(self):
        name = "yodep-{0}".format(unicode(uuid.uuid4()))
        dep = utils.create_deployment(name=name)
        cont_name = "nginx"
        cont_image = "nginx:1.7.9"
        cont = utils.create_container(name=cont_name, image=cont_image)
        dep.add_container(container=cont)
        dep.set_replicas(1)
        if utils.is_reachable(dep.config.api_host):
            d = dep.create()
            self.assertIsNotNone(d)
            self.assertIsInstance(d, K8sDeployment)
            self.assertEqual(d, dep)
            self.assertEqual(1, d.model.model['status']['replicas'])
            self.assertEqual(1, d.model.model['status']['availableReplicas'])
            self.assertEqual(1, d.model.model['status']['updatedReplicas'])

    def test_create_three_replicas(self):
        name = "yodep-{0}".format(unicode(uuid.uuid4()))
        dep = utils.create_deployment(name=name)
        cont_name = "nginx"
        cont_image = "nginx:1.7.9"
        cont = utils.create_container(name=cont_name, image=cont_image)
        dep.add_container(container=cont)
        dep.set_replicas(3)
        if utils.is_reachable(dep.config.api_host):
            d = dep.create()
            self.assertIsNotNone(d)
            self.assertIsInstance(d, K8sDeployment)
            self.assertEqual(d, dep)
            self.assertEqual(3, d.model.model['status']['replicas'])
            self.assertEqual(3, d.model.model['status']['availableReplicas'])
            self.assertEqual(3, d.model.model['status']['updatedReplicas'])

    def test_create_already_exists(self):
        name = "yodep-{0}".format(unicode(uuid.uuid4()))
        dep = utils.create_deployment(name=name)
        cont_name = "nginx"
        cont_image = "nginx:1.7.9"
        cont = utils.create_container(name=cont_name, image=cont_image)
        dep.add_container(container=cont)
        dep.set_replicas(1)
        if utils.is_reachable(dep.config.api_host):
            dep.create()
            try:
                dep.create()
            except Exception as err:
                self.assertIsInstance(err, AlreadyExistsException)

    # ------------------------------------------x--------------------------------------- api - list

    def test_list_nonexistent(self):
        name = "yodep-{0}".format(unicode(uuid.uuid4()))
        dep = utils.create_deployment(name=name)
        if utils.is_reachable(dep.config.api_host):
            objs = dep.list()
            self.assertIsInstance(objs, list)
            self.assertEqual(0, len(objs))

    def test_list_multiple(self):
        name = "yocontainer"
        container = utils.create_container(name=name)
        config = K8sConfig(kubeconfig=utils.kubeconfig_fallback)
        deployments = []
        count = 3
        objs = []
        if utils.is_reachable(config.api_host):
            for i in range(0, count):
                name = "yodep-{0}".format(unicode(uuid.uuid4()))
                dep = utils.create_deployment(config, name)
                dep.add_container(container)
                result = dep.create()
                self.assertIsInstance(result, K8sDeployment)
                self.assertEqual(dep, result)
                deployments.append(dep)
                objs = dep.list()
            self.assertEqual(count, len(deployments))
            self.assertEqual(count, len(objs))

    # --------------------------------------------------------------------------------- api - update



    # --------------------------------------------------------------------------------- api - delete

    def test_delete_nonexistent(self):
        name = "yorc-{0}".format(unicode(uuid.uuid4()))
        dep = utils.create_deployment(name=name)
        if utils.is_reachable(dep.config.api_host):
            try:
                dep.delete()
                self.fail("Should not fail.")
            except Exception as err:
                self.assertIsInstance(err, NotFoundException)

    def test_delete(self):
        name = "yocontainer"
        container = utils.create_container(name=name)
        name = "yodep-{0}".format(unicode(uuid.uuid4()))
        dep = utils.create_deployment(name=name)
        dep.add_container(container)
        if utils.is_reachable(dep.config.api_host):
            dep.create()
            utils.cleanup_deployments()
            result = dep.list()
            self.assertIsInstance(result, list)
            self.assertEqual(0, len(result))

    # -------------------------------------------------------------------------------------  get by name

    def test_get_by_name_none_args(self):
        try:
            K8sDeployment.get_by_name()
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_get_by_name_invalid_config(self):
        name = "yoname"
        config = object()
        try:
            K8sDeployment.get_by_name(config=config, name=name)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_get_by_name_invalid_name(self):
        name = object()
        try:
            K8sDeployment.get_by_name(name=name)
            self.fail("Should not fail.")
        except Exception as err:
            self.assertIsInstance(err, SyntaxError)

    def test_get_by_name_nonexistent(self):
        name = "yodep-{0}".format(unicode(uuid.uuid4()))
        dep = utils.create_deployment(name=name)
        if utils.is_reachable(dep.config.api_host):
            result = K8sDeployment.get_by_name(config=dep.config, name=name)
            self.assertIsInstance(result, list)
            self.assertEqual(0, len(result))

    def test_get_by_name(self):
        cont_name = "yocontainer"
        container = utils.create_container(name=cont_name)
        name = "yodep-{0}".format(unicode(uuid.uuid4()))
        dep = utils.create_deployment(name=name)
        dep.add_container(container)
        if utils.is_reachable(dep.config.api_host):
            dep.create()
            result = K8sDeployment.get_by_name(config=dep.config, name=name)
            self.assertIsInstance(result, list)
            self.assertEqual(1, len(result))
            self.assertIsInstance(result[0], K8sDeployment)
            self.assertEqual(dep, result[0])

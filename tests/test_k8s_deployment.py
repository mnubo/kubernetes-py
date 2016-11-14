#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import unittest
import uuid

import utils
from kubernetes import K8sDeployment, K8sConfig
from kubernetes.K8sExceptions import *


class K8sDeploymentTests(unittest.TestCase):
    
    def setUp(self):
        utils.cleanup_deployments()
        utils.cleanup_rs()
        utils.cleanup_pods()

    def tearDown(self):
        utils.cleanup_deployments()
        utils.cleanup_rs()
        utils.cleanup_pods()

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
        with self.assertRaises(SyntaxError):
            K8sDeployment(config=config)

    def test_init_with_invalid_name(self):
        name = object()
        with self.assertRaises(SyntaxError):
            utils.create_rc(name=name)

    def test_init_with_name(self):
        name = "yomama"
        dep = utils.create_deployment(name=name)
        self.assertIsNotNone(dep)
        self.assertIsInstance(dep, K8sDeployment)
        self.assertEqual(dep.name, name)

    # ------------------------------------------x--------------------------------------- api - create

    def test_create_no_args(self):
        name = "yodep-{0}".format(str(uuid.uuid4()))
        dep = utils.create_deployment(name=name)
        if utils.is_reachable(dep.config.api_host):
            with self.assertRaises(UnprocessableEntityException):
                dep.create()

    def test_create_zero_replicas(self):
        name = "yodep-{0}".format(str(uuid.uuid4()))
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
            self.assertEqual(0, d.desired_replicas)
            self.assertIsNone(d.available_replicas)
            self.assertIsNone(d.current_replicas)
            self.assertIsNone(d.unavailable_replicas)
            self.assertIsNone(d.updated_replicas)

    def test_create_one_replica(self):
        name = "yodep-{0}".format(str(uuid.uuid4()))
        dep = utils.create_deployment(name=name)
        cont_name = "nginx"
        cont_image = "nginx:1.7.9"
        cont = utils.create_container(name=cont_name, image=cont_image)
        dep.add_container(container=cont)
        dep.desired_replicas = 1
        if utils.is_reachable(dep.config.api_host):
            d = dep.create()
            self.assertIsNotNone(d)
            self.assertIsInstance(d, K8sDeployment)
            self.assertEqual(d, dep)
            self.assertEqual(1, d.desired_replicas)
            self.assertEqual(1, d.available_replicas)
            self.assertEqual(1, d.updated_replicas)

    def test_create_three_replicas(self):
        name = "yodep-{0}".format(str(uuid.uuid4()))
        dep = utils.create_deployment(name=name)
        cont_name = "nginx"
        cont_image = "nginx:1.7.9"
        cont = utils.create_container(name=cont_name, image=cont_image)
        dep.add_container(container=cont)
        dep.desired_replicas = 3
        if utils.is_reachable(dep.config.api_host):
            d = dep.create()
            self.assertIsNotNone(d)
            self.assertIsInstance(d, K8sDeployment)
            self.assertEqual(d, dep)
            self.assertEqual(3, d.desired_replicas)
            self.assertEqual(3, d.available_replicas)
            self.assertEqual(3, d.updated_replicas)

    def test_create_already_exists(self):
        name = "yodep-{0}".format(str(uuid.uuid4()))
        dep = utils.create_deployment(name=name)
        cont_name = "nginx"
        cont_image = "nginx:1.7.9"
        cont = utils.create_container(name=cont_name, image=cont_image)
        dep.add_container(container=cont)
        dep.desired_replicas = 1
        if utils.is_reachable(dep.config.api_host):
            dep.create()
            with self.assertRaises(AlreadyExistsException):
                dep.create()

    # --------------------------------------------------------------------------------- api - list

    def test_list_nonexistent(self):
        name = "yodep-{0}".format(str(uuid.uuid4()))
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
                name = "yodep-{0}".format(str(uuid.uuid4()))
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

    def test_update_nonexistent(self):
        name = "yodep-{0}".format(str(uuid.uuid4()))
        dep = utils.create_deployment(name=name)
        if utils.is_reachable(dep.config.api_host):
            with self.assertRaises(NotFoundException):
                dep.update()

    def test_update_name_fails(self):
        name = "yocontainer"
        container = utils.create_container(name=name)
        name1 = "yodep1"
        name2 = "yodep2"
        dep = utils.create_deployment(name=name1)
        dep.add_container(container)
        if utils.is_reachable(dep.config.api_host):
            dep.create()
            dep.name = name2
            with self.assertRaises(BadRequestException):
                dep.update()

    def test_update_namespace_fails(self):
        name = "yocontainer"
        container = utils.create_container(name=name)
        name = "yorc-{0}".format(str(uuid.uuid4()))
        nspace = "yonamespace"
        dep = utils.create_deployment(name=name)
        dep.add_container(container)
        if utils.is_reachable(dep.config.api_host):
            dep.create()
            dep.namespace = nspace
            with self.assertRaises(BadRequestException):
                dep.update()

    def test_update_container_image(self):
        name = "nginx"
        image1 = "nginx:1.7.9"
        image2 = "nginx:1.9.1"
        container = utils.create_container(name=name, image=image1)
        dep_name = "yodep-{0}".format(str(uuid.uuid4()))
        dep = utils.create_deployment(name=dep_name)
        dep.add_container(container)
        dep.desired_replicas = 3
        if utils.is_reachable(dep.config.api_host):
            dep.create()
            self.assertEqual(image1, dep.containers[0].image)
            dep.container_image = (name, image2)
            d = dep.update()
            self.assertIn('deployment.kubernetes.io/revision', dep.annotations)
            self.assertNotEqual(image1, d.containers[0].image)
            self.assertEqual(image2, d.containers[0].image)

    def test_update_labels(self):
        name = "nginx"
        image = "nginx:1.7.9"
        container = utils.create_container(name=name, image=image)
        dep_name = "yodep-{0}".format(str(uuid.uuid4()))
        dep = utils.create_deployment(name=dep_name)
        dep.add_container(container)
        dep.set_replicas(3)
        if utils.is_reachable(dep.config.api_host):
            dep.create()
            labels = dep.get_labels()
            labels['newkey'] = 'newvalue'
            dep.set_labels(labels)
            updated = dep.update()
            self.assertEqual(labels, updated.get_labels())

    def test_update_pod_labels(self):
        name = "nginx"
        image = "nginx:1.7.9"
        container = utils.create_container(name=name, image=image)
        dep_name = "yodep-{0}".format(str(uuid.uuid4()))
        dep = utils.create_deployment(name=dep_name)
        dep.add_container(container)
        dep.set_replicas(3)
        if utils.is_reachable(dep.config.api_host):
            dep.create()
            labels = dep.get_pod_labels()
            labels['newkey'] = 'newvalue'
            dep.set_pod_labels(labels)
            updated = dep.update()
            self.assertEqual(labels, updated.get_pod_labels())

    # --------------------------------------------------------------------------------- api - rollback

    def test_rollback_no_args(self):
        name = "nginx"
        image1 = "nginx:1.7.9"
        image2 = "nginx:1.9.1"
        container = utils.create_container(name=name, image=image1)
        dep_name = "yodep-{0}".format(str(uuid.uuid4()))
        dep = utils.create_deployment(name=dep_name)
        dep.add_container(container)
        dep.desired_replicas = 3
        if utils.is_reachable(dep.config.api_host):
            dep.create()
            self.assertEqual(image1, dep.containers[0].image)
            dep.container_image = (name, image2)
            dep.update()
            self.assertIn('deployment.kubernetes.io/revision', dep.annotations)
            self.assertNotEqual(image1, dep.containers[0].image)
            self.assertEqual(image2, dep.containers[0].image)
            dep.rollback()

    # --------------------------------------------------------------------------------- api - delete

    def test_delete_nonexistent(self):
        name = "yorc-{0}".format(str(uuid.uuid4()))
        dep = utils.create_deployment(name=name)
        if utils.is_reachable(dep.config.api_host):
            with self.assertRaises(NotFoundException):
                dep.delete()

    def test_delete(self):
        name = "yocontainer"
        container = utils.create_container(name=name)
        name = "yodep-{0}".format(str(uuid.uuid4()))
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
        with self.assertRaises(SyntaxError):
            K8sDeployment.get_by_name()

    def test_get_by_name_invalid_config(self):
        name = "yoname"
        config = object()
        with self.assertRaises(SyntaxError):
            K8sDeployment.get_by_name(config=config, name=name)

    def test_get_by_name_invalid_name(self):
        name = object()
        with self.assertRaises(SyntaxError):
            K8sDeployment.get_by_name(name=name)

    def test_get_by_name_nonexistent(self):
        name = "yodep-{0}".format(str(uuid.uuid4()))
        dep = utils.create_deployment(name=name)
        if utils.is_reachable(dep.config.api_host):
            result = K8sDeployment.get_by_name(config=dep.config, name=name)
            self.assertIsInstance(result, list)
            self.assertEqual(0, len(result))

    def test_get_by_name(self):
        cont_name = "yocontainer"
        container = utils.create_container(name=cont_name)
        name = "yodep-{0}".format(str(uuid.uuid4()))
        dep = utils.create_deployment(name=name)
        dep.add_container(container)
        if utils.is_reachable(dep.config.api_host):
            dep.create()
            result = K8sDeployment.get_by_name(config=dep.config, name=name)
            self.assertIsInstance(result, list)
            self.assertEqual(1, len(result))
            self.assertIsInstance(result[0], K8sDeployment)
            self.assertEqual(dep, result[0])

    # -------------------------------------------------------------------------------------  get scale

    def test_scale(self):
        cont_name = "yocontainer"
        container = utils.create_container(name=cont_name)
        name = "yodep-{0}".format(str(uuid.uuid4()))
        dep = utils.create_deployment(name=name)
        dep.add_container(container)
        dep.set_replicas(3)
        if utils.is_reachable(dep.config.api_host):
            dep.create()
            replicas = dep.get_replicas()
            for k in replicas:
                self.assertEqual(3, replicas[k])
            dep.scale(5)
            replicas = dep.get_replicas()
            for k in replicas:
                self.assertEqual(5, replicas[k])

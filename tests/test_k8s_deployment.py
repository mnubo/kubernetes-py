#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import time
import uuid

from kubernetes_py.K8sConfig import K8sConfig
from kubernetes_py.K8sContainer import K8sContainer
from kubernetes_py.K8sDeployment import K8sDeployment
from kubernetes_py.K8sExceptions import *
from kubernetes_py.K8sPod import K8sPod
from kubernetes_py.K8sReplicaSet import K8sReplicaSet
from tests import _utils
from tests.BaseTest import BaseTest


class K8sDeploymentTests(BaseTest):
    def setUp(self):
        _utils.cleanup_nodes()
        _utils.cleanup_deployments()
        _utils.cleanup_rs()
        _utils.cleanup_pods()

    def tearDown(self):
        _utils.cleanup_nodes()
        _utils.cleanup_deployments()
        _utils.cleanup_rs()
        _utils.cleanup_pods()

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
            _utils.create_deployment(name=name)

    def test_init_with_name(self):
        name = "yomama"
        dep = _utils.create_deployment(name=name)
        self.assertIsNotNone(dep)
        self.assertIsInstance(dep, K8sDeployment)
        self.assertEqual(dep.name, name)

    # ------------------------------------------x--------------------------------------- api - create

    def test_create_no_args(self):
        name = "yodep-{0}".format(str(uuid.uuid4()))
        dep = _utils.create_deployment(name=name)

        if _utils.is_reachable(dep.config):
            with self.assertRaises(UnprocessableEntityException):
                dep.create()

    def test_create_zero_replicas(self):
        name = "yodep-{0}".format(str(uuid.uuid4()))
        dep = _utils.create_deployment(name=name)
        cont_name = "redis"
        cont_image = "redis:3.2.3"
        cont = _utils.create_container(name=cont_name, image=cont_image)
        dep.add_container(container=cont)

        if _utils.is_reachable(dep.config):
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
        dep = _utils.create_deployment(name=name)
        cont_name = "nginx"
        cont_image = "nginx:1.7.9"
        cont = _utils.create_container(name=cont_name, image=cont_image)
        dep.add_container(container=cont)
        dep.desired_replicas = 1

        if _utils.is_reachable(dep.config):
            d = dep.create()
            self.assertIsNotNone(d)
            self.assertIsInstance(d, K8sDeployment)
            self.assertEqual(d, dep)
            self.assertEqual(1, d.desired_replicas)
            self.assertEqual(1, d.available_replicas)
            self.assertEqual(1, d.updated_replicas)

    def test_create_three_replicas(self):
        name = "yodep-{0}".format(str(uuid.uuid4()))
        dep = _utils.create_deployment(name=name)
        cont_name = "nginx"
        cont_image = "nginx:1.7.9"
        cont = _utils.create_container(name=cont_name, image=cont_image)
        dep.add_container(container=cont)
        dep.desired_replicas = 3

        if _utils.is_reachable(dep.config):
            d = dep.create()
            self.assertIsNotNone(d)
            self.assertIsInstance(d, K8sDeployment)
            self.assertEqual(d, dep)
            self.assertEqual(3, d.desired_replicas)
            self.assertEqual(3, d.available_replicas)
            self.assertEqual(3, d.updated_replicas)

    def test_create_already_exists(self):
        name = "yodep-{0}".format(str(uuid.uuid4()))
        dep = _utils.create_deployment(name=name)
        cont_name = "nginx"
        cont_image = "nginx:1.7.9"
        cont = _utils.create_container(name=cont_name, image=cont_image)
        dep.add_container(container=cont)
        dep.desired_replicas = 1

        if _utils.is_reachable(dep.config):
            dep.create()
            with self.assertRaises(AlreadyExistsException):
                dep.create()

    # --------------------------------------------------------------------------------- api - list

    def test_list(self):
        name = "yodep-{0}".format(str(uuid.uuid4()))
        dep = _utils.create_deployment(name=name)
        cont_name = "redis"
        cont_image = "redis:3.2.3"
        cont = _utils.create_container(name=cont_name, image=cont_image)
        dep.add_container(container=cont)

        if _utils.is_reachable(dep.config):
            dep.create()
            objs = dep.list()
            for x in objs:
                self.assertIsInstance(x, K8sDeployment)

    def test_list_multiple(self):
        name = "yocontainer"
        container = _utils.create_container(name=name)
        config = K8sConfig(kubeconfig=_utils.kubeconfig_fallback)
        deployments = []
        count = 3
        objs = []

        if _utils.is_reachable(config):
            for i in range(0, count):
                name = "yodep-{0}".format(str(uuid.uuid4()))
                dep = _utils.create_deployment(config, name)
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
        dep = _utils.create_deployment(name=name)

        if _utils.is_reachable(dep.config):
            with self.assertRaises(NotFoundException):
                dep.update()

    def test_update_name_fails(self):
        name = "yocontainer"
        container = _utils.create_container(name=name)
        name1 = "yodep1"
        name2 = "yodep2"
        dep = _utils.create_deployment(name=name1)
        dep.add_container(container)

        if _utils.is_reachable(dep.config):
            dep.create()
            dep.name = name2
            with self.assertRaises(NotFoundException):
                dep.update()

    def test_update_namespace_fails(self):
        name = "yocontainer"
        container = _utils.create_container(name=name)
        name = "yorc-{0}".format(str(uuid.uuid4()))
        nspace = "yonamespace"
        dep = _utils.create_deployment(name=name)
        dep.add_container(container)

        if _utils.is_reachable(dep.config):
            dep.create()
            dep.namespace = nspace
            with self.assertRaises(BadRequestException):
                dep.update()

    def test_update_container_image(self):
        name = "nginx"
        image1 = "nginx:1.7.9"
        image2 = "nginx:1.9.1"
        container = _utils.create_container(name=name, image=image1)
        dep_name = "yodep-{0}".format(str(uuid.uuid4()))
        dep = _utils.create_deployment(name=dep_name)
        dep.add_container(container)
        dep.desired_replicas = 3

        if _utils.is_reachable(dep.config):
            dep.create()
            self.assertEqual(image1, dep.containers[0].image)
            dep.container_image = (name, image2)
            d = dep.update()
            self.assertIn("deployment.kubernetes.io/revision", dep.annotations)
            self.assertNotEqual(image1, d.containers[0].image)
            self.assertEqual(image2, d.containers[0].image)

    def test_update_labels(self):
        name = "nginx"
        image = "nginx:1.7.9"
        container = _utils.create_container(name=name, image=image)
        dep_name = "yodep-{0}".format(str(uuid.uuid4()))
        dep = _utils.create_deployment(name=dep_name)
        dep.add_container(container)
        dep.desired_replicas = 3

        if _utils.is_reachable(dep.config):
            dep.create()
            labels = dep.labels
            labels["newkey"] = "newvalue"
            dep.labels = labels
            updated = dep.update()
            self.assertEqual(labels, updated.labels)

    def test_update_pod_labels(self):
        name = "nginx"
        image = "nginx:1.7.9"
        container = _utils.create_container(name=name, image=image)
        dep_name = "yodep-{0}".format(str(uuid.uuid4()))
        dep = _utils.create_deployment(name=dep_name)
        dep.add_container(container)
        dep.desired_replicas = 3

        if _utils.is_reachable(dep.config):
            dep.create()
            labels = dep.pod_labels
            labels["newkey"] = "newvalue"
            dep.pod_labels = labels
            updated = dep.update()
            self.assertEqual(labels, updated.pod_labels)

    # --------------------------------------------------------------------------------- api - rollback

    def test_rollback_no_args(self):
        name = "nginx"
        image1 = "nginx:1.7.9"
        image2 = "nginx:1.9.1"
        container = _utils.create_container(name=name, image=image1)
        dep_name = "yodep-{0}".format(str(uuid.uuid4()))
        dep = _utils.create_deployment(name=dep_name)
        dep.add_container(container)
        dep.desired_replicas = 3

        if _utils.is_reachable(dep.config):
            dep.create()
            self.assertEqual(image1, dep.containers[0].image)
            dep.container_image = (name, image2)
            dep.update()
            self.assertIn("deployment.kubernetes.io/revision", dep.annotations)
            rev_before = dep.get_annotation("deployment.kubernetes.io/revision")
            self.assertNotEqual(image1, dep.containers[0].image)
            self.assertEqual(image2, dep.containers[0].image)
            dep.rollback()
            self.assertIn("deployment.kubernetes.io/revision", dep.annotations)
            rev_after = dep.get_annotation("deployment.kubernetes.io/revision")
            self.assertNotEqual(rev_before, rev_after)
            self.assertGreater(rev_after, rev_before)
            self.assertEqual(image1, dep.containers[0].image)
            self.assertNotEqual(image2, dep.containers[0].image)

    # --------------------------------------------------------------------------------- api - delete

    def test_delete_nonexistent(self):
        name = "yorc-{0}".format(str(uuid.uuid4()))
        dep = _utils.create_deployment(name=name)

        if _utils.is_reachable(dep.config):
            with self.assertRaises(NotFoundException):
                dep.delete()

    def test_delete_no_cascade(self):
        name = "yocontainer"
        container = _utils.create_container(name=name)
        name = "yodep-{0}".format(str(uuid.uuid4()))
        dep = _utils.create_deployment(name=name)
        dep.add_container(container)
        dep.desired_replicas = 3

        if _utils.is_reachable(dep.config):
            dep.create()
            dep.delete(cascade=False)
            result = dep.list()
            self.assertIsInstance(result, list)
            self.assertEqual(0, len(result))
            repsets = K8sReplicaSet(config=dep.config, name="yo").list()
            self.assertEqual(1, len(repsets))
            pods = K8sPod(config=dep.config, name="yo").list()
            self.assertEqual(3, len(pods))

    def test_delete_cascade(self):
        c_redis = _utils.create_container(name="redis", image="redis")
        c_nginx = _utils.create_container(name="nginx", image="nginx")
        name = "yodep-{0}".format(str(uuid.uuid4()))
        dep = _utils.create_deployment(name=name)
        dep.add_container(c_redis)
        dep.desired_replicas = 3

        if _utils.is_reachable(dep.config):
            dep.create()
            dep.add_container(c_nginx)
            dep.update()
            repsets = K8sReplicaSet(config=dep.config, name="yo").list()
            self.assertEqual(2, len(repsets))
            pods = K8sPod(config=dep.config, name="yo").list()
            self.assertLessEqual(3, len(pods))  # rollout burst
            dep.delete(cascade=True)
            result = dep.list()
            self.assertIsInstance(result, list)
            self.assertEqual(0, len(result))
            repsets = K8sReplicaSet(config=dep.config, name="yo").list()
            self.assertEqual(0, len(repsets))
            pods = K8sPod(config=dep.config, name="yo").list()
            self.assertEqual(0, len(pods))

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
        dep = _utils.create_deployment(name=name)

        if _utils.is_reachable(dep.config):
            result = K8sDeployment.get_by_name(config=dep.config, name=name)
            self.assertIsInstance(result, list)
            self.assertEqual(0, len(result))

    def test_get_by_name(self):
        cont_name = "yocontainer"
        container = _utils.create_container(name=cont_name)
        name = "yodep-{0}".format(str(uuid.uuid4()))
        dep = _utils.create_deployment(name=name)
        dep.add_container(container)

        if _utils.is_reachable(dep.config):
            dep.create()
            result = K8sDeployment.get_by_name(config=dep.config, name=name)
            self.assertIsInstance(result, list)
            self.assertEqual(1, len(result))
            self.assertIsInstance(result[0], K8sDeployment)
            self.assertEqual(dep, result[0])

    # ------------------------------------------------------------------------------------- scale

    def test_scale(self):
        cont_name = "yocontainer"
        container = _utils.create_container(name=cont_name)
        name = "yodep-{0}".format(str(uuid.uuid4()))
        dep = _utils.create_deployment(name=name)
        dep.add_container(container)
        dep.desired_replicas = 2

        if _utils.is_reachable(dep.config):
            dep.create()
            self.assertEqual(2, dep.desired_replicas)
            self.assertEqual(2, dep.updated_replicas)
            self.assertEqual(2, dep.available_replicas)
            dep.scale(3)
            self.assertEqual(3, dep.desired_replicas)
            self.assertEqual(3, dep.updated_replicas)
            self.assertEqual(3, dep.available_replicas)
            dep.scale(1)
            self.assertEqual(1, dep.desired_replicas)
            self.assertEqual(1, dep.updated_replicas)
            self.assertEqual(1, dep.available_replicas)

    def test_update_container_image_keep_env_vars(self):
        name = "yodep-{0}".format(str(uuid.uuid4()))
        dep = _utils.create_deployment(name=name)
        cont_name = "nginx"
        cont_image = "nginx:1.7.9"
        new_image = "nginx:1.10.3"
        env_var_name = "YoVariable"
        cont = _utils.create_container(name=cont_name, image=cont_image)
        cont.add_env(name=env_var_name, value=name)
        dep.add_container(container=cont)
        dep.desired_replicas = 1

        if _utils.is_reachable(dep.config):
            dep.create()
            with self.assertRaises(AlreadyExistsException):
                dep.create()
            # Change the container image
            dep.container_image = (cont_name, new_image)
            # Update the deployment
            dep.update()
            # Refresh
            dep.get()
            for c in dep.containers:
                self.assertIsInstance(c, K8sContainer)
                if c.name == cont_name:
                    self.assertEqual(c.image, new_image)
                    self.assertEqual(c.env[0].name, env_var_name)
                    self.assertEqual(c.env[0].value, name)

    # ---------------------------------------------------------------------------------- revision

    def test_revision(self):
        c_redis = _utils.create_container(name="redis", image="redis")
        c_nginx = _utils.create_container(name="nginx", image="nginx")
        c_postgres = _utils.create_container(name="postgres", image="postgres:alpine")

        name = "yodep-{0}".format(str(uuid.uuid4()))
        dep = _utils.create_deployment(name=name)
        dep.add_container(c_redis)
        dep.desired_replicas = 2

        if _utils.is_reachable(dep.config):
            dep.create()
            self.assertEqual(1, dep.revision)
            dep.add_container(c_nginx)
            dep.update()
            time.sleep(5)
            dep.get()
            self.assertEqual(2, dep.revision)
            dep.add_container(c_postgres)
            dep.update()
            time.sleep(5)
            dep.get()
            self.assertEqual(3, dep.revision)
            dep.rollback(revision=1)
            time.sleep(5)
            dep.get()
            self.assertEqual(4, dep.revision)
            dep.add_container(c_nginx)
            dep.update()
            time.sleep(5)
            dep.get()
            self.assertEqual(5, dep.revision)

    # ---------------------------------------------------------------------------------- replicaset creationTimestamp

    def test_replicaset_creation_timestamp(self):
        c_redis = _utils.create_container(name="redis", image="redis")
        c_nginx_1 = _utils.create_container(name="nginx", image="nginx")
        c_nginx_2 = _utils.create_container(name="postgres", image="postgres:alpine")

        name = "yodep-{0}".format(str(uuid.uuid4()))
        dep = _utils.create_deployment(name=name)
        dep.add_container(c_redis)
        dep.desired_replicas = 2

        if _utils.is_reachable(dep.config):
            dep.create()
            self.assertEqual(1, dep.revision)
            dep.add_container(c_nginx_1)
            dep.update()
            dep.get()
            self.assertEqual(2, dep.revision)
            dep.add_container(c_nginx_2)
            dep.update()
            dep.get()
            self.assertEqual(3, dep.revision)

            rsets = K8sReplicaSet(config=dep.config, name="yo").list()
            for i in range(0, len(rsets) - 1):
                self.assertGreaterEqual(rsets[i].creation_timestamp, rsets[i + 1].creation_timestamp)

    # ---------------------------------------------------------------------------------- replicaset purge

    def test_purge_replica_set(self):
        c_redis = _utils.create_container(name="redis", image="redis")
        c_nginx = _utils.create_container(name="nginx", image="nginx")
        c_postgres = _utils.create_container(name="postgres", image="postgres:alpine")
        # c_memcached = utils.create_container(name="memcached", image="memcached:alpine")

        name = "yodep-{0}".format(str(uuid.uuid4()))
        dep = _utils.create_deployment(name=name)
        dep.add_container(c_redis)
        dep.desired_replicas = 2

        if _utils.is_reachable(dep.config):
            dep.create()
            dep.add_container(c_nginx)
            dep.update()
            dep.add_container(c_postgres)
            dep.update()
            rsets = K8sReplicaSet(config=dep.config, name="yo").list()
            self.assertEqual(3, len(rsets))
            dep.purge_replica_sets(keep=2)
            rsets = K8sReplicaSet(config=dep.config, name="yo").list()
            self.assertEqual(2, len(rsets))

#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import time
import uuid

from kubernetes_py.K8sCronJob import K8sCronJob
from kubernetes_py.K8sPod import K8sPod
from kubernetes_py.models.v2alpha1.CronJob import CronJob
from kubernetes_py.K8sExceptions import CronJobAlreadyRunningException
from tests import _constants
from tests import _utils
from tests.BaseTest import BaseTest


class K8sCronJobTests(BaseTest):

    def setUp(self):
        _utils.cleanup_cronjobs()
        _utils.cleanup_jobs()
        _utils.cleanup_pods()

    def tearDown(self):
        _utils.cleanup_cronjobs()
        _utils.cleanup_jobs()
        _utils.cleanup_pods()

    # --------------------------------------------------------------------------------- init

    def test_init_no_args(self):
        try:
            K8sCronJob()
            self.fail("Should not fail.")
        except SyntaxError:
            pass
        except IOError:
            pass
        except Exception as err:
            self.fail("Unhandled exception: [ {0} ]".format(err))

    def test_init_with_invalid_config(self):
        config = object()
        with self.assertRaises(SyntaxError):
            K8sCronJob(config=config)

    def test_init_with_invalid_name(self):
        name = object()
        with self.assertRaises(SyntaxError):
            _utils.create_cronjob(name=name)

    def test_init_with_name(self):
        name = "yomama"
        rc = _utils.create_cronjob(name=name)
        self.assertIsNotNone(rc)
        self.assertIsInstance(rc, K8sCronJob)
        self.assertEqual(rc.name, name)

    # --------------------------------------------------------------------------------- containers

    def test_containers(self):
        c_name = "redis"
        c_image = "redis:latest"
        c_image_2 = "redis:3.2.3"
        container = _utils.create_container(name=c_name, image=c_image)
        name = "job-{}".format(uuid.uuid4())

        cj = _utils.create_cronjob(name=name)
        cj.add_container(container)
        self.assertEqual(1, len(cj.containers))
        self.assertIn(c_name, cj.container_image)
        self.assertEqual(c_image, cj.container_image[c_name])

        container = _utils.create_container(name=c_name, image=c_image_2)
        cj.add_container(container)
        self.assertEqual(1, len(cj.containers))
        self.assertEqual(c_image_2, cj.container_image[c_name])

    # --------------------------------------------------------------------------------- imagePullSecrets

    def test_add_image_pull_secrets(self):
        cfg = _utils.create_config()
        cfg.pull_secret = [
            {'name': 'secret-name'},
            {'name': 'other-secret-name'},
            {'name': 'secret-name'}  # duplicate
        ]
        cj = _utils.create_cronjob(config=cfg, name="yo")
        self.assertEqual(2, len(cj.image_pull_secrets))  # duplicate not present

    # --------------------------------------------------------------------------------- api - create

    def test_api_create(self):
        name = "job-{}".format(uuid.uuid4())
        job = CronJob(_constants.cronjob())
        k8s_cronjob = _utils.create_cronjob(name=name)
        k8s_cronjob.model = job
        if _utils.is_reachable(k8s_cronjob.config):
            k8s_cronjob.create()
            self.assertIsInstance(k8s_cronjob, K8sCronJob)

    def test_api_create_long_running_with_concurrency(self):
        name = "job-{}".format(uuid.uuid4())
        job = CronJob(_constants.cronjob_90())

        k8s_cronjob = _utils.create_cronjob(name=name)
        k8s_cronjob.model = job
        k8s_cronjob.concurrency_policy = "Allow"

        if _utils.is_reachable(k8s_cronjob.config):
            k8s_cronjob.create()
            self.assertIsInstance(k8s_cronjob, K8sCronJob)
            self.assertEqual('Allow', k8s_cronjob.concurrency_policy)

    def test_api_create_long_running_no_concurrency(self):
        name = "job-{}".format(uuid.uuid4())
        job = CronJob(_constants.cronjob_90())

        k8s_cronjob = _utils.create_cronjob(name=name)
        k8s_cronjob.model = job
        k8s_cronjob.concurrency_policy = "Forbid"
        k8s_cronjob.starting_deadline_seconds = 10

        if _utils.is_reachable(k8s_cronjob.config):
            k8s_cronjob.create()
            self.assertIsInstance(k8s_cronjob, K8sCronJob)
            self.assertEqual('Forbid', k8s_cronjob.concurrency_policy)
            self.assertEqual(10, k8s_cronjob.starting_deadline_seconds)

    # --------------------------------------------------------------------------------- api - list

    def test_list(self):
        name = "job-{}".format(uuid.uuid4())
        job = CronJob(_constants.cronjob_90())

        k8s_cronjob = _utils.create_cronjob(name=name)
        k8s_cronjob.model = job
        k8s_cronjob.concurrency_policy = "Forbid"
        k8s_cronjob.starting_deadline_seconds = 10

        if _utils.is_reachable(k8s_cronjob.config):
            k8s_cronjob.create()
            crons = k8s_cronjob.list()
            for c in crons:
                self.assertIsInstance(c, K8sCronJob)

    # --------------------------------------------------------------------------------- api - last scheduled time

    def test_last_schedule_time(self):
        name = "job-{}".format(uuid.uuid4())
        job = CronJob(_constants.cronjob_90())

        k8s_cronjob = _utils.create_cronjob(name=name)
        k8s_cronjob.model = job
        k8s_cronjob.concurrency_policy = "Forbid"
        k8s_cronjob.starting_deadline_seconds = 10

        if _utils.is_reachable(k8s_cronjob.config):
            k8s_cronjob.create()
            while not k8s_cronjob.last_schedule_time:
                k8s_cronjob.get()
                time.sleep(2)
            lst = k8s_cronjob.last_schedule_time
            self.assertIsNotNone(lst)
            self.assertIsInstance(lst, str)

    # --------------------------------------------------------------------------------- api - pod

    def test_pod(self):
        name = "job-{}".format(uuid.uuid4())
        model = CronJob(_constants.cronjob_90())

        cj = _utils.create_cronjob(name=name)
        cj.model = model
        cj.concurrency_policy = "Forbid"
        cj.starting_deadline_seconds = 10

        if _utils.is_reachable(cj.config):
            cj.create()
            while not cj.last_schedule_time:
                cj.get()
                time.sleep(2)
            pod = cj.pod
            self.assertIsInstance(pod, K8sPod)

    # --------------------------------------------------------------------------------- api - run

    def test_run_already_running(self):
        name = "job-{}".format(uuid.uuid4())
        model = CronJob(_constants.cronjob_90())

        cj = _utils.create_cronjob(name=name)
        cj.model = model
        cj.concurrency_policy = "Forbid"
        cj.starting_deadline_seconds = 10

        if _utils.is_reachable(cj.config):
            cj.create()
            while not cj.last_schedule_time:
                cj.get()
                time.sleep(2)
            with self.assertRaises(CronJobAlreadyRunningException):
                cj.run()

    def test_run(self):
        name = "job-{}".format(uuid.uuid4())
        model = CronJob(_constants.cronjob_90())

        cj = _utils.create_cronjob(name=name)
        cj.model = model
        cj.concurrency_policy = "Forbid"
        cj.starting_deadline_seconds = 10

        if _utils.is_reachable(cj.config):
            cj.create()
            self.assertFalse(cj.suspend)
            cj.run()
            self.assertFalse(cj.suspend)

    # --------------------------------------------------------------------------------- api - activeDeadlineSeconds

    def test_active_deadline_seconds(self):
        ads = 50
        cfg = _utils.create_config()
        cj = CronJob(_constants.cronjob())
        k8s = K8sCronJob(config=cfg, name="yo")
        k8s.model = cj
        self.assertIsNone(k8s.active_deadline_seconds)
        k8s.active_deadline_seconds = ads
        self.assertIsNotNone(k8s.active_deadline_seconds)
        self.assertEqual(k8s.active_deadline_seconds, ads)

    def test_observe_active_deadline_seconds(self):
        cfg = _utils.create_config()
        cj = CronJob(_constants.cronjob_exit_1())
        k8s = K8sCronJob(config=cfg, name="yo")
        k8s.model = cj
        if _utils.is_reachable(cfg):
            k8s.create()
            self.assertIsInstance(k8s, K8sCronJob)

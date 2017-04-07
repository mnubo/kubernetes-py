#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import uuid

from tests import utils
from tests.BaseTest import BaseTest
from kubernetes.K8sJob import K8sJob
from kubernetes.models.v1.Job import Job
from kubernetes.models.v1.JobSpec import JobSpec
from kubernetes.models.v1.JobStatus import JobStatus
from kubernetes.models.v1.ObjectMeta import ObjectMeta


class K8sJobTests(BaseTest):

    def setUp(self):
        utils.cleanup_jobs()
        utils.cleanup_pods()

    def tearDown(self):
        utils.cleanup_jobs()
        utils.cleanup_pods()

    # --------------------------------------------------------------------------------- init

    def test_init_no_args(self):
        try:
            K8sJob()
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
            K8sJob(config=config)

    def test_init_with_invalid_name(self):
        name = object()
        with self.assertRaises(SyntaxError):
            utils.create_job(name=name)

    def test_init_with_name(self):
        name = "yomama"
        rc = utils.create_job(name=name)
        self.assertIsNotNone(rc)
        self.assertIsInstance(rc, K8sJob)
        self.assertEqual(rc.name, name)

    # --------------------------------------------------------------------------------- struct

    def test_struct_k8s_job(self):
        name = "yomama"
        job = utils.create_job(name=name)
        self.assertIsNotNone(job)
        self.assertIsInstance(job, K8sJob)
        self.assertIsNotNone(job.model)
        self.assertIsInstance(job.model, Job)

    def test_struct_job(self):
        name = "yomama"
        job = utils.create_job(name=name)
        self.assertIsInstance(job.model, Job)
        self.assertIsInstance(job.model.metadata, ObjectMeta)
        self.assertIsInstance(job.model.spec, JobSpec)
        self.assertIsInstance(job.model.status, JobStatus)

    # --------------------------------------------------------------------------------- parallelism

    def test_parallelism_none_arg(self):
        p = None
        name = "job-{}".format(str(uuid.uuid4()))
        job = utils.create_job(name=name)
        with self.assertRaises(SyntaxError):
            job.parallelism = p

    def test_parallelism_invalid_arg(self):
        p = object()
        name = "job-{}".format(str(uuid.uuid4()))
        job = utils.create_job(name=name)
        with self.assertRaises(SyntaxError):
            job.parallelism = p

    def test_parallelism_negative_int(self):
        p = -5
        name = "job-{}".format(str(uuid.uuid4()))
        job = utils.create_job(name=name)
        with self.assertRaises(SyntaxError):
            job.parallelism = p

    def test_parallelism(self):
        p = 5
        name = "job-{}".format(str(uuid.uuid4()))
        job = utils.create_job(name=name)
        job.parallelism = p
        self.assertEqual(p, job.parallelism)

    # --------------------------------------------------------------------------------- completions

    def test_completions_none_arg(self):
        c = None
        name = "job-{}".format(str(uuid.uuid4()))
        job = utils.create_job(name=name)
        with self.assertRaises(SyntaxError):
            job.completions = c

    def test_completions_invalid_arg(self):
        c = object()
        name = "job-{}".format(str(uuid.uuid4()))
        job = utils.create_job(name=name)
        with self.assertRaises(SyntaxError):
            job.completions = c

    def test_completions_negative_int(self):
        c = -5
        name = "job-{}".format(str(uuid.uuid4()))
        job = utils.create_job(name=name)
        with self.assertRaises(SyntaxError):
            job.completions = c

    def test_completions(self):
        c = 5
        name = "job-{}".format(str(uuid.uuid4()))
        job = utils.create_job(name=name)
        job.completions = c
        self.assertEqual(c, job.completions)

    # --------------------------------------------------------------------------------- activeDeadlineSeconds

    def test_active_deadline_seconds_none_arg(self):
        s = None
        name = "job-{}".format(str(uuid.uuid4()))
        job = utils.create_job(name=name)
        with self.assertRaises(SyntaxError):
            job.active_deadline_seconds = s

    def test_active_deadline_seconds_invalid_arg(self):
        s = object()
        name = "job-{}".format(str(uuid.uuid4()))
        job = utils.create_job(name=name)
        with self.assertRaises(SyntaxError):
            job.active_deadline_seconds = s

    def test_active_deadline_seconds_negative_int(self):
        s = -5
        name = "job-{}".format(str(uuid.uuid4()))
        job = utils.create_job(name=name)
        with self.assertRaises(SyntaxError):
            job.active_deadline_seconds = s

    def test_active_deadline_seconds(self):
        s = 5
        name = "job-{}".format(str(uuid.uuid4()))
        job = utils.create_job(name=name)
        job.active_deadline_seconds = s
        self.assertEqual(s, job.active_deadline_seconds)

    # --------------------------------------------------------------------------------- restartPolicy

    def test_restart_policy_none_arg(self):
        p = None
        name = "job-{}".format(str(uuid.uuid4()))
        job = utils.create_job(name=name)
        with self.assertRaises(SyntaxError):
            job.restart_policy = p

    def test_restart_policy_invalid_arg(self):
        p = 'Always'
        name = "job-{}".format(str(uuid.uuid4()))
        job = utils.create_job(name=name)
        with self.assertRaises(SyntaxError):
            job.restart_policy = p

    def test_restart_policy(self):
        p = 'Never'
        name = "job-{}".format(str(uuid.uuid4()))
        job = utils.create_job(name=name)
        self.assertEqual('OnFailure', job.restart_policy)
        job.restart_policy = p
        self.assertEqual(p, job.restart_policy)

    # --------------------------------------------------------------------------------- api - create

    def test_api_create(self):
        name = "job-{}".format(uuid.uuid4())
        job = Job(utils.job())
        k8s_job = utils.create_job(name=name)
        k8s_job.model = job
        if utils.is_reachable(k8s_job.config):
            k8s_job.create()
            self.assertIsInstance(k8s_job, K8sJob)

    # --------------------------------------------------------------------------------- api - list

    def test_api_list(self):
        name = "job-{}".format(uuid.uuid4())
        job = Job(utils.job())
        k8s_job = utils.create_job(name=name)
        k8s_job.model = job
        if utils.is_reachable(k8s_job.config):
            k8s_job.create()
            _list = k8s_job.list()
            for x in _list:
                self.assertIsInstance(x, K8sJob)

    # --------------------------------------------------------------------------------- api - update

    def test_api_update(self):
        name = "job-{}".format(uuid.uuid4())
        job = Job(utils.job())
        k8s_job = utils.create_job(name=name)
        k8s_job.model = job
        k8s_job.completions = 30
        if utils.is_reachable(k8s_job.config):
            k8s_job.create()
            k8s_job.parallelism = 10
            k8s_job.update()
            self.assertEqual(k8s_job.parallelism, 10)

    # --------------------------------------------------------------------------------- api - scale

    def test_api_scale(self):
        name = "job-{}".format(uuid.uuid4())
        job = Job(utils.job())
        k8s_job = utils.create_job(name=name)
        k8s_job.model = job
        k8s_job.completions = 30
        if utils.is_reachable(k8s_job.config.api_host):
            k8s_job.create()
            k8s_job.scale(10)
            self.assertEqual(k8s_job.parallelism, 10)

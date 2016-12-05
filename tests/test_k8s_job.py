#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import unittest
import uuid

from kubernetes.K8sJob import K8sJob
from kubernetes.models.v1.Job import Job
from kubernetes.models.v1.JobSpec import JobSpec
from kubernetes.models.v1.ObjectMeta import ObjectMeta
from tests import utils


class K8sJobTests(unittest.TestCase):

    def setUp(self):
        utils.cleanup_jobs()

    def tearDown(self):
        utils.cleanup_jobs()

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
        self.assertIsNone(job.model.status)

    # --------------------------------------------------------------------------------- api - create

    def test_api_create(self):
        name = "job-{}".format(uuid.uuid4())
        job = Job(model=utils.job())
        k8s_job = utils.create_job(name=name)
        k8s_job.model = job
        if utils.is_reachable(k8s_job.config.api_host):
            k8s_job.create()
            self.assertIsInstance(k8s_job, K8sJob)
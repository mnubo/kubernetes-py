#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes.models.v1 import (
    BaseModel
)


class ReplicationControllerStatus(BaseModel):
    """
    http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_replicationcontrollerstatus
    """

    def __init__(self):
        super(ReplicationControllerStatus, self).__init__()
        self.replicas = 0
        self.fully_labeled_replicas = 0
        self.ready_replicas = 0
        self.observed_generation = 0

    # ------------------------------------------------------------------------------------- serialize

    def json(self):
        data = {}
        if self.replicas is not None:
            data['replicas'] = self.replicas
        if self.fully_labeled_replicas is not None:
            data['fullyLabeledReplicas'] = self.fully_labeled_replicas
        if self.ready_replicas is not None:
            data['readyReplicas'] = self.ready_replicas
        if self.observed_generation is not None:
            data['observedGeneration'] = self.observed_generation
        return data

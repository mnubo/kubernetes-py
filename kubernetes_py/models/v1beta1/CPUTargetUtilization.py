#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#


class CPUTargetUtilization(object):
    """
    https://kubernetes.io/docs/api-reference/extensions/v1beta1/definitions/#_v1beta1_cputargetutilization
    """

    def __init__(self, model=None):
        super(CPUTargetUtilization, self).__init__()

        self._target_percentage = 70

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'targetPercentage' in model:
            self.target_percentage = model['targetPercentage']

    # ------------------------------------------------------------------------------------- targetPercentage

    @property
    def target_percentage(self):
        return self._target_percentage
    
    @target_percentage.setter
    def target_percentage(self, t=None):
        if not isinstance(t, int):
            raise SyntaxError("CPUTargetUtilization: target_percentage: [ {} ] is invalid.".format(t))
        self._target_percentage = t

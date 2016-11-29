#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#


class RollbackConfig(object):
    """
    http://kubernetes.io/docs/api-reference/extensions/v1beta1/definitions/#_v1beta1_rollbackconfig
    """

    def __init__(self, model=None):
        super(RollbackConfig, self).__init__()

        self._revision = 0

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'revision' in model:
            self.revision = model['revision']

    # ------------------------------------------------------------------------------------- revision

    @property
    def revision(self):
        return self._revision

    @revision.setter
    def revision(self, rev=None):
        if not isinstance(rev, int):
            raise SyntaxError('RollbackConfig: revision: [ {} ] is invalid.'.format(rev))
        self._revision = rev

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.revision is not None:
            data['revision'] = self.revision
        return data

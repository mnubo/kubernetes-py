#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#


class NamespaceSpec(object):
    """
    https://kubernetes.io/docs/api-reference/v1/definitions/#_v1_namespacespec
    """

    def __init__(self, model=None):
        super(NamespaceSpec, self).__init__()

        self._finalizers = None

        if model is not None:
            self._build_with_model(model)

    def _build_with_model(self, model=None):
        if 'finalizers' in model:
            self.finalizers = model['finalizers']

    # --------------------------------------------------------------------------------- finalizers

    @property
    def finalizers(self):
        return self._finalizers

    @finalizers.setter
    def finalizers(self, f=None):
        if not isinstance(f, list):
            raise SyntaxError('NamespaceSpec: finalizers: [ {} ] is invalid. Must be a list of strings.'.format(f))
        self._finalizers = f

    # --------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = {}
        if self.finalizers is not None:
            data['finalizers'] = self.finalizers
        return data

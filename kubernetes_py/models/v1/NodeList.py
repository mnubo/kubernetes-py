#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

from kubernetes_py.models.unversioned.ListMeta import ListMeta
from kubernetes_py.models.unversioned.ListModel import ListModel
from kubernetes_py.models.v1.Node import Node
from kubernetes_py.utils import filter_model, is_valid_list


class NodeList(ListModel):
    """
    https://kubernetes.io/docs/api-reference/v1/definitions/#_v1_nodelist
    """

    def __init__(self, model=None):
        super(NodeList, self).__init__()

        self.kind = "NodeList"
        self.api_version = "v1"

        if model is not None:
            m = filter_model(model)
            self._build_with_model(m)

    def _build_with_model(self, model=None):
        if "kind" in model:
            self.kind = model["kind"]
        if "apiVersion" in model:
            self.api_version = model["apiVersion"]
        if "metadata" in model:
            self.metadata = ListMeta(model["metadata"])
        if "items" in model:
            if isinstance(model["items"], list):
                l = list()
                for i in model["items"]:
                    l.append(Node(model=i))
                self.items = l
            else:
                raise SyntaxError("NodeList: items: [ {0} ] is invalid.".format(model["items"]))

    # ------------------------------------------------------------------------------------- items

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, i=None):
        if not is_valid_list(target=i, element_class=Node):
            raise SyntaxError("NodeList: items: [ {0} ] is invalid.".format(i))
        self._items = i

    # ------------------------------------------------------------------------------------- serialize

    def serialize(self):
        data = super(NodeList, self).serialize()
        return data

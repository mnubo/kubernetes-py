#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import copy
import socket
import importlib

from kubernetes.K8sExceptions import NotFoundException


def is_valid_string(target=None):
    if target is None:
        return False
    if not isinstance(target, str):
        return False
    return True


def is_valid_list(target=None, element_class=None):
    if target is None:
        return False
    if not isinstance(target, list):
        return False
    if element_class is not None:
        for x in target:
            if not isinstance(x, element_class):
                return False
    return True


def is_valid_dict(target=None, keys=None, type=None):
    if target is None:
        return False
    if not isinstance(target, dict):
        return False
    for k, v in target.items():
        if not isinstance(k, str):
            return False
        if type is not None and not isinstance(v, type):
            return False
    if keys is not None and isinstance(keys, list):
        for x in target:
            if x not in keys:
                return False
    return True


def is_reachable(ip=None):
    if not is_valid_string(ip):
        return False
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False


def filter_model(model=None):
    mutable = copy.deepcopy(model)
    for key in model:
        if model[key] is None:
            mutable.pop(key)
    return mutable


def str_to_class(obj_type=None):
    import_paths = [
        "kubernetes.models.unversioned.{}".format(obj_type),
        "kubernetes.models.v1.{}".format(obj_type),
        "kubernetes.models.v1alpha1.{}".format(obj_type),
        "kubernetes.models.v1beta1.{}".format(obj_type),
        "kubernetes.models.v2alpha1.{}".format(obj_type),
    ]

    module = None
    for path in import_paths:
        try:
            module = importlib.import_module(path)
            break
        except ImportError:
            pass

    if module is not None:
        _class = getattr(module, obj_type)()
        return _class

    raise NotFoundException("Could not import obj_type: [ {} ]".format(obj_type))
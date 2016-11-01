#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#


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


def is_valid_dict(target=None, keys=None):
    if target is None:
        return False
    if not isinstance(target, dict):
        return False
    if keys is not None and isinstance(keys, list):
        for x in target:
            for y in keys:
                if y not in x:
                    return False
    return True

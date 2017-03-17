#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

import collections
from six import string_types


def convert(data):
    if isinstance(data, string_types):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.items()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data

#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#


class InvalidObjectException(Exception):
    def __init__(self, *args, **kwargs):
        super(InvalidObjectException, self).__init__(*args, **kwargs)


class UnauthorizedException(Exception):
    def __init__(self, *args, **kwargs):
        super(UnauthorizedException, self).__init__(*args, **kwargs)


class NotFoundException(Exception):
    def __init__(self, *args, **kwargs):
        super(NotFoundException, self).__init__(*args, **kwargs)


class UnprocessableEntityException(Exception):
    def __init__(self, *args, **kwargs):
        super(UnprocessableEntityException, self).__init__(*args, **kwargs)


class BadRequestException(Exception):
    def __init__(self, *args, **kwargs):
        super(BadRequestException, self).__init__(*args, **kwargs)


class AlreadyExistsException(Exception):
    def __init__(self, *args, **kwargs):
        super(AlreadyExistsException, self).__init__(*args, **kwargs)


class TimedOutException(Exception):
    def __init__(self, *args, **kwargs):
        super(TimedOutException, self).__init__(*args, **kwargs)


class PodNotReadyException(Exception):
    def __init__(self, *args, **kwargs):
        super(PodNotReadyException, self).__init__(*args, **kwargs)


class VersionMismatchException(Exception):
    def __init__(self, *args, **kwargs):
        super(VersionMismatchException, self).__init__(*args, **kwargs)


class DrainNodeException(Exception):
    def __init__(self, *args, **kwargs):
        super(DrainNodeException, self).__init__(*args, **kwargs)


class CronJobAlreadyRunningException(Exception):
    def __init__(self, *args, **kwargs):
        super(CronJobAlreadyRunningException, self).__init__(*args, **kwargs)


class CronJobRunException(Exception):
    def __init__(self, *args, **kwargs):
        super(CronJobRunException, self).__init__(*args, **kwargs)


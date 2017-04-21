#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#
import base64
import json
import os
import tempfile
import requests
from kubernetes.utils.ConvertData import convert
from six.moves.urllib.parse import urlencode


class HttpRequest:
    def __init__(self, method='GET', host='localhost:80', url='/', data=None, auth=None,
                 cert=None, ca_cert=None, ca_cert_data=None, token=None):

        self.http_method = method
        self.http_host = host
        self.url = url
        self.data = data
        self.auth = auth
        self.cert = cert
        self.ca_cert = ca_cert
        self.ca_cert_data = ca_cert_data
        self.token = token

    def send(self):
        state = dict(success=False, reason=None, status=None, data=None)
        http_headers = dict()
        http_headers['Accept'] = 'application/json'

        if self.http_method in ['PUT', 'POST', 'PATCH']:
            http_headers['Content-type'] = 'application/json'

        if self.token is not None:
            http_headers['Authorization'] = 'Bearer {token}'.format(token=self.token)

        if self.data is not None and self.http_method in ['GET']:
            url = "{0}?{1}".format(self.url, urlencode(self.data))
            self.url = url

        self.url = self.http_host + self.url

        temp = None
        verify = False
        if self.ca_cert is not None:
            verify = self.ca_cert
        if self.ca_cert_data is not None:
            temp = tempfile.NamedTemporaryFile(delete=False)
            data = base64.b64decode(self.ca_cert_data)
            temp.write(data)
            temp.close()
            verify = temp.name

        try:

            response = requests.request(
                method=self.http_method,
                url=self.url,
                auth=self.auth,
                cert=self.cert,
                headers=http_headers,
                data="" if self.data is None else json.dumps(self.data),
                verify=verify
            )

        except Exception as err:
            raise err

        finally:
            if temp is not None:
                os.unlink(temp.name)

        state['status'] = response.status_code
        state['reason'] = response.reason
        resp_data = response.content.decode()

        if len(resp_data) > 0:
            try:
                state['data'] = convert(data=json.loads(resp_data))
            except ValueError:
                state['data'] = resp_data.strip()

        if state['status'] in [200, 201]:
            state['success'] = True

        return state

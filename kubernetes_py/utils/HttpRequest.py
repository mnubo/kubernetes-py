#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#
import re
import base64
import json
import os
import tempfile
import requests
import urllib3
from kubernetes_py.utils.ConvertData import convert
from six.moves.urllib.parse import urlencode

RE_VALID_SSL_IP = re.compile(
    r"^https://(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])"
)


class HttpRequest:
    def __init__(
        self,
        method="GET",
        host="localhost:80",
        url="/",
        data=None,
        auth=None,
        cert=None,
        cert_data=None,
        ca_cert=None,
        ca_cert_data=None,
        token=None,
    ):

        self.http_method = method
        self.http_host = host
        self.url = url
        self.data = data
        self.auth = auth
        self.cert = cert
        self.cert_data = cert_data
        self.ca_cert = ca_cert
        self.ca_cert_data = ca_cert_data
        self.token = token

    def send(self):
        state = dict(success=False, reason=None, status=None, data=None)
        http_headers = dict()
        http_headers["Accept"] = "application/json"

        if self.http_method in ["PUT", "POST", "PATCH"]:
            http_headers["Content-type"] = "application/json"

        if self.token is not None:
            http_headers["Authorization"] = "Bearer {token}".format(token=self.token)

        if self.data is not None and self.http_method in ["GET"]:
            url = "{0}?{1}".format(self.url, urlencode(self.data))
            self.url = url

        self.url = self.http_host + self.url

        temp = None
        this_cert_file = None
        this_key_file = None
        verify = False
        if self.ca_cert is not None:
            verify = self.ca_cert
        if self.ca_cert_data is not None:
            temp = tempfile.NamedTemporaryFile(delete=False)
            data = base64.b64decode(self.ca_cert_data)
            temp.write(data)
            temp.close()
            verify = temp.name
        if self.cert_data is not None:
            (this_cert_data, this_key_data) = self.cert_data
            this_cert_file = tempfile.NamedTemporaryFile(delete=False)
            decoded_cert = base64.b64decode(this_cert_data)
            this_cert_file.write(decoded_cert)
            this_cert_file.close()
            this_key_file = tempfile.NamedTemporaryFile(delete=False)
            decoded_key = base64.b64decode(this_key_data)
            this_key_file.write(decoded_key)
            this_key_file.close()
            self.cert = (this_cert_file.name, this_key_file.name)

        # TODO: TLS issue with Python 2.7 and urllib3 when hostname is an IP address
        # A better fix should be found but I can't think of anything else for now.
        search_result = RE_VALID_SSL_IP.search(self.http_host)
        if search_result:
            verify = False
            urllib3.disable_warnings()

        try:

            response = requests.request(
                method=self.http_method,
                url=self.url,
                auth=self.auth,
                cert=self.cert,
                headers=http_headers,
                data="" if self.data is None else json.dumps(self.data),
                verify=verify,
            )

        except Exception as err:
            raise err

        finally:
            if temp is not None:
                os.unlink(temp.name)
            if this_cert_file is not None:
                os.unlink(this_cert_file.name)
            if this_key_file is not None:
                os.unlink(this_key_file.name)

        state["status"] = response.status_code
        state["reason"] = response.reason

        # There was an issue with "kubectl logs" type requests where returned content is "text/plain" and
        # we do have characters of unknown origin.
        try:
            resp_data = response.content.decode("utf-8")
        except UnicodeDecodeError:
            resp_data = response.content

        if len(resp_data) > 0:
            try:
                state["data"] = convert(data=json.loads(resp_data))
            except Exception:
                state["data"] = resp_data

        if 200 <= state["status"] <= 299:
            state["success"] = True

        return state

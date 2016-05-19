import httplib
import urllib
import json
import base64
import requests
from kubernetes.utils.ConvertData import convert


class HttpRequest:
    def __init__(self, method='GET', host='localhost:80', url='/', data=None, auth=None, token=None):
        self.http_method = method
        self.http_host = host
        self.url = url
        self.data = data
        self.auth = auth
        self.token = token

    def send(self):
        state = dict(success=False, reason=None, status=None, data=None)
        http_headers = dict()
        http_headers['Accept'] = 'application/json'
        if self.http_method in ['PUT', 'POST']:
            http_headers['Content-type'] = 'application/json'
        if self.token is not None:
            http_headers['Authorization'] = 'Bearer {token}'.format(token=self.token)

        if self.data is not None and self.http_method in ['GET']:
            url = "{orig_url}?{encoded_params}".format(orig_url=self.url, encoded_params=urllib.urlencode(self.data))
            self.url = url
        self.url = self.http_host + self.url

        if self.data is None:
            response = requests.request(method=self.http_method, url=self.url, auth=self.auth, verify=False)
        else:
            json_encoded = json.dumps(self.data)
            # @todo: Add certificate verification !
            response = requests.request(method=self.http_method, url=self.url, auth=self.auth, headers=http_headers, body=json_encoded, verify=False)

        state['status'] = response.status_code
        state['reason'] = response.reason
        resp_data = response.text.decode('utf-8')

        if len(resp_data) > 0:
            state['data'] = convert(data=json.loads(resp_data))

        if state['status'] in [200, 201]:
            state['success'] = True

        return state

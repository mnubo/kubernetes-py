import httplib
import urllib
import json
from kubernetes.utils.ConvertData import convert

class HttpRequest:
    def __init__(self, method='GET', host='localhost:80', url='/', data=None):
        self.http_method = method
        self.http_host = host
        self.url = url
        self.data = data

    def send(self):
        state = dict(success=False, reason=None, status=None, data=None)
        http_headers = dict()
        http_headers['Accept'] = 'application/json'
        if self.http_method in ['PUT', 'POST']:
            http_headers['Content-type'] = 'application/json'

        conn = httplib.HTTPConnection(self.http_host)

        if self.data is not None and self.http_method in ['GET']:
            url = "{orig_url}?{encoded_params}".format(orig_url=self.url, encoded_params=urllib.urlencode(self.data))
            self.url = url

        if self.data is None:
            conn.request(method=self.http_method, url=self.url)
        else:
            json_encoded = json.dumps(self.data)
            conn.request(method=self.http_method, url=self.url, headers=http_headers, body=json_encoded)

        response = conn.getresponse()
        state['status'] = response.status
        state['reason'] = response.reason

        if state['status'] in [200, 201]:
            resp_data = response.read().decode('utf-8')
            if len(resp_data) > 0:
                state['data'] = convert(data=json.loads(resp_data))
            state['success'] = True
        else:
            state['data'] = response.read().decode('utf-8')

        conn.close()

        return state

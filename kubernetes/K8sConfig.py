import re

DEFAULT_API_HOST = "localhost:8888"
DEFAULT_API_VERSION = "v1"
DEFAULT_NAMESPACE = "default"

VALID_API_VERSIONS = ["v1"]


class K8sConfig:
    def __init__(self, api_host=DEFAULT_API_HOST, version=DEFAULT_API_VERSION,
                 namespace=DEFAULT_NAMESPACE, pull_secret=None, auth=None, token=None):

        if not isinstance(api_host, str) or not isinstance(version, str):
            raise SyntaxError('Please make sure api_host and version are strings.')

        if version not in VALID_API_VERSIONS:
            valid = ", ".join(VALID_API_VERSIONS)
            raise SyntaxError('Please provide a valid version in: {0}'.format(valid))

        if not isinstance(namespace, str):
            raise SyntaxError('Please make sure namespace is a string.')

        if auth is not None and not isinstance(auth, tuple):
            raise SyntaxError('Please make sure auth is a tuple.')

        if token is not None and not isinstance(token, str):
            raise SyntaxError('Please make sure token is a string.')

        http_https_re = re.compile(r"^http[s]*")
        if not http_https_re.search(api_host):
            api_host = "http://{host}".format(host=api_host)

        valid_url_re = re.compile("(https?\:\/\/)([a-z0-9-.]*)(\:)([0-9]{2,5})")
        if not valid_url_re.match(api_host):
            raise SyntaxError('Please make sure the API host is valid: {0}'.format(api_host))

        self.api_host = api_host
        self.version = version
        self.namespace = namespace
        self.pull_secret = pull_secret
        self.auth = auth
        self.token = token

    def get_api_host(self):
        return self.api_host

    def get_namespace(self):
        return self.namespace

    def get_pull_secret(self):
        return self.pull_secret

    def get_auth(self):
        return self.auth

    def get_token(self):
        return self.token

    def get_version(self):
        return self.version

    def set_api_host(self, api_host=None):
        self.api_host = api_host
        return self

    def set_namespace(self, namespace='default'):
        self.namespace = namespace
        return self

    def set_pull_secret(self, pull_secret):
        assert isinstance(pull_secret, str)
        self.pull_secret = pull_secret
        return self

    def set_auth(self, auth):
        assert isinstance(auth, tuple)
        self.auth = auth
        return self

    def set_token(self, token):
        assert isinstance(token, str)
        self.token = token
        return self

    def set_version(self, version=None):
        self.version = version
        return self

class K8sConfig:
    def __init__(self, api_host='localhost:8888', version='v1', namespace='default', pull_secret=None, auth=None, token=None):
        valid_versions = ['v1']
        if not isinstance(api_host, str) or not isinstance(version, str):
            raise SyntaxError('Please make sure api_host and version are strings.')
        if version not in valid_versions:
            raise SyntaxError('Please provide a valid version in: {str}'.format(str=', '.join(valid_versions)))
        if not isinstance(namespace, str):
            raise SyntaxError('Please make sure namespace is a string.')
        if not isinstance(auth, tuple):
            raise SyntaxError('Please make sure auth is a tuple.')
        if not isinstance(namespace, str):
            raise SyntaxError('Please make sure token is a string.')
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

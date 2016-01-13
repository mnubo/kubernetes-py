class BaseUrls:
    def __init__(self, namespace='default'):
        self.version = 'v1'
        self.namespace = namespace
        self.urls = dict()
        self.urls['Pod'] = '/api/{version}/namespaces/{namespace}/pods'\
            .format(version=self.version, namespace=self.namespace)
        self.urls['ReplicationController'] = '/api/{version}/namespaces/{namespace}/replicationcontrollers'\
            .format(version=self.version, namespace=self.namespace)
        self.urls['Service'] = '/api/{version}/namespaces/{namespace}/services'\
            .format(version=self.version, namespace=self.namespace)
        self.urls['Secret'] = '/api/{version}/namespaces/{namespace}/secrets'\
            .format(version=self.version, namespace=self.namespace)

    def get_base_url(self, object_type=None):
        if object_type is None or not isinstance(object_type, str) or object_type not in self.urls.keys():
            raise SyntaxError('Please get an object_type as a string in the following list: {obj_types}'
                              .format(obj_types=', '.join(self.urls.keys())))
        return self.urls[object_type]

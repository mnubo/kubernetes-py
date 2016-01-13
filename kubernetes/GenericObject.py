from k8s.utils import HttpRequest
from k8s.utils import K8sConfig
import importlib


class GenericObject:
    def __init__(self, config=None, obj_type=None, name=None):
        valid_objects = ['Pod', 'ReplicationController', 'Secret', 'Service']
        if config is None or obj_type is None or not isinstance(config, K8sConfig) or not isinstance(obj_type, str):
            raise SyntaxError('Please define config as a K8sConfig object and obj_type as a string.')
        if obj_type not in valid_objects:
            raise SyntaxError('Please make sure object type is in: {my_type}'.format(my_type=', '.join(valid_objects)))
        self.config = config
        self.name = name
        try:
            i = importlib.import_module('models.{version}.BaseUrls'.format(version=self.config.get_version()))
            self.base_url = i(namespace=self.config.get_namespace()).get_base_url(obj_type)
        except:
            raise

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def list(self):
        state = HttpRequest(method='GET', host=self.config.get_api_host(), url=self.base_url).send()
        return state.data

    def get(self):
        this_url = '{base}/{name}'.format(base=self.base_url, name=self.name)
        state = HttpRequest(method='GET', host=self.config.get_api_host(), url=this_url).send()
        return state.data

    def create(self, model):
        this_url = '{base}/{name}'.format(base=self.base_url, name=self.name)
        state = HttpRequest(method='POST', host=self.config.get_api_host(), url=this_url, data=model).send()
        return state.data

    def update(self, model):
        this_url = '{base}/{name}'.format(base=self.base_url, name=self.name)
        state = HttpRequest(method='PUT', host=self.config.get_api_host(), url=this_url, data=model).send()
        return state.data

    def delete(self, model):
        this_url = '{base}/{name}'.format(base=self.base_url, name=self.name)
        state = HttpRequest(method='DELETE', host=self.config.get_api_host(), url=this_url, data=model).send()
        return state.data

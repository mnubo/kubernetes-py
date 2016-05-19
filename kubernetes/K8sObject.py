from kubernetes.utils import HttpRequest
from kubernetes.models.v1.BaseUrls import BaseUrls
from kubernetes.models.v1.BaseModel import BaseModel
from kubernetes.models.v1.DeleteOptions import DeleteOptions
from kubernetes.K8sConfig import K8sConfig
from kubernetes.exceptions.NotFoundException import NotFoundException
from kubernetes.exceptions.UnprocessableEntityException import UnprocessableEntityException
import json


class K8sObject(object):
    def __init__(self, config=None, obj_type=None, name=None):
        valid_objects = ['Pod', 'ReplicationController', 'Secret', 'Service']
        if config is None:
            self.config = K8sConfig()
        else:
            try:
                assert isinstance(config, K8sConfig)
                self.config = config
            except:
                raise SyntaxError('Please define config as a K8sConfig object.')
        if obj_type is None or not isinstance(obj_type, str):
            raise SyntaxError('Please define obj_type as a string.')
        if obj_type not in valid_objects:
            raise SyntaxError('Please make sure object type is in: {my_type}'.format(my_type=', '.join(valid_objects)))
        else:
            self.obj_type = obj_type

        self.name = name

        self.model = BaseModel()
        assert isinstance(self.model, BaseModel)

        try:
            self.base_url = BaseUrls(namespace=self.config.get_namespace()).get_base_url(object_type=obj_type)
        except:
            raise Exception('Cannot import version specific classes')

    def __str__(self):
        return "Kubernetes {obj_type} named {name}. Definition: {model}"\
            .format(obj_type=self.obj_type, name=self.name, model=self.model.get())

    def as_dict(self):
        return self.model.get()

    def as_json(self):
        return json.dumps(self.model.get())

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name
        if self.model is not None:
            my_method = getattr(self.model, "set_name", None)
            if callable(my_method):
                my_method(name=name)
        return self

    def request(self, method='GET', host=None, url=None, auth=None, data=None, token=None):
        # default parameters
        host = self.config.get_api_host() if host is None else host
        url = self.base_url if url is None else url
        auth = self.config.auth if auth is None else auth
        token = self.config.token if token is None else token

        return HttpRequest(host=host, url=url, auth=auth, data=data, token=token).send()

    def list(self):
        state = self.request(method='GET')
        if not state.get('status'):
            raise Exception('Could not fetch list of objects of type: {this_type}.'.format(this_type=self.obj_type))
        return state.get('data', dict()).get('items', list())

    def get_model(self):
        if self.name is None:
            raise Exception('Cannot fetch object without name set first.')
        this_url = '{base}/{name}'.format(base=self.base_url, name=self.name)
        state = self.request(method='GET', url=this_url)
        if state.get('success'):
            model = state.get('data')
        else:
            message = 'Failed to fetch object definition for {resource_type} {name}. HTTP-{code}'\
                .format(name=self.name, resource_type=self.obj_type, code=state.get('status', ''))
            raise NotFoundException(message)
        return model

    def get_with_params(self, data):
        if not isinstance(data, dict):
            raise SyntaxError('data must be a dict of parameters to be encoded in the URL.')
        this_url = '{base}'.format(base=self.base_url)
        state = self.request(method='GET', url=this_url, data=data)
        return state.get('data', None).get('items', list())

    def create(self):
        if self.name is None:
            raise Exception('Cannot create object without name set first.')
        this_url = '{base}'.format(base=self.base_url)
        state = self.request(method='POST', url=this_url, data=self.model.get())
        if not state.get('success'):
            message = 'Failed to create object: HTTP-{code} {http_data}'\
                .format(code=state.get('status', ''), http_data=state.get('data', dict()).get('message', None))
            if int(state.get('status', 0)) == 422:
                raise UnprocessableEntityException(message)
            else:
                raise Exception(message)
        return self

    def update(self):
        if self.name is None:
            raise Exception('Cannot create object without name set first.')
        this_url = '{base}/{name}'.format(base=self.base_url, name=self.name)
        state = self.request(method='PUT', url=this_url, data=self.model.get())
        if not state.get('success'):
            message = 'Failed to update object: {http_data}'\
                .format(http_data=state.get('data', dict()).get('message', None))
            raise Exception(message)
        return self

    def delete(self):
        if self.name is None:
            raise Exception('Cannot create object without name set first.')
        this_url = '{base}/{name}'.format(base=self.base_url, name=self.name)
        self.model = DeleteOptions(kind='DeleteOptions')
        state = self.request(method='DELETE', url=this_url, data=self.model.get())
        if not state.get('success'):
            message = 'Failed to delete object: {http_data}'\
                .format(http_data=state.get('data', dict()).get('message', None))
            raise Exception(message)
        return self

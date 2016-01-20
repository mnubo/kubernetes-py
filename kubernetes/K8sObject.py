from kubernetes.utils import HttpRequest
from kubernetes.models.v1.BaseUrls import BaseUrls
from kubernetes.models.v1.BaseModel import BaseModel
from kubernetes.models.v1.DeleteOptions import DeleteOptions
from kubernetes.K8sConfig import K8sConfig
from kubernetes.exceptions.NotFoundException import NotFoundException


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

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name
        if self.model is not None:
            my_method = getattr(self.model, "set_name", None)
            if callable(my_method):
                my_method(name=name)
        return self

    def list(self):
        state = HttpRequest(method='GET', host=self.config.get_api_host(), url=self.base_url).send()
        if not state.get('status'):
            raise Exception('Could not fetch list of objects of type: {this_type}.'.format(this_type=self.obj_type))
        return state.data

    def get_model(self):
        if self.name is None:
            raise Exception('Cannot fetch object without name set first.')
        this_url = '{base}/{name}'.format(base=self.base_url, name=self.name)
        state = HttpRequest(method='GET', host=self.config.get_api_host(), url=this_url).send()
        if state.get('success'):
            model = state.get('data')
        else:
            raise NotFoundException('Failed to fetch object definition for {resource_type} {name}.'
                                    .format(name=self.name, resource_type=self.obj_type))
        return model

    def create(self):
        if self.name is None:
            raise Exception('Cannot create object without name set first.')
        this_url = '{base}'.format(base=self.base_url)
        state = HttpRequest(method='POST', host=self.config.get_api_host(), url=this_url, data=self.model.get()).send()
        if not state.get('success'):
            raise Exception('Failed to create object.')
        return self

    def update(self):
        if self.name is None:
            raise Exception('Cannot create object without name set first.')
        this_url = '{base}/{name}'.format(base=self.base_url, name=self.name)
        state = HttpRequest(method='PUT', host=self.config.get_api_host(), url=this_url, data=self.model.get()).send()
        if not state.get('success'):
            raise Exception('Failed to update object.')
        return self

    def delete(self):
        if self.name is None:
            raise Exception('Cannot create object without name set first.')
        this_url = '{base}/{name}'.format(base=self.base_url, name=self.name)
        self.model = DeleteOptions(kind='DeleteOptions')
        state = HttpRequest(method='DELETE', host=self.config.get_api_host(),
                            url=this_url, data=self.model.get()).send()
        if not state.get('success'):
            raise Exception('Failed to delete object.')
        return self

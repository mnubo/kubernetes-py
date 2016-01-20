from kubernetes.models.v1.PodBasedModel import PodBasedModel
from kubernetes.models.v1.PodSpec import PodSpec
from kubernetes.models.v1.ObjectMeta import ObjectMeta


class ReplicationController(PodBasedModel):
    def __init__(self, name=None, image=None, namespace='default', replicas=1, model=None):
        PodBasedModel.__init__(self)
        if model is not None:
            assert isinstance(model, dict)
            self.model = model
            if 'metadata' in self.model.keys():
                self.rc_metadata = ObjectMeta(model=self.model['metadata'])
            if 'template' in self.model['spec'].keys():
                self.pod_spec = PodSpec(model=self.model['spec']['template']['spec'])
                self.pod_metadata = ObjectMeta(model=self.model['spec']['template']['metadata'])
        else:
            if name is None or not isinstance(name, str):
                raise SyntaxError('ReplicationController: name should be a string.')
            self.model = dict(kind='ReplicationController', apiVersion='v1')
            self.rc_metadata = ObjectMeta(name=name, namespace=namespace)

            self.model['spec'] = {
                "replicas": replicas,
                "selector": dict(name=name)
            }

            if image is not None:
                self.model['spec']['template'] = dict()
                self.pod_spec = PodSpec(name=name, image=image)
                self.pod_metadata = ObjectMeta(name=name, namespace=namespace)

            self._update_model()

    def _update_model(self):
        self.model['metadata'] = self.rc_metadata.get()
        if self.pod_metadata is not None:
            if 'template' not in self.model['spec'].keys():
                self.model['spec']['template'] = dict()
            self.model['spec']['template']['metadata'] = self.pod_metadata.get()
        if self.pod_spec is not None:
            if 'template' not in self.model['spec'].keys():
                self.model['spec']['template'] = dict()
            self.model['spec']['template']['spec'] = self.pod_spec.get()
        return self

    def add_label(self, k=None, v=None):
        assert isinstance(k, str)
        assert isinstance(v, str)
        self.rc_metadata.add_label(k=k, v=v)
        self._update_model()
        return self

    def set_name(self, name):
        assert isinstance(name, str)
        self.rc_metadata.set_name(name=name)
        self._update_model()
        return self

    def set_namespace(self, name):
        assert isinstance(name, str)
        self.rc_metadata.set_namespace(name=name)
        self.pod_metadata.set_namespace(name=name)
        self._update_model()
        return self

    def set_replicas(self, replicas=None):
        if replicas is None or not isinstance(replicas, int):
            raise SyntaxError('ReplicationController: replicas should be a positive integer value')
        self.model['spec']['replicas'] = replicas
        return self

    def set_selector(self, selector=None):
        if selector is None or not isinstance(selector, dict):
            raise SyntaxError('ReplicationController: Selector should be a dict of key, value pairs.')
        self.model['spec']['selector'] = selector
        return self

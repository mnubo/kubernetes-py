from kubernetes.K8sPodBasedObject import K8sPodBasedObject
from kubernetes.models.v1.Pod import Pod


class K8sPod(K8sPodBasedObject):
    def __init__(self, config=None, name=None):
        K8sPodBasedObject.__init__(self, config=config, obj_type='Pod', name=name)
        self.model = Pod(name=name, namespace=self.config.get_namespace())

    def add_label(self, k, v):
        self.model.add_pod_label(k=k, v=v)
        return self

    def get(self):
        self.model = Pod(model=self.get_model())
        return self

    def set_namespace(self, name):
        self.model.set_pod_namespace(name=name)
        return self

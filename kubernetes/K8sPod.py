from kubernetes.K8sPodBasedObject import K8sPodBasedObject
from kubernetes.models.v1.Pod import Pod


class K8sPod(K8sPodBasedObject):
    def __init__(self, config=None, name=None):
        K8sPodBasedObject.__init__(self, config=config, obj_type='Pod', name=name)
        self.model = Pod(name=name, namespace=self.config.get_namespace())
        if self.config.get_pull_secret() is not None:
            self.model.add_image_pull_secrets(name=self.config.get_pull_secret())

    def add_annotation(self, k, v):
        self.model.add_pod_annotation(k=k, v=v)
        return self

    def add_label(self, k, v):
        self.model.add_pod_label(k=k, v=v)
        return self

    def del_annotation(self, k):
        self.model.del_pod_annotation(k=k)
        return self

    def del_label(self, k):
        self.model.del_pod_label(k=k)
        return self

    def get(self):
        self.model = Pod(model=self.get_model())
        return self

    def get_annotation(self, k):
        return self.model.get_pod_annotation(k=k)

    def get_annotations(self):
        return self.model.get_pod_annotations()

    def get_label(self, k):
        return self.model.get_pod_label(k=k)

    def get_labels(self):
        return self.model.get_pod_labels()

    def set_annotations(self, new_dict):
        self.model.set_pod_annotations(new_dict=new_dict)
        return self

    def set_labels(self, new_dict):
        self.model.set_pod_labels(new_dict=new_dict)
        return self

    def set_namespace(self, name):
        self.model.set_pod_namespace(name=name)
        return self

from kubernetes.K8sPodBasedObject import K8sPodBasedObject
from kubernetes.K8sContainer import K8sContainer
from kubernetes.models.v1.ReplicationController import ReplicationController
import uuid

class K8sReplicationController(K8sPodBasedObject):

    def __init__(self, config=None, name=None, image=None, replicas=0):
        K8sPodBasedObject.__init__(self, config=config, obj_type='ReplicationController', name=name)
        self.model = ReplicationController(name=name, namespace=self.config.get_namespace())
        self.set_replicas(replicas)
        self.set_selector(selector=dict(name=name))
        if image is not None:
            self.model.add_container(K8sContainer(name=name, image=image).get_model())
            self.model.set_pod_name(name=name)
            my_version = str(uuid.uuid4())
            self.model.add_pod_label(k='rc_version', v=my_version)
            self.set_selector(selector=dict(name=name, rc_version=my_version))

    def add_label(self, k, v):
        self.model.add_label(k=k, v=v)
        return self

    def get(self):
        self.model = ReplicationController(model=self.get_model())
        return self

    def set_namespace(self, name):
        self.model.set_namespace(name=name)
        return self

    def set_replicas(self, replicas):
        self.model.set_replicas(replicas=replicas)
        return self

    def set_selector(self, selector):
        self.model.set_selector(selector=selector)
        return self

    @staticmethod
    def resize(config, name, replicas):
        try:
            this_rc = K8sReplicationController(config=config, name=name).get()
            this_rc.set_replicas(replicas)
            this_rc.update()
        except:
            raise
        return this_rc

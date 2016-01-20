from kubernetes.models.v1.BaseModel import BaseModel
from kubernetes.models.v1.ObjectMeta import ObjectMeta
from kubernetes.models.v1.PodSpec import PodSpec
from kubernetes.models.v1.Container import Container


class PodBasedModel(BaseModel):
    def __init__(self):
        BaseModel.__init__(self)
        self.pod_spec = PodSpec()
        self.pod_metadata = ObjectMeta()

    def _update_model(self):
        self.model['metadata'] = self.pod_metadata.get()
        self.model['spec'] = self.pod_spec.get()
        return self

    def add_container(self, container):
        try:
            assert isinstance(container, Container)
            self.pod_spec.add_container(container=container)
            self._update_model()
        except:
            raise
        return self

    def add_host_volume(self, name, path):
        try:
            self.pod_spec.add_host_volume(name=name, path=path)
            self._update_model()
        except:
            raise
        return self

    def add_pod_label(self, k=None, v=None):
        try:
            assert isinstance(k, str)
            assert isinstance(v, str)
            self.pod_metadata.add_label(k=k, v=v)
            self._update_model()
        except:
            raise
        return self

    def set_active_deadline(self, seconds):
        try:
            self.pod_spec.set_active_deadline(seconds)
            self._update_model()
        except:
            raise
        return self

    def set_dns_policy(self, policy):
        try:
            self.pod_spec.set_dns_policy(policy=policy)
            self._update_model()
        except:
            raise
        return self

    def set_image_pull_secrets(self, name):
        try:
            self.pod_spec.set_image_pull_secrets(name=name)
            self._update_model()
        except:
            raise
        return self

    def set_pod_name(self, name=None):
        assert isinstance(name, str)
        try:
            self.pod_metadata.set_name(name=name)
            self._update_model()
        except:
            raise
        return self

    def set_pod_namespace(self, name=None):
        try:
            assert isinstance(name, str)
            self.pod_metadata.set_namespace(name=name)
            self._update_model()
        except:
            raise
        return self

    def set_restart_policy(self, policy):
        try:
            self.pod_spec.set_restart_policy(policy=policy)
            self._update_model()
        except:
            raise
        return self

    def set_service_account(self, name):
        try:
            self.pod_spec.set_service_account(name=name)
            self._update_model()
        except:
            raise
        return self

    def set_termination_grace_period(self, seconds=None):
        try:
            self.pod_spec.set_termination_grace_period(seconds=seconds)
            self._update_model()
        except:
            raise
        return self

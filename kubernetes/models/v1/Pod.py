from kubernetes.models.v1.ObjectMeta import ObjectMeta
from kubernetes.models.v1.PodBasedModel import PodBasedModel
from kubernetes.models.v1.PodSpec import PodSpec
from kubernetes.models.v1.PodStatus import PodStatus


class Pod(PodBasedModel):
    def __init__(self, name=None, image=None, namespace='default', model=None):
        PodBasedModel.__init__(self)
        if model is not None:
            self.model = model
            if 'status' in self.model.keys():
                self.pod_status = PodStatus(model=self.model['status'])
            self.pod_spec = PodSpec(model=self.model['spec'])
            self.pod_metadata = ObjectMeta(model=self.model['metadata'])
        else:
            if name is None or not isinstance(name, str):
                raise SyntaxError('name should be a string.')
            self.model = dict(kind='Pod', apiVersion='v1')
            if name is not None:
                self.pod_metadata = ObjectMeta(name=name, namespace=namespace)
                self.pod_spec = PodSpec(name=name, image=image)
                self.pod_spec.set_restart_policy('Always')
                self._update_model()

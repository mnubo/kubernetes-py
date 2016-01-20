from kubernetes.models.v1.BaseModel import BaseModel
from kubernetes.models.v1.Container import Container


class PodSpec(BaseModel):
    def __init__(self, name=None, image=None, model=None):
        BaseModel.__init__(self)
        self.containers = list()
        if model is not None:
            assert isinstance(model, dict)
            self.model = model
            for c in self.model['containers']:
                self.containers.append(Container(model=c))
        else:
            self.model = {
                "containers": [],
                "dnsPolicy": "Default",
                "volumes": []
            }
            if name is not None and image is not None:
                if not isinstance(name, str) or not isinstance(image, str):
                    raise SyntaxError('PodSpec: Name and image should be strings.')
                self.containers.append(Container(name=name, image=image))
                self._update_model()

    def _update_model(self):
        self.model['containers'] = []
        for c in self.containers:
            assert isinstance(c, Container)
            self.model['containers'].append(c.get())

    def add_container(self, container=None):
        if container is None or not isinstance(container, Container):
            raise SyntaxError('PodSpec: container should be a container object.')
        else:
            self.containers.append(container)
            self._update_model()
        return self

    def add_host_volume(self, name=None, path=None):
        if (name is None or path is None) or (not isinstance(name, str) or not isinstance(path, str)):
            raise SyntaxError('PodSpec: name and path should be strings.')
        else:
            self.model['spec']['volumes'].append({
                "name": name,
                "source": {
                    "hostPath": {
                        "path": path
                    }
                }
            })
        return self

    def set_active_deadline(self, seconds=None):
        if seconds is None or not isinstance(seconds, int):
            raise SyntaxError('PodSpec: seconds should be a positive integer.')
        self.model['spec']['activeDeadlineSeconds'] = seconds
        return self

    def set_dns_policy(self, policy='Default'):
        if policy in ['Default', 'ClusterFirst']:
            self.model['spec']['dnsPolicy'] = policy
        else:
            raise SyntaxError('PodSpec: policy should be one of: Default, ClusterFirst')
        return self

    def set_image_pull_secrets(self, name=None):
        if name is None or not isinstance(name, str):
            raise SyntaxError('name should be a string.')
        self.model['spec']['imagePullSecrets'] = dict(name=name)
        return self

    def set_restart_policy(self, policy='Never'):
        if policy in ['Always', 'OnFailure', 'Never']:
            self.model['spec']['restartPolicy'] = policy
        else:
            raise SyntaxError('PodSpec: policy should be one of: Always, OnFailure, Never')
        return self

    def set_service_account(self, name=None):
        if name is None or not isinstance(name, str):
            raise SyntaxError('PodSpec: name should be a string.')
        self.model['spec']['serviceAccountName'] = name
        return self

    def set_termination_grace_period(self, seconds=None):
        if seconds is None or not isinstance(seconds, int):
            raise SyntaxError('PodSpec: seconds should be a positive integer.')
        self.model['spec']['terminationGracePeriodSeconds'] = seconds
        return self

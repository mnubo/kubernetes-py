from . import PodSpec


class Pod:
    def __init__(self, name=None, image=None, namespace='default'):
        if name is None or not isinstance(name, str):
            raise SyntaxError('name should be a string.')
        self.model = dict(kind='Pod', apiVersion='v1')
        self.model['metadata'] = dict(name=name, namespace=namespace, labels=dict(name=name))
        pod_spec = PodSpec(name=name, image=image)
        self.model['spec'] = pod_spec.get()

    def get(self):
        return self.model

    def add_container(self, container):
        try:
            self.model['spec'].add_container(container=container)
        except:
            raise
        return

    def add_host_volume(self, name, path):
        try:
            self.model['spec'].add_host_volume(name=name, path=path)
        except:
            raise
        return

    def add_label(self, k=None, v=None):
        if k is None or v is None:
            raise SyntaxError
        self.model['metadata']['labels'].update({k: v})
        return

    def set_active_deadline(self, seconds):
        try:
            self.model['spec'].set_active_deadline(seconds)
        except:
            raise
        return

    def set_dns_policy(self, policy):
        try:
            self.model['spec'].set_dns_policy(policy=policy)
        except:
            raise
        return

    def set_image_pull_secrets(self, name):
        try:
            self.model['spec'].set_image_pull_secrets(name=name)
        except:
            raise
        return

    def set_name(self, name=None):
        if name is None:
            raise SyntaxError
        self.model['metadata']['name'] = name
        self.model['metadata']['labels']['name'] = name
        return

    def set_namespace(self, name=None):
        if name is None:
            raise SyntaxError
        self.model['metadata']['namespace'] = name
        return

    def set_restart_policy(self, policy):
        try:
            self.model['spec'].set_restart_policy(policy=policy)
        except:
            raise
        return

    def set_service_account(self, name):
        try:
            self.model['spec'].set_service_account(name=name)
        except:
            raise
        return

    def set_termination_grace_period(self, seconds=None):
        try:
            self.model['spec'].set_termination_grace_period(seconds=seconds)
        except:
            raise
        return

from . import PodSpec


class ReplicationController:
    def __init__(self, name=None, image=None, namespace='default', replicas=1):
        if name is None or not isinstance(name, str):
            raise SyntaxError('name should be a string.')
        self.model = dict(kind='ReplicationController', apiVersion='v1')
        self.model['metadata'] = dict(name=name, namespace=namespace, labels=dict(name=name))
        pod_template = PodSpec(name=name, image=image)
        self.model['spec'] = {
            "replicas": replicas,
            "selector": dict(name=name),
            "template": pod_template.get()
        }

    def get(self):
        return self.model

    def set_name(self, name=None):
        if name is None or not isinstance(name, str):
            raise SyntaxError('name should be a string.')
        self.model['metadata']['name'] = name
        self.model['metadata']['labels']['name'] = name
        return

    def set_namespace(self, name=None):
        if name is None or not isinstance(name, str):
            raise SyntaxError('namespace name should be a string.')
        self.model['metadata']['namespace'] = name
        return

    def set_replicas(self, replicas=None):
        if replicas is None or not isinstance(replicas, int):
            raise SyntaxError('replicas should be a positive integer value')
        self.model['spec']['replicas'] = replicas
        return

    def set_selector(self, selector=None):
        if selector is None or not isinstance(selector, dict):
            raise SyntaxError('Selector should be a dict of key, value pairs.')
        self.model['spec']['selector'] = selector
        return

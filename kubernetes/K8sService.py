from kubernetes.K8sObject import K8sObject
from kubernetes.models.v1.Service import Service


class K8sService(K8sObject):

    def __init__(self, config=None, name=None):
        K8sObject.__init__(self, config=config, obj_type='Service', name=name)
        self.model = Service(name=name, namespace=self.config.get_namespace())

    def add_label(self, k, v):
        assert isinstance(k, str)
        assert isinstance(v, str)
        self.model.add_label(k=k, v=v)
        return self

    def add_port(self, name, port, target_port, protocol='TCP'):
        assert isinstance(name, str)
        assert isinstance(port, int)
        assert isinstance(protocol, str)
        self.model.add_port(name=name, port=port, target_port=target_port, protocol=protocol)
        return self

    def add_selector(self, selector):
        assert isinstance(selector, dict)
        self.model.add_selector(selector=selector)
        return self

    def get(self):
        self.model = Service(model=self.get_model())
        return self

    def set_cluster_ip(self, ip):
        assert isinstance(ip, str)
        self.model.set_cluster_ip(ip=ip)
        return self

    def set_external_ip(self, ips):
        assert isinstance(ips, list)
        self.model.set_external_ip(ips=ips)
        return self

    def set_load_balancer_ip(self, ip):
        assert isinstance(ip, str)
        self.model.set_load_balancer_ip(ip=ip)
        return self

    def set_namespace(self, name):
        assert isinstance(name, str)
        self.set_namespace(name=name)
        return self

    def set_session_affinity(self, affinity_type):
        assert isinstance(affinity_type, str)
        self.model.set_session_affinity(affinity_type=affinity_type)
        return self

    def set_service_type(self, service_type):
        assert isinstance(service_type, str)
        self.model.set_service_type(service_type=service_type)
        return self

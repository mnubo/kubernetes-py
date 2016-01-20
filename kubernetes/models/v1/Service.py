from kubernetes.models.v1.BaseModel import BaseModel
from kubernetes.models.v1.ObjectMeta import ObjectMeta


class Service(BaseModel):
    def __init__(self, name=None, namespace='default', port_name=None, port=0,
                 target_port=None, selector=None, session_affinity='None', model=None):
        BaseModel.__init__(self)
        if model is not None:
            assert isinstance(model, dict)
            self.model = model
            self.svc_metadata = ObjectMeta(model=self.model['metadata'])
        else:
            self.model = dict(kind='Service', apiVersion='v1')
            self.svc_metadata = ObjectMeta(name=name, namespace=namespace)
            self.model['spec'] = dict(ports=[], selector=dict(), sessionAffinity=session_affinity, type='ClusterIP')
            if port_name is not None and port > 0 and target_port is not None:
                self.add_port(port=port, target_port=target_port, name=port_name)
            if selector is not None:
                self.add_selector(selector=selector)
            self._update_model()

    def _update_model(self):
        self.model['metadata'] = self.svc_metadata.get()
        return self

    def add_label(self, k, v):
        assert isinstance(k, str)
        assert isinstance(v, str)
        self.svc_metadata.add_label(k=k, v=v)
        self._update_model()
        return self

    def add_port(self, name=None, port=None, target_port=None, protocol='TCP'):
        if (port is None or target_port is None or name is None) or (not isinstance(port, int)):
            raise SyntaxError('port and target_port should be positive integers')
        if protocol not in ['TCP', 'UDP']:
            raise SyntaxError('protocol should be TCP or UDP.')
        if isinstance(target_port, int):
            self.model['spec']['ports'].append(dict(name=name, protocol=protocol,
                                                    port=int(port), target_port=int(target_port)))
        else:
            self.model['spec']['ports'].append(dict(name=name, protocol=protocol,
                                                    port=int(port), target_port=target_port))
        return self

    def add_selector(self, selector=None):
        if (selector is None) or (not isinstance(selector, dict)):
            raise SyntaxError('Service: selector should be a dict of string, string.')
        if 'selector' not in self.model['spec'].keys():
            self.model['spec']['selector'] = dict()
        self.model['spec']['selector'].update(selector)
        return self

    def set_cluster_ip(self, ip=None):
        if ip is not None:
            self.model['spec']['clusterIP'] = ip
        return self

    def set_external_ip(self, ips=None):
        if ips is None or not isinstance(ips, list):
            raise SyntaxError('Service: ips should be a list of IP addresses')
        self.model['spec']['externalIPs'] = ips
        return self

    def set_load_balancer_ip(self, ip=None):
        if ip is None:
            raise SyntaxError('Service: ip should be an ip address.')
        self.model['spec']['loadBalancerIP'] = ip
        return self

    def set_name(self, name):
        assert isinstance(name, str)
        self.svc_metadata.set_name(name=name)
        self._update_model()
        return self

    def set_namespace(self, name):
        assert isinstance(name, str)
        self.svc_metadata.set_namespace(name=name)
        self._update_model()
        return self

    def set_session_affinity(self, affinity_type=None):
        if affinity_type is None or affinity_type not in ['None', 'ClientIP']:
            raise SyntaxError('Service: affinity_type should be either: None or ClientIP')
        self.model['spec']['sessionAffinity'] = affinity_type
        return self

    def set_service_type(self, service_type=None):
        if service_type is None or service_type not in ['ClusterIP', 'NodePort', 'LoadBalancer']:
            raise SyntaxError('Service: service_type should be one of: ClusterIP, NodePort, LoadBalancer')
        self.model['spec']['type'] = service_type
        return self

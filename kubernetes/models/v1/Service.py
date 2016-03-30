from kubernetes.models.v1.BaseModel import BaseModel
from kubernetes.models.v1.ObjectMeta import ObjectMeta


class Service(BaseModel):
    def __init__(self, name=None, namespace='default', port_name=None, port=0,
                 target_port=None, selector=None, session_affinity='None', model=None):
        BaseModel.__init__(self)
        if model is not None:
            assert isinstance(model, dict)
            self.model = model
            if 'status' in self.model.keys():
                self.model.pop('status', None)
            self.svc_metadata = ObjectMeta(model=self.model['metadata'], del_server_attr=False)
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
        return self

    def add_annotation(self, k, v):
        assert isinstance(k, str)
        assert isinstance(v, str)
        self.svc_metadata.add_annotation(k=k, v=v)
        return self

    def add_port(self, port, name=None, target_port=None, protocol=None, node_port=None):
        my_port = dict()

        if port is not None and isinstance(port, int):
            my_port['port'] = port
        else:
            raise SyntaxError('port should be an integer.')

        if name is not None:
            if isinstance(name, str):
                my_port['name'] = name
            else:
                raise SyntaxError('name should be a string.')

        if protocol is not None:
            if protocol in ['TCP', 'UDP']:
                my_port['protocol'] = protocol
            else:
                raise SyntaxError('protocol should be TCP or UDP')

        if target_port is not None:
            if isinstance(target_port, int):
                my_port['targetPort'] = target_port
            elif isinstance(target_port, str):
                my_port['targetPort'] = target_port
            else:
                raise SyntaxError('target_port should either be a string or an integer')

        if node_port is not None:
            if isinstance(node_port, int):
                my_port['nodePort'] = node_port
            else:
                raise SyntaxError('node_port should be an integer.')

        self.model['spec']['ports'].append(my_port)
        return self

    def add_selector(self, selector=None):
        if (selector is None) or (not isinstance(selector, dict)):
            raise SyntaxError('Service: selector should be a dict of string, string.')
        if 'selector' not in self.model['spec'].keys():
            self.model['spec']['selector'] = dict()
        self.model['spec']['selector'].update(selector)
        return self

    def del_annotation(self, k):
        assert isinstance(k, str)
        self.svc_metadata.del_annotation(k=k)
        return self

    def del_label(self, k):
        assert isinstance(k, str)
        self.svc_metadata.del_label(k=k)
        return self

    def del_meta_creation_timestamp(self):
        self.svc_metadata.del_creation_timestamp()
        return self

    def del_meta_generation(self):
        self.svc_metadata.del_generation()
        return self

    def del_meta_resource_version(self):
        self.svc_metadata.del_resource_version()
        return self

    def del_meta_self_link(self):
        self.svc_metadata.del_self_link()
        return self

    def del_meta_uid(self):
        self.svc_metadata.del_uid()
        return self

    def del_server_generated_meta_attr(self):
        return self.svc_metadata.del_server_generated_meta_attr()

    def get_annotation(self, k):
        assert isinstance(k, str)
        return self.svc_metadata.get_annotation(k=k)

    def get_annotations(self):
        return self.svc_metadata.get_annotations()

    def get_cluster_ip(self):
        return self.model['spec']['clusterIP']

    def get_label(self, k):
        assert isinstance(k, str)
        return self.svc_metadata.get_label(k=k)

    def get_labels(self):
        return self.svc_metadata.get_annotations()

    def get_name(self):
        return self.svc_metadata.get_name()

    def get_namespace(self):
        return self.svc_metadata.get_namespace()

    def get_meta_creation_timestamp(self):
        return self.svc_metadata.get_creation_timestamp()

    def get_meta_generation(self):
        return self.svc_metadata.get_generation()

    def get_meta_resource_version(self):
        return self.svc_metadata.get_resource_version()

    def get_meta_self_link(self):
        return self.svc_metadata.get_self_link()

    def get_meta_uid(self):
        return self.svc_metadata.get_uid()

    def set_annotations(self, new_dict):
        assert isinstance(new_dict, dict)
        self.svc_metadata.set_annotations(new_dict=new_dict)
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

    def set_labels(self, new_dict):
        assert isinstance(new_dict, dict)
        self.svc_metadata.set_labels(new_dict=new_dict)
        return self

    def set_load_balancer_ip(self, ip=None):
        if ip is None:
            raise SyntaxError('Service: ip should be an ip address.')
        self.model['spec']['loadBalancerIP'] = ip
        return self

    def set_meta_creation_timestamp(self, ts):
        return self.svc_metadata.set_creation_timestamp(ts=ts)

    def set_meta_generation(self, gen):
        return self.svc_metadata.set_generation(gen=gen)

    def set_meta_resource_version(self, ver):
        return self.svc_metadata.set_resource_version(ver=ver)

    def set_meta_self_link(self, link):
        return self.svc_metadata.set_self_link(link=link)

    def set_meta_uid(self, uid):
        return self.svc_metadata.set_uid(uid=uid)

    def set_name(self, name):
        assert isinstance(name, str)
        self.svc_metadata.set_name(name=name)
        return self

    def set_namespace(self, name):
        assert isinstance(name, str)
        self.svc_metadata.set_namespace(name=name)
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

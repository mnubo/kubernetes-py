class Service:
    def __init__(self, name=None, namespace='default', port_name=None, port=0,
                 target_port=None, selector=None, session_affinity='None'):
        self.model = dict(kind='Service', apiVersion='v1')
        self.model['metadata'] = dict(name=name, namespace=namespace, labels=dict(name=name))
        self.model['spec'] = dict(ports=[], selector=[], sessionAffinity=session_affinity, type='ClusterIP')
        if port_name is not None and port > 0 and target_port is not None:
            self.add_port(port=port, target_port=target_port, name=port_name)
        if selector is not None:
            self.add_selector(selector=selector)

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

    def add_selector(self, selector=None):
        if (selector is None) or (not isinstance(selector, dict)):
            raise SystemError('selector should be a dict of string, string.')
        self.model['spec']['selector'].update(selector)
        return

    def set_cluster_ip(self, ip=None):
        if ip is None:
            ip = ""
        self.model['spec']['clusterIP'] = ip
        return

    def set_externap_ip(self, ips=None):
        if ips is None or not isinstance(ips, list):
            raise SyntaxError('ips should be a list of IP addresses')
        self.model['spec']['externalIPs'] = ips
        return

    def set_load_balancer_ip(self, ip=None):
        if ip is None:
            raise SyntaxError('ip should be an ip address.')
        self.model['spec']['loadBalancerIP'] = ip
        return

    def set_session_affinity(self, affinity_type=None):
        if affinity_type is None or affinity_type not in ['None', 'ClientIP']:
            raise SyntaxError('affinity_type should be either: None or ClientIP')
        self.model['spec']['sessionAffinity'] = affinity_type
        return

    def set_service_type(self, service_type=None):
        if service_type is None or service_type not in ['ClusterIP', 'NodePort', 'LoadBalancer']:
            raise SyntaxError('service_type should be one of: ClusterIP, NodePort, LoadBalancer')
        self.model['spec']['type'] = service_type
        return

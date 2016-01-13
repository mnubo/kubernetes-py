import base64


class Secret:
    def __init__(self, name=None, namespace='default'):
        if name is None or not isinstance(name, str):
            raise SyntaxError('name must be a string.')
        self.model = dict(kind='Secret', apiVersion='v1')
        self.model['metadata'] = dict(name=name, namespace=namespace, labels=dict(name=name))

    def set_data(self, data_key=None, data_value=None):
        if data_key is None or data_value is None:
            raise SyntaxError('data_key should be a string and data_value a content')
        else:
            if 'data' not in self.model.keys():
                self.model['data'] = dict()
            self.model['data'] = base64.b64encode(data_value)
        return

    def set_type(self, secret_type=None):
        if secret_type is None or not isinstance(secret_type, str):
            raise SyntaxError('secret_type must be a string')
        self.model['type'] = secret_type
        return

    def set_dockercfg_secret(self, data=None):
        if data is None or not isinstance(data, str):
            raise SyntaxError('data must be a string')
        self.set_type(secret_type='kubernetes.io/dockercfg')
        self.set_data(data_key='.dockercfg', data_value=data)
        return

    def set_dockercfg_json_secret(self, data=None):
        if data is None or not isinstance(data, str):
            raise SyntaxError('data must be a string')
        self.set_type(secret_type='kubernetes.io/dockerconfigjson')
        self.set_data(data_key='.dockerconfigjson', data_value=data)
        return

    def set_service_account_token(self, account_name=None, account_uid=None, token=None,
                                  kubecfg_data=None, cacert=None):
        if account_name is None or account_uid is None or token is None \
                or not isinstance(account_name, str) or not isinstance(account_uid, str) \
                or not isinstance(token, str):
            raise SyntaxError('account_name, account_uid and token must be strings.')
        self.set_type(secret_type='kubernetes.io/service-account-token')
        self.model['metadata']['annotations'] = dict()
        self.model['metadata']['annotations']['kubernetes.io/service-account.name'] = account_name
        self.model['metadata']['annotations']['kubernetes.io/service-account.uid'] = account_uid
        self.set_data(data_key='token', data_value=token)
        if kubecfg_data is not None:
            self.set_data(data_key='kubernetes.kubeconfig', data_value=kubecfg_data)
        if cacert is not None:
            self.set_data(data_key='ca.crt', data_value=cacert)
        return

from kubernetes.K8sObject import K8sObject
from kubernetes.models.v1.Secret import Secret


class K8sSecret(K8sObject):

    def __init__(self, config=None, name=None):
        K8sObject.__init__(self, config=config, obj_type='Secret', name=name)
        self.model = Secret(name=name, namespace=self.config.namespace)

    def add_annotation(self, k, v):
        assert isinstance(k, str)
        assert isinstance(v, str)
        self.model.add_annotation(k=k, v=v)
        return self

    def add_label(self, k, v):
        assert isinstance(k, str)
        assert isinstance(v, str)
        self.model.add_label(k=k, v=v)
        return self

    def get(self):
        self.model = Secret(model=self.get_model())
        return self

    def set_data(self, data_key, data_value):
        assert isinstance(data_value, str)
        assert isinstance(data_value, str)
        self.model.set_data(data_key=data_key, data_value=data_value)
        return self

    def set_type(self, secret_type):
        assert isinstance(secret_type, str)
        self.model.set_type(secret_type=secret_type)
        return self

    def set_dockercfg_secret(self, data):
        assert isinstance(data, str)
        self.model.set_dockercfg_secret(data=data)
        return self

    def set_dockercfg_json_secret(self, data):
        assert isinstance(data, str)
        self.model.set_dockercfg_json_secret(data=data)
        return self

    def set_service_account_token(self, account_name, account_uid, token,
                                  kubecfg_data=None, cacert=None):
        assert isinstance(account_name, str)
        assert isinstance(account_uid, str)
        assert isinstance(token, str)
        self.model.set_service_account_token(account_name=account_name, account_uid=account_uid,
                                             token=token, kubecfg_data=kubecfg_data, cacert=cacert)
        return self

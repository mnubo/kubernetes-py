from kubernetes.models.v1.BaseModel import BaseModel
from kubernetes.models.v1.ObjectMeta import ObjectMeta
import base64


class Secret(BaseModel):
    def __init__(self, name=None, namespace='default', model=None):
        BaseModel.__init__(self)
        if model is not None:
            assert isinstance(model, dict)
            if 'status' in self.model.keys():
                self.model.pop('status', None)
            self.model = model
            self.secret_metadata = ObjectMeta(model=self.model['metadata'])
        else:
            if name is None or not isinstance(name, str):
                raise SyntaxError('name must be a string.')
            self.model = dict(kind='Secret', apiVersion='v1')
            self.secret_metadata = ObjectMeta(name=name, namespace=namespace)
            self._update_model()

    def _update_model(self):
        self.model['metadata'] = self.secret_metadata.get()
        return self

    def add_label(self, k=None, v=None):
        assert isinstance(k, str)
        assert isinstance(v, str)
        self.secret_metadata.add_label(k=k, v=v)
        return self

    def add_annotation(self, k=None, v=None):
        assert isinstance(k, str)
        assert isinstance(v, str)
        self.secret_metadata.add_annotation(k=k, v=v)
        return self

    def get_annotation(self, k):
        assert isinstance(k, str)
        return self.secret_metadata.get_annotation(k=k)

    def get_annotations(self):
        return self.secret_metadata.get_annotations()

    def get_label(self, k):
        assert isinstance(k, str)
        return self.secret_metadata.get_label(k=k)

    def get_labels(self):
        return self.secret_metadata.get_annotations()

    def set_annotations(self, new_dict):
        assert isinstance(new_dict, dict)
        self.secret_metadata.set_annotations(dico=new_dict)
        return self

    def set_data(self, data_key=None, data_value=None):
        if data_key is None or data_value is None:
            raise SyntaxError('Secret: data_key should be a string and data_value a content')
        else:
            if 'data' not in self.model.keys():
                self.model['data'] = dict()
            self.model['data'][data_key] = base64.b64encode(data_value)
        return self

    def set_dockercfg_secret(self, data=None):
        if data is None or not isinstance(data, str):
            raise SyntaxError('Secret: data must be a string')
        self.set_type(secret_type='kubernetes.io/dockercfg')
        self.set_data(data_key='.dockercfg', data_value=data)
        return self

    def set_dockercfg_json_secret(self, data=None):
        if data is None or not isinstance(data, str):
            raise SyntaxError('Secret: data must be a string')
        self.set_type(secret_type='kubernetes.io/dockerconfigjson')
        self.set_data(data_key='.dockerconfigjson', data_value=data)
        return self

    def set_labels(self, new_dict):
        assert isinstance(new_dict, dict)
        self.secret_metadata.set_labels(dico=new_dict)
        return self

    def set_service_account_token(self, account_name=None, account_uid=None, token=None,
                                  kubecfg_data=None, cacert=None):
        if account_name is None or account_uid is None or token is None \
                or not isinstance(account_name, str) or not isinstance(account_uid, str) \
                or not isinstance(token, str):
            raise SyntaxError('Secret: account_name, account_uid and token must be strings.')
        self.set_type(secret_type='kubernetes.io/service-account-token')
        self.secret_metadata.add_annotation(k='kubernetes.io/service-account.name', v=account_name)
        self.secret_metadata.add_annotation(k='kubernetes.io/service-account.uid', v=account_uid)
        self.set_data(data_key='token', data_value=token)
        if kubecfg_data is not None:
            self.set_data(data_key='kubernetes.kubeconfig', data_value=kubecfg_data)
        if cacert is not None:
            self.set_data(data_key='ca.crt', data_value=cacert)
        return self

    def set_type(self, secret_type=None):
        if secret_type is None or not isinstance(secret_type, str):
            raise SyntaxError('Secret: secret_type must be a string')
        self.model['type'] = secret_type
        return self

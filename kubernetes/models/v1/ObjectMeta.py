from kubernetes.models.v1.BaseModel import BaseModel


class ObjectMeta(BaseModel):
    def __init__(self, name=None, namespace='default', model=None):
        BaseModel.__init__(self)
        if model is not None:
            self.model = model
            if 'generation' in self.model.keys():
                self.model.pop('generation', None)
            if 'resourceVersion' in self.model.keys():
                self.model.pop('resourceVersion', None)
            if 'creationTimestamp' in self.model.keys():
                self.model.pop('creationTimestamp', None)
            if 'status' in self.model.keys():
                self.model.pop('status', None)
            if 'selfLink' in self.model.keys():
                self.model.pop('selfLink', None)
            if 'uid' in self.model.keys():
                self.model.pop('uid', None)
        else:
            self.model = dict(name=name, namespace=namespace, labels=dict(name=name))

    def add_annotation(self, k=None, v=None):
        if k is None or v is None:
            raise SyntaxError('ObjectMeta: make sure to fill key and value when adding an annotation.')
        if 'annotations' not in self.model.keys():
            self.model['annotations'] = dict()
        if k not in self.model['annotations'].keys():
            self.model['annotations'].update({k: v})
        else:
            self.model['annotations'][k] = v
        return self

    def add_label(self, k=None, v=None):
        if k is None or v is None:
            raise SyntaxError('ObjectMeta: make sure to fill key and value when adding a label.')
        if k not in self.model['labels'].keys():
            self.model['labels'].update({k: v})
        else:
            self.model['labels'][k] = v
        return self

    def del_annotation(self, k=None):
        if k is None or not isinstance(k, str):
            raise SyntaxError('ObjectMeta: make sure k is a string')
        if k in self.model['annotations'].keys():
            assert isinstance(self.model['annotations'], dict)
            self.model['annotations'].pop(k, None)
        return self

    def del_label(self, k=None):
        if k is None or not isinstance(k, str):
            raise SyntaxError('ObjectMeta: make sure k is a string')
        if k in self.model['labels'].keys():
            assert isinstance(self.model['labels'], dict)
            self.model['labels'].pop(k, None)
        return self

    def get_annotation(self, k):
        my_value = None
        if not isinstance(k, str):
            raise SyntaxError('ObjectMeta: k should be a string.')
        if 'annotations' in self.model.keys():
            if k in self.model['annotations'].keys():
                my_value = self.model['annotations'][k]
        return my_value

    def get_annotations(self):
        my_value = None
        if 'annotations' in self.model.keys():
            my_value = self.model['annotations']
        return my_value

    def get_label(self, k):
        my_value = None
        if not isinstance(k, str):
            raise SyntaxError('ObjectMeta: k should be a string.')
        if 'labels' in self.model.keys():
            if k in self.model['labels'].keys():
                my_value = self.model['labels'][k]
        return my_value

    def get_labels(self):
        my_value = None
        if 'labels' in self.model.keys():
            my_value = self.model['labels']
        return my_value

    def get_name(self):
        return self.model['name']

    def get_namespace(self):
        return self.model['namespace']

    def set_annotations(self, new_dict):
        assert isinstance(new_dict, dict)
        self.model['annotations'] = new_dict
        return self

    def set_generate_name(self, mode, name=None):
        if not isinstance(mode, bool):
            raise SyntaxError('ObjectMeta: ensure mode is True or False')
        if mode:
            if name is None:
                self.model['generateName'] = self.model['name']
            else:
                assert isinstance(name, str)
                self.model['generateName'] = name
        else:
            if 'generateName' in self.model.keys():
                self.model.pop('generatedName', None)
        return self

    def set_labels(self, new_dict):
        assert isinstance(new_dict, dict)
        self.model['labels'] = new_dict
        return self

    def set_name(self, name=None, set_label=True):
        if name is None or not isinstance(name, str):
            raise SyntaxError('ObjectMeta: name should be a string.')
        self.model['name'] = name
        if set_label:
            self.model['labels']['name'] = name
        return self

    def set_namespace(self, name=None):
        if name is None or not isinstance(name, str):
            raise SyntaxError('ObjectMeta: namespace name should be a string.')
        self.model['namespace'] = name
        return self

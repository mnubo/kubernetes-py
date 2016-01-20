from kubernetes.models.v1.BaseModel import BaseModel


class ObjectMeta(BaseModel):
    def __init__(self, name=None, namespace='default', model=None):
        if model is not None:
            self.model = model
        else:
            self.model = dict(name=name, namespace=namespace, labels=dict(name=name))

    def add_label(self, k=None, v=None):
        if k is None or v is None:
            raise SyntaxError('ObjectMeta: make sure to fill key and value when adding a label.')
        if k not in self.model['labels'].keys():
            self.model['labels'].update({k: v})
        else:
            self.model['labels'][k] = v
        return self

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

    def set_generate_name(self, mode):
        if not isinstance(mode, bool):
            raise SyntaxError('ObjectMeta: ensure mode is True or False')
        if mode:
            self.model['generateName'] = 'True'
        else:
            if 'generateName' in self.model.keys():
                self.model.pop('generatedName', None)
        return self

    def set_name(self, name=None):
        if name is None or not isinstance(name, str):
            raise SyntaxError('ObjectMeta: name should be a string.')
        self.model['name'] = name
        self.model['labels']['name'] = name
        return self

    def set_namespace(self, name=None):
        if name is None or not isinstance(name, str):
            raise SyntaxError('ObjectMeta: namespace name should be a string.')
        self.model['namespace'] = name
        return self

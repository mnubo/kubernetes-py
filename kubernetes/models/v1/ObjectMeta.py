from kubernetes.models.v1.BaseModel import BaseModel


class ObjectMeta(BaseModel):
    def __init__(self, name=None, namespace='default', model=None, del_server_attr=True):
        BaseModel.__init__(self)
        if model is not None:
            self.model = model
            if del_server_attr:
                self.del_server_generated_meta_attr()
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

    def del_creation_timestamp(self):
        if 'creationTimestamp' in self.model.keys():
            self.model.pop('creationTimestamp', None)
        return self

    def del_deletion_timestamp(self):
        if 'deletionTimestamp' in self.model.keys():
            self.model.pop('deletionTimestamp', None)
        return self

    def del_deletion_grace_period_seconds(self):
        if 'deletionGracePeriodSeconds' in self.model.keys():
            self.model.pop('deletionGracePeriodSeconds', None)
        return self

    def del_generation(self):
        if 'generation' in self.model.keys():
            self.model.pop('generation', None)
        return self

    def del_label(self, k=None):
        if k is None or not isinstance(k, str):
            raise SyntaxError('ObjectMeta: make sure k is a string')
        if k in self.model['labels'].keys():
            assert isinstance(self.model['labels'], dict)
            self.model['labels'].pop(k, None)
        return self

    def del_resource_version(self):
        if 'resourceVersion' in self.model.keys():
            self.model.pop('resourceVersion', None)
        return self

    def del_status(self):
        if 'status' in self.model.keys():
            self.model.pop('status', None)
        return self

    def del_self_link(self):
        if 'selfLink' in self.model.keys():
            self.model.pop('selfLink', None)
        return self

    def del_server_generated_meta_attr(self):
        self.del_generation()\
            .del_resource_version()\
            .del_creation_timestamp()\
            .del_deletion_timestamp()\
            .del_deletion_grace_period_seconds()\
            .del_status()\
            .del_self_link()\
            .del_uid()
        return self

    def del_uid(self):
        if 'uid' in self.model.keys():
            self.model.pop('uid', None)
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

    def get_creation_timestamp(self):
        my_value = None
        if 'creationTimestamp' in self.model.keys():
            my_value = self.model['creationTimestamp']
        return my_value

    def get_deletion_timestamp(self):
        my_value = None
        if 'deletionTimestamp' in self.model.keys():
            my_value = self.model['deletionTimestamp']
        return my_value

    def get_deletion_grace_period_seconds(self):
        my_value = None
        if 'deletionGracePeriodSeconds' in self.model.keys():
            my_value = self.model['deletionGracePeriodSeconds']
        return my_value

    def get_generate_name(self):
        my_value = None
        if 'generateName' in self.model.keys():
            my_value = self.model['generateName']
        return my_value

    def get_generation(self):
        my_value = None
        if 'generation' in self.model.keys():
            my_value = self.model['generation']
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

    def get_resource_version(self):
        my_value = None
        if 'resourceVersion' in self.model.keys():
            my_value = self.model['resourceVersion']
        return my_value

    def get_status(self):
        my_value = None
        if 'status' in self.model.keys():
            my_value = self.model['status']
        return my_value

    def get_self_link(self):
        my_value = None
        if 'selfLink' in self.model.keys():
            my_value = self.model['selfLink']
        return my_value

    def get_uid(self):
        my_value = None
        if 'uid' in self.model.keys():
            my_value = self.model['uid']
        return my_value

    def set_annotations(self, new_dict):
        assert isinstance(new_dict, dict)
        self.model['annotations'] = new_dict
        return self

    def set_creation_timestamp(self, ts=None):
        if ts is None or not isinstance(ts, str):
            raise SyntaxError('ObjectMeta: ts should be a string.')
        self.model['creationTimestamp'] = ts
        return self

    def set_deletion_timestamp(self, ts=None):
        if ts is None or not isinstance(ts, str):
            raise SyntaxError('ObjectMeta: ts should be a string.')
        self.model['deletionTimestamp'] = ts
        return self

    def set_deletion_grace_period_seconds(self, secs=None):
        if secs is None or not isinstance(secs, str):
            raise SyntaxError('ObjectMeta: secs should be a int.')
        self.model['deletionGracePeriodSeconds'] = secs
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
                self.model.pop('generateName', None)
        return self

    def set_generation(self, gen=None):
        if gen is None or not isinstance(gen, int):
            raise SyntaxError('ObjectMeta: gen should be a int.')
        self.model['generation'] = gen
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

    def set_resource_version(self, ver=None):
        if ver is None or not isinstance(ver, str):
            raise SyntaxError('ObjectMeta: gen should be a string.')
        self.model['resourceVersion'] = ver
        return self

    def set_self_link(self, link=None):
        if link is None or not isinstance(link, str):
            raise SyntaxError('ObjectMeta: link should be a string.')
        self.model['selfLink'] = link
        return self

    def set_uid(self, uid=None):
        if uid is None or not isinstance(uid, str):
            raise SyntaxError('ObjectMeta: uid should be a string.')
        self.model['uid'] = uid
        return self


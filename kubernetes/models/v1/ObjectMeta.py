#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
#

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

    # ------------------------------------------------------------------------------------- add

    def add_annotation(self, k=None, v=None):
        if k is None or v is None:
            raise SyntaxError('ObjectMeta: annotation: [ {0}, {1} ] cannot be None.'.format(k, v))
        if not isinstance(k, str) or not isinstance(v, str):
            kc = k.__class__.__name__
            vc = v.__class__.__name__
            raise SyntaxError('ObjectMeta: annotation: [ {0}, {1} ] must be strings.'.format(kc, vc))

        if 'annotations' not in self.model:
            self.model['annotations'] = dict()

        if k not in self.model['annotations']:
            self.model['annotations'].update({k: v})
        else:
            self.model['annotations'][k] = v

        return self

    def add_label(self, k=None, v=None):
        if k is None or v is None:
            raise SyntaxError('ObjectMeta: label: [ {0}, {1} ] cannot be None.'.format(k, v))
        if not isinstance(k, str) or not isinstance(v, str):
            kc = k.__class__.__name__
            vc = v.__class__.__name__
            raise SyntaxError('ObjectMeta: label: [ {0}, {1} ] must be strings.'.format(kc, vc))

        if k not in self.model['labels']:
            self.model['labels'].update({k: v})
        else:
            self.model['labels'][k] = v
        return self

    # ------------------------------------------------------------------------------------- delete

    def del_annotation(self, k=None):
        if k is None:
            raise SyntaxError('ObjectMeta: k: [ {0} ] cannot be None.'.format(k))
        if not isinstance(k, str):
            raise SyntaxError('ObjectMeta: k: [ {0} ] must be a string'.format(k.__class__.__name__))

        if 'annotations' not in self.model:
            return self

        if k in self.model['annotations']:
            assert isinstance(self.model['annotations'], dict)
            self.model['annotations'].pop(k, None)

        return self

    def del_creation_timestamp(self):
        if 'creationTimestamp' in self.model:
            self.model.pop('creationTimestamp', None)
        return self

    def del_deletion_timestamp(self):
        if 'deletionTimestamp' in self.model:
            self.model.pop('deletionTimestamp', None)
        return self

    def del_deletion_grace_period_seconds(self):
        if 'deletionGracePeriodSeconds' in self.model:
            self.model.pop('deletionGracePeriodSeconds', None)
        return self

    def del_generation(self):
        if 'generation' in self.model:
            self.model.pop('generation', None)
        return self

    def del_label(self, k=None):
        if k is None:
            raise SyntaxError('ObjectMeta: k: [ {0} ] cannot be None.'.format(k))
        if not isinstance(k, str):
            raise SyntaxError('ObjectMeta: k: [ {0} ] must be a string.'.format(k.__class__.__name__))

        if 'labels' not in self.model:
            return self

        if k in self.model['labels']:
            assert isinstance(self.model['labels'], dict)
            self.model['labels'].pop(k, None)

        return self

    def del_resource_version(self):
        if 'resourceVersion' in self.model:
            self.model.pop('resourceVersion', None)
        return self

    def del_status(self):
        if 'status' in self.model:
            self.model.pop('status', None)
        return self

    def del_self_link(self):
        if 'selfLink' in self.model:
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
        if 'uid' in self.model:
            self.model.pop('uid', None)
        return self

    # ------------------------------------------------------------------------------------- get

    def get_annotation(self, k):
        if k is None:
            raise SyntaxError('ObjectMeta: k: [ {0} ] cannot be None.'.format(k))
        if not isinstance(k, str):
            raise SyntaxError('ObjectMeta: k: [ {0} ] must be a string.'.format(k.__class__.__name__))
        if 'annotations' in self.model:
            if k in self.model['annotations']:
                return self.model['annotations'][k]
        return None

    def get_annotations(self):
        if 'annotations' in self.model:
            return self.model['annotations']
        return None

    def get_creation_timestamp(self):
        if 'creationTimestamp' in self.model:
            return self.model['creationTimestamp']
        return None

    def get_deletion_timestamp(self):
        if 'deletionTimestamp' in self.model:
            return self.model['deletionTimestamp']
        return None

    def get_deletion_grace_period_seconds(self):
        if 'deletionGracePeriodSeconds' in self.model:
            return self.model['deletionGracePeriodSeconds']
        return None

    def get_generate_name(self):
        if 'generateName' in self.model:
            return self.model['generateName']
        return None

    def get_generation(self):
        if 'generation' in self.model:
            return self.model['generation']
        return None

    def get_label(self, k):
        if k is None:
            raise SyntaxError('ObjectMeta: k: [ {0} ] cannot be None.'.format(k))
        if not isinstance(k, str):
            raise SyntaxError('ObjectMeta: k: [ {0} ] must be a string.'.format(k.__class__.__name__))
        if 'labels' in self.model and k in self.model['labels']:
            return self.model['labels'][k]
        return None

    def get_labels(self):
        if 'labels' in self.model:
            return self.model['labels']
        return None

    def get_name(self):
        return self.model['name']

    def get_namespace(self):
        return self.model['namespace']

    def get_resource_version(self):
        if 'resourceVersion' in self.model:
            return self.model['resourceVersion']
        return None

    def get_status(self):
        if 'status' in self.model:
            return self.model['status']
        return None

    def get_self_link(self):
        if 'selfLink' in self.model:
            return self.model['selfLink']
        return None

    def get_uid(self):
        if 'uid' in self.model:
            return self.model['uid']
        return None

    def set_annotations(self, dico=None):
        if dico is None:
            raise SyntaxError('ObjectMeta: dico: [ {0} ] cannot be None.'.format(dico))
        if not isinstance(dico, dict):
            raise SyntaxError('ObjectMeta: dico: [ {0} ] must be a dict.'.format(dico.__class__.__name__))
        for k, v in dico.iteritems():
            if not isinstance(k, str) or not isinstance(v, str):
                raise SyntaxError('ObjectMeta: dico: [ {0} ] must be a mapping of str -> str.'.format(dico))
        self.model['annotations'] = dico
        return self

    # ------------------------------------------------------------------------------------- set

    def set_creation_timestamp(self, ts=None):
        if ts is None:
            raise SyntaxError('ObjectMeta: ts: [ {0} ] cannot be None.'.format(ts))
        if not isinstance(ts, str):
            raise SyntaxError('ObjectMeta: ts: [ {0} ] must be a string.'.format(ts.__class__.__name__))
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
            if 'generateName' in self.model:
                self.model.pop('generateName', None)
        return self

    def set_generation(self, gen=None):
        if gen is None:
            raise SyntaxError('ObjectMeta: gen: [ {0} ] cannot be None.'.format(gen))
        if not isinstance(gen, int):
            raise SyntaxError('ObjectMeta: gen: [ {0} ] must be an int.'.format(gen.__class__.__name__))
        self.model['generation'] = gen
        return self

    def set_labels(self, labels=None):
        if labels is None:
            raise SyntaxError('ObjectMeta: dico: [ {0} ] cannot be None.'.format(labels))
        if not isinstance(labels, dict):
            raise SyntaxError('ObjectMeta: dico: [ {0} ] must be a dict.'.format(labels.__class__.__name__))
        for k, v in labels.iteritems():
            if not isinstance(k, str) or not isinstance(v, str):
                raise SyntaxError('ObjectMeta: dico: [ {0} ] must be a mapping of str -> str.'.format(labels))
        self.model['labels'] = labels
        return self

    def set_name(self, name=None, set_label=True):
        if name is None or not isinstance(name, str):
            raise SyntaxError('ObjectMeta: name should be a string.')
        self.model['name'] = name
        if set_label:
            self.model['labels']['name'] = name
        return self

    def set_namespace(self, name=None):
        if name is None:
            raise SyntaxError('ObjectMeta: name: [ {0} ] cannot be None.'.format(name))
        if not isinstance(name, str):
            raise SyntaxError('ObjectMeta: name: [ {0} ] must be a string.'.format(name.__class__.__name__))
        self.model['namespace'] = name
        return self

    def set_resource_version(self, ver=None):
        if ver is None:
            raise SyntaxError('ObjectMeta: ver: [ {0} ] cannot be None.'.format(ver))
        if not isinstance(ver, str):
            raise SyntaxError('ObjectMeta: ver: [ {0} ] must be a string.'.format(ver.__class__.__name__))
        self.model['resourceVersion'] = ver
        return self

    def set_self_link(self, link=None):
        if link is None:
            raise SyntaxError('ObjectMeta: link: [ {0} ] cannot be None.'.format(link))
        if not isinstance(link, str):
            raise SyntaxError('ObjectMeta: link: [ {0} ] must be a string.'.format(link.__class__.__name__))
        self.model['selfLink'] = link
        return self

    def set_uid(self, uid=None):
        if uid is None:
            raise SyntaxError('ObjectMeta: uid: [ {0} ] cannot be None.'.format(uid))
        if not isinstance(uid, str):
            raise SyntaxError('ObjectMeta: uid: [ {0} ] must be a string.'.format(uid.__class__.__name__))
        self.model['uid'] = uid
        return self

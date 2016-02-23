from kubernetes.K8sPodBasedObject import K8sPodBasedObject
from kubernetes.models.v1.Pod import Pod
from kubernetes.models.v1.PodStatus import PodStatus


class K8sPod(K8sPodBasedObject):
    def __init__(self, config=None, name=None):
        K8sPodBasedObject.__init__(self, config=config, obj_type='Pod', name=name)
        self.model = Pod(name=name, namespace=self.config.get_namespace())
        if self.config.get_pull_secret() is not None:
            self.model.add_image_pull_secrets(name=self.config.get_pull_secret())

    def add_annotation(self, k, v):
        self.model.add_pod_annotation(k=k, v=v)
        return self

    def add_label(self, k, v):
        self.model.add_pod_label(k=k, v=v)
        return self

    def del_annotation(self, k):
        self.model.del_pod_annotation(k=k)
        return self

    def del_label(self, k):
        self.model.del_pod_label(k=k)
        return self

    def get(self):
        self.model = Pod(model=self.get_model())
        return self

    def get_annotation(self, k):
        return self.model.get_pod_annotation(k=k)

    def get_annotations(self):
        return self.model.get_pod_annotations()

    def get_label(self, k):
        return self.model.get_pod_label(k=k)

    def get_labels(self):
        return self.model.get_pod_labels()

    def get_status(self):
        return self.model.get_pod_status()

    def is_ready(self):
        ready = False
        status = self.get_status()
        if status is not None:
            assert isinstance(status, PodStatus)
            pod_phase = status.get_pod_phase()
            conditions = status.get_pod_conditions()
            conditions_ok = 0
            for cond in conditions:
                assert isinstance(cond, dict)
                cond_type = cond.get('type', '')
                cond_status = cond.get('status', 'False')
                if cond_status == 'True' and cond_type == 'Ready':
                    conditions_ok += 1
            if pod_phase == 'Running' and len(conditions) == conditions_ok:
                ready = True
        return ready

    def set_annotations(self, new_dict):
        self.model.set_pod_annotations(new_dict=new_dict)
        return self

    def set_labels(self, new_dict):
        self.model.set_pod_labels(new_dict=new_dict)
        return self

    def set_namespace(self, name):
        self.model.set_pod_namespace(name=name)
        return self

    @staticmethod
    def get_by_name(config, name):
        try:
            pod_list = list()
            data = dict(labelSelector="name={pod_name}".format(pod_name=name))
            pods = K8sPod(config=config, name=name).get_with_params(data=data).get('items', list())
            for pod in pods:
                pod_name = Pod(model=pod).get_pod_name()
                pod_list.append(K8sPod(config=config, name=pod_name).get())
        except:
            raise
        return pod_list

    @staticmethod
    def get_by_labels(config, labels):
        assert isinstance(labels, dict)
        try:
            pod_list = list()
            my_labels = ",".join(['%s=%s' % (key, value) for (key, value) in labels.items()])
            data = dict(labelSelector="{labels}".format(labels=my_labels))
            pods = K8sPod(config=config, name=labels.get('name')).get_with_params(data=data).get('items', list())
            for pod in pods:
                pod_name = Pod(model=pod).get_pod_name()
                pod_list.append(K8sPod(config=config, name=pod_name).get())
        except:
            raise
        return pod_list

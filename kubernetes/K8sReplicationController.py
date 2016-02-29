from kubernetes.K8sPodBasedObject import K8sPodBasedObject
from kubernetes.K8sPod import K8sPod
from kubernetes.K8sContainer import K8sContainer
from kubernetes.models.v1.ReplicationController import ReplicationController
from kubernetes.exceptions.NotFoundException import NotFoundException
import uuid
import copy
import time


class K8sReplicationController(K8sPodBasedObject):

    def __init__(self, config=None, name=None, image=None, replicas=0):
        K8sPodBasedObject.__init__(self, config=config, obj_type='ReplicationController', name=name)
        self.model = ReplicationController(name=name, namespace=self.config.get_namespace())
        self.set_replicas(replicas)
        my_version = str(uuid.uuid4())
        self.model.add_pod_label(k='rc_version', v=my_version)
        self.set_selector(selector=dict(name=name, rc_version=my_version))
        if image is not None:
            self.model.add_container(K8sContainer(name=name, image=image).get_model())
            self.model.set_pod_name(name=name)
        if self.config.get_pull_secret() is not None:
            self.add_image_pull_secrets(name=self.config.get_pull_secret())

    def add_annotation(self, k, v):
        assert isinstance(k, str)
        if not isinstance(v, str):
            v = str(v)
        self.model.add_annotation(k=k, v=v)
        return self

    def add_label(self, k, v):
        assert isinstance(k, str)
        assert isinstance(v, str)
        self.model.add_label(k=k, v=v)
        return self

    def add_pod_annotation(self, k, v):
        assert isinstance(k, str)
        assert isinstance(v, str)
        self.model.add_pod_annotation(k=k, v=v)
        return self

    def add_pod_label(self, k, v):
        assert isinstance(k, str)
        assert isinstance(v, str)
        self.model.add_pod_label(k=k, v=v)
        return self

    def del_annotation(self, k):
        assert isinstance(k, str)
        self.model.del_annotation(k=k)
        return self

    def del_label(self, k):
        assert isinstance(k, str)
        self.model.del_label(k=k)
        return self

    def del_pod_annotation(self, k):
        assert isinstance(k, str)
        self.model.del_pod_annotation(k=k)
        return self

    def del_pod_label(self, k):
        assert isinstance(k, str)
        self.model.del_pod_label(k=k)
        return self

    def get(self):
        self.model = ReplicationController(model=self.get_model())
        return self

    def get_annotation(self, k):
        assert isinstance(k, str)
        return self.model.get_annotation(k=k)

    def get_annotations(self):
        return self.model.get_annotations()

    def get_label(self, k):
        assert isinstance(k, str)
        return self.model.get_label(k=k)

    def get_labels(self):
        return self.model.get_labels()

    def get_pod_annotation(self, k):
        assert isinstance(k, str)
        return self.model.get_pod_annotation(k=k)

    def get_pod_annotations(self):
        return self.model.get_pod_annotations()

    def get_pod_label(self, k):
        assert isinstance(k, str)
        return self.model.get_pod_label(k=k)

    def get_pod_labels(self):
        return self.model.get_pod_labels()

    def get_replicas(self):
        return self.model.get_replicas()

    def get_selector(self):
        return self.model.get_selector()

    def set_annotations(self, new_dict):
        assert isinstance(new_dict, dict)
        self.model.set_annotations(new_dict=new_dict)
        return self

    def set_labels(self, new_dict):
        assert isinstance(new_dict, dict)
        self.model.set_labels(new_dict=new_dict)
        return self

    def set_namespace(self, name):
        self.model.set_namespace(name=name)
        return self

    def set_pod_annotations(self, new_dict):
        assert isinstance(new_dict, dict)
        self.model.set_pod_annotations(new_dict=new_dict)
        return self

    def set_pod_labels(self, new_dict):
        assert isinstance(new_dict, dict)
        self.model.set_pod_labels(new_dict=new_dict)
        return self

    def set_replicas(self, replicas):
        self.model.set_replicas(replicas=replicas)
        return self

    def set_selector(self, selector):
        self.model.set_selector(selector=selector)
        return self

    def wait_for_replicas(self, replicas, labels=None):
        if labels is None:
            labels = self.get_pod_labels()
        name = labels.get('name', None)
        pod_list = list()
        ready_check = False

        print('Will wait for replicas to be equal to {replicas} and labels are: {labels}'.format(replicas=str(replicas),
                                                                                                 labels=labels))
        pod_qty = len(pod_list)
        while not ((pod_qty == replicas) and ready_check):
            try:
                if labels is None:
                    pod_list = K8sPod.get_by_name(config=self.config, name=name)
                else:
                    pod_list = K8sPod.get_by_labels(config=self.config, labels=labels)
                pod_qty = len(pod_list)
                if replicas > 0:
                    pods_ready = 0
                    for pod in pod_list:
                        assert isinstance(pod, K8sPod)
                        if pod.is_ready():
                            pods_ready += 1
                    if pods_ready == len(pod_list):
                        ready_check = True
                else:
                    ready_check = True
            except:
                raise
            time.sleep(0.2)
        return self

    @staticmethod
    def get_by_name(config, name):
        try:
            rc_list = list()
            data = dict(labelSelector="name={pod_name}".format(pod_name=name))
            rcs = K8sReplicationController(config=config, name=name).get_with_params(data=data)
            for rc in rcs:
                try:
                    rc_name = ReplicationController(model=rc).get_name()
                    rc_list.append(K8sReplicationController(config=config, name=rc_name).get())
                except NotFoundException:
                    pass
        except:
            raise
        return rc_list

    @staticmethod
    def resize(config, name, replicas):
        try:
            current_rc = K8sReplicationController(config=config, name=name).get()
            current_rc.set_replicas(replicas)
            current_rc.update()
            current_rc.wait_for_replicas(replicas=replicas)
        except:
            raise
        return current_rc

    @staticmethod
    def rolling_update(config, name, image=None, container_name=None, new_rc=None, wait_seconds=10):
        next_rc_suffix = '-next'
        partner_annotation = 'update-partner'
        replicas_annotation = 'desired-replicas'
        next_name = name + next_rc_suffix
        phase = 'init'
        next_exists = False
        next_rc = None

        try:
            current_rc = K8sReplicationController(config=config, name=name).get()
            current_exists = True
        except NotFoundException:
            raise NotFoundException('RollingUpdate: Current replication controller does not exist.')
        except:
            raise

        try:
            next_rc = K8sReplicationController(config=config, name=next_name).get()
            next_exists = True
        except NotFoundException:
            pass
        except:
            raise

        if current_exists and not next_exists:
            try:
                if new_rc is not None:
                    next_rc = new_rc
                    next_rc.add_annotation(k=replicas_annotation, v=next_rc.get_replicas())
                else:
                    next_rc = copy.deepcopy(current_rc)
                    next_rc.add_annotation(k=replicas_annotation, v=current_rc.get_replicas())
                    if container_name is not None:
                        next_rc.set_image(name=container_name, image=image)
                    else:
                        next_rc.set_image(name=name, image=image)
                next_rc.set_name(name=next_name)
                next_rc.add_pod_label(k='name', v=name)
                my_version = str(uuid.uuid4())
                next_rc.add_pod_label(k='rc_version', v=my_version)
                next_rc.set_selector(selector=dict(name=name, rc_version=my_version))
                next_rc.set_replicas(replicas=0)
                next_rc.set_pod_generate_name(mode=True, name=name)
                next_rc.create()
            except:
                raise
            try:
                current_rc.add_annotation(k=partner_annotation, v=next_name)
                current_rc.update()
            except:
                raise
            phase = 'rollout'
        elif next_exists and not current_exists:
            phase = 'rename'
        elif current_exists and next_exists:
            if not next_rc.get_annotation(k=replicas_annotation):
                try:
                    next_rc.add_annotation(k=replicas_annotation, v=current_rc.get_replicas())
                    next_rc.update()
                except:
                    raise
            phase = 'rollout'

        if phase == 'rollout':
            desired_replicas = next_rc.get_annotation(k=replicas_annotation)
            try:
                while next_rc.get_replicas() < int(desired_replicas):
                    next_replicas = next_rc.get_replicas() + 1
                    next_rc.set_replicas(replicas=next_replicas)
                    next_rc.update()
                    next_rc.wait_for_replicas(replicas=next_replicas, labels=next_rc.get_pod_labels())
                    time.sleep(wait_seconds)
                    if current_rc.get_replicas() > 0:
                        current_replicas = current_rc.get_replicas() - 1
                        current_rc.set_replicas(replicas=current_replicas)
                        current_rc.update()
                        current_rc.wait_for_replicas(replicas=current_replicas, labels=current_rc.get_pod_labels())
                if current_rc.get_replicas() > 0:
                    current_rc.set_replicas(replicas=0)
                    current_rc.update()
                    current_rc.wait_for_replicas(replicas=0, labels=current_rc.get_pod_labels())
            except:
                raise
            phase = 'rename'

        if phase == 'rename':
            try:
                current_rc.delete()
                current_rc = copy.deepcopy(next_rc)
                current_rc.set_name(name=name)
                current_rc.del_annotation(k=partner_annotation)
                current_rc.del_annotation(k=replicas_annotation)
                current_rc.create()
                next_rc.delete()
            except:
                raise

        return current_rc

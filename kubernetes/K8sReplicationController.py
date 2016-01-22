from kubernetes.K8sPodBasedObject import K8sPodBasedObject
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
        self.set_selector(selector=dict(name=name))
        if image is not None:
            self.model.add_container(K8sContainer(name=name, image=image).get_model())
            self.model.set_pod_name(name=name)
            my_version = str(uuid.uuid4())
            self.model.add_pod_label(k='rc_version', v=my_version)
            self.set_selector(selector=dict(name=name, rc_version=my_version))
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

    @staticmethod
    def resize(config, name, replicas):
        try:
            this_rc = K8sReplicationController(config=config, name=name).get()
            this_rc.set_replicas(replicas)
            this_rc.update()
        except:
            raise
        return this_rc

    @staticmethod
    def rolling_update(config, name, image, wait_seconds=10):
        next_rc_suffix = '-next'
        partner_annotation = 'update-partner'
        replicas_annotation = 'desired-replicas'
        next_name = name + next_rc_suffix
        phase = 'init'
        that_exist = False
        that_rc = None

        try:
            this_rc = K8sReplicationController(config=config, name=name).get()
            this_exist = True
        except NotFoundException:
            raise NotFoundException('RollingUpdate: Current replication controller does not exist.')
        except:
            raise

        try:
            that_rc = K8sReplicationController(config=config, name=next_name).get()
            that_exist = True
        except NotFoundException:
            pass
        except:
            raise

        if this_exist and not that_exist:
            try:
                that_rc = copy.deepcopy(this_rc)
                that_rc.set_name(name=next_name)
                that_rc.add_pod_label(k='name', v=name)
                my_version = str(uuid.uuid4())
                that_rc.add_pod_label(k='rc_version', v=my_version)
                that_rc.set_selector(selector=dict(name=name, rc_version=my_version))
                that_rc.add_annotation(k=replicas_annotation, v=this_rc.get_replicas())
                that_rc.set_replicas(replicas=0)
                that_rc.set_image(name=name, image=image)
                that_rc.set_pod_generate_name(mode=True, name=name)
                that_rc.create()
            except:
                raise
            try:
                this_rc.add_annotation(k=partner_annotation, v=next_name)
                this_rc.update()
            except:
                raise
            phase = 'rollout'
        elif that_exist and not this_exist:
            phase = 'rename'
        elif this_exist and that_exist:
            if not that_rc.get_annotation(k=replicas_annotation):
                try:
                    that_rc.add_annotation(k=replicas_annotation, v=this_rc.get_replicas())
                    that_rc.update()
                except:
                    raise
            phase = 'rollout'

        if phase == 'rollout':
            desired_replicas = that_rc.get_annotation(k=replicas_annotation)
            while that_rc.get_replicas() < int(desired_replicas):
                try:
                    that_next_replicas = that_rc.get_replicas() + 1
                    that_rc.set_replicas(replicas=that_next_replicas)
                    that_rc.update()
                    time.sleep(wait_seconds)
                    if this_rc.get_replicas() > 0:
                        this_next_replicas = this_rc.get_replicas() - 1
                        this_rc.set_replicas(replicas=this_next_replicas)
                        this_rc.update()

                except:
                    raise
            phase = 'rename'

        if phase == 'rename':
            try:
                this_rc.delete()
                this_rc = copy.deepcopy(that_rc)
                this_rc.set_name(name=name)
                this_rc.del_annotation(k=partner_annotation)
                this_rc.del_annotation(k=replicas_annotation)
                this_rc.create()
                that_rc.delete()
            except:
                raise

        return this_rc

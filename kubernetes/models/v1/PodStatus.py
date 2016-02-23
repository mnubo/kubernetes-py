from kubernetes.models.v1.BaseModel import BaseModel
from kubernetes.models.v1.ContainerStatus import ContainerStatus


class PodStatus(BaseModel):
    def __init__(self, model=None):
        BaseModel.__init__(self)
        if model is not None:
            assert isinstance(model, dict)
            self.model = model

    def get_pod_phase(self):
        return self.model.get('phase', None)

    def get_pod_conditions(self):
        return self.model.get('conditions', list())

    def get_message(self):
        return self.model.get('message', '')

    def get_reason(self):
        return self.model.get('reason', '')

    def get_host_ip(self):
        return self.model.get('hostIP', None)

    def get_pod_ip(self):
        return self.model.get('podIP', None)

    def get_start_time(self):
        return self.model.get('startTime', None)

    def get_container_statuses(self):
        my_list = list()
        model_list = self.model.get('containerStatuses', list())

        if len(model_list) > 0:
            for status in model_list:
                my_list.append(ContainerStatus(model=status))

        return my_list

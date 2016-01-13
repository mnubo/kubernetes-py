from . import Container


class PodSpec:
    def __init__(self, name=None, image=None):
        self.model = {
            "containers": [],
            "dnsPolicy": "Default",
            "restartPolicy": "Never",
            "volumes": []
        }
        if name is not None and image is not None:
            if not isinstance(name, str) or not isinstance(image, str):
                raise SyntaxError('Name and image should be strings.')
            base_container = Container(name=name, image=image)
            self.model['containers'].append(base_container)

    def get(self):
        return self.model

    def add_container(self, container=None):
        if container is None or not isinstance(container, Container):
            raise SyntaxError('container should be a container object.')
        else:
            self.model['spec']['containers'].append(container)
        return

    def add_host_volume(self, name=None, path=None):
        if (name is None or path is None) or (not isinstance(name, str) or not isinstance(path, str)):
            raise SyntaxError('name and path should be strings.')
        else:
            self.model['spec']['volumes'].append({
                "name": name,
                "source": {
                    "hostPath": {
                        "path": path
                    }
                }
            })
        return

    def set_active_deadline(self, seconds=None):
        if seconds is None or not isinstance(seconds, int):
            raise SyntaxError('seconds should be a positive integer.')
        self.model['spec']['activeDeadlineSeconds'] = seconds
        return

    def set_dns_policy(self, policy='Default'):
        if policy in ['Default', 'ClusterFirst']:
            self.model['spec']['dnsPolicy'] = policy
        else:
            raise SyntaxError('policy should be one of: Default, ClusterFirst')
        return

    def set_image_pull_secrets(self, name=None):
        if name is None or not isinstance(name, str):
            raise SyntaxError('name should be a string.')
        self.model['spec']['imagePullSecrets'] = dict(name=name)
        return

    def set_restart_policy(self, policy='Never'):
        if policy in ['Always', 'OnFailure', 'Never']:
            self.model['spec']['restartPolicy'] = policy
        else:
            raise SyntaxError('policy should be one of: Always, OnFailure, Never')

    def set_service_account(self, name=None):
        if name is None or not isinstance(name, str):
            raise SyntaxError('name should be a string.')
        self.model['spec']['serviceAccountName'] = name
        return

    def set_termination_grace_period(self, seconds=None):
        if seconds is None or not isinstance(seconds, int):
            raise SyntaxError('seconds should be a positive integer.')
        self.model['spec']['terminationGracePeriodSeconds'] = seconds
        return

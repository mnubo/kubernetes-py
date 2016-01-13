class Container:
    def __init__(self, name=None, image=None):
        if name is None or image is None:
            raise SyntaxError
        self.model = {
            "name": name,
            "image": image,
            "command": [],
            "args": [],
            "env": [],
            "imagePullPolicy": 'PullIfNotPresent',
            "ports": [],
            "privileged": False,
            "hostNetwork": False,
            "volumeMounts": []
        }

    def get(self):
        return self.model

    def add_port(self, container_port, host_port, protocol='TCP', name=None):
        if container_port > 0 and host_port > 0:
            if name is None:
                name = 'port{portnum}'.format(portnum=str(host_port))
            self.model['ports'].append({
                "containerPort": int(container_port),
                "hostPort": int(host_port),
                "protocol": protocol,
                "name": name
            })
        else:
            raise SyntaxError('container_port and host_port should be integers.')
        return

    def add_env(self, name=None, value=None):
        if name is None or value is None:
            raise SyntaxError('name and value should be strings.')
        else:
            self.model['env'].append({"name": name, "value": value})
        return

    def add_volume_mount(self, name=None, read_only=False, mount_path=None):
        if name is None or mount_path is None:
            raise SyntaxError('name and mount_path should be strings.')
        else:
            self.model['volumeMounts'].append({
                "name": name,
                "readOnly": read_only,
                "mountPath": mount_path
            })
        return

    def set_name(self, name=None):
        if name is None:
            raise SyntaxError('name should be a string.')
        else:
            self.model['name'] = name
        return

    def set_image(self, image=None):
        if image is None:
            raise SyntaxError('image should be a string.')
        else:
            self.model['image'] = image
        return

    def set_command(self, cmd=None):
        if cmd is None:
            cmd = []
        else:
            if not isinstance(cmd, list):
                raise SyntaxError('cmd should be a list.')
        self.model['command'] = cmd
        return

    def set_arguments(self, args=None):
        if args is None:
            args = []
        else:
            if not isinstance(args, list):
                raise SyntaxError('args should be a list.')
        self.model['args'] = args
        return

    def set_pull_policy(self, policy='IfNotPresent'):
        if not isinstance(policy, str):
            raise SyntaxError('Policy should be one of: Always, Never, IfNotPresent')
        if policy in ['Always', 'Never', 'IfNotPresent']:
            self.model['imagePullPolicy'] = policy
        else:
            raise SyntaxError
        return

    def set_privileged(self, mode=True):
        if not isinstance(mode, bool):
            raise SyntaxError('mode should be True or False')
        self.model['privileged'] = mode
        return

    def set_host_network(self, mode=True):
        if not isinstance(mode, bool):
            raise SyntaxError('mode should be True or False')
        self.model['hostNetwork'] = mode
        return

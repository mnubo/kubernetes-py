# kubernetes-py

[![Build Status](https://travis-ci.org/mnubo/kubernetes-py.svg?branch=master)](https://travis-ci.org/mnubo/kubernetes-py)
[![Coverage Status](https://coveralls.io/repos/github/mnubo/kubernetes-py/badge.svg?branch=master)](https://coveralls.io/github/mnubo/kubernetes-py?branch=master)

A python module to use Kubernetes. Currently based on the version 1 of the API.

Currently supported Kubernetes objects:

* ~/.kube/config
* Pod
* ReplicationController
* Secret
* Service

## Usage

Documentation is currently work in progress. Please find some code snippets to help understand how to use this module.

### Configuration

By default, the module attempts to load existing configuration from `~/.kube/config`. You are welcome to specify
another location from where to load a kubeconfig file.

Otherwise, kubeconfig parameters can be overridden piecemeal. Please see `K8sConfig.py` for more information.
    
    from kubernetes import K8sConfig
    
    # Defaults found in ~/.kube/config
    cfg_default = K8sConfig()
    
    # Defaults found in another kubeconfig file
    cfg_other = K8sConfig(kubeconfig='/path/to/kubeconfig')
    
    # Overriding the host, using basic auth
    cfg_basic = K8sConfig(kubeconfig=None, api_host=somehost:8888, auth=('basic_user', 'basic_passwd'))
    
    # Overriding the host, using certificates
    cfg_cert = K8sConfig(kubeconfig=None, api_host=somehost:8888, cert=('/path/to/cert.crt', '/path/to/cert.key'))
    
    # Overriding the host, using a Bearer token
    cfg_token = K8sConfig(kubeconfig=None, api_host=somehost:8888, token='50a2fabfdd276f573ff97ace8b11c5f4')


### Containers

This module uses the default container runtime.

Defining a container:

    from kubernetes import K8sContainer
    
    container = K8sContainer(name='redis', image='redis')
    container.add_port(container_port=6379, host_port=6379, name='redis')


### Pods

Creating a pod:

    from kubernetes import K8sPod
    
    pod = K8sPod(config=cfg_basic, name='redis')
    pod.add_container(container)
    pod.create()
    
Fetching a pod:

    from kubernetes import K8sPod
    
    pod = K8sPod(config=cfg_token, name='redis')
    pod.get()

Deleting a pod:

    from kubernetes import K8sPod
    
    pod = K8sPod(config=cfg_cert, name='redis')
    pod.delete()

### ReplicationController

Creating a replication controller:

    from kubernetes import K8sConfig
    from kubernetes import K8sReplicationController
    
    that_cfg = K8sConfig(api_host='somehost:8888')
    that_rc = K8sReplicationController(config=that_cfg, name='redis', image='library/redis:2', replicas=1)
    that_rc.create()

Fetching a replication controller:

    from kubernetes import K8sConfig
    from kubernetes import K8sReplicationController
    
    that_cfg = K8sConfig(api_host='somehost:8888')
    that_rc = K8sReplicationController(config=that_cfg, name='redis')
    that_rc.get()

Deleting a replication controller:

    from kubernetes import K8sConfig
    from kubernetes import K8sReplicationController
    
    that_cfg = K8sConfig(api_host='somehost:8888')
    that_rc = K8sReplicationController(config=that_cfg, name='redis')
    that_rc.get()
    that_rc.delete()

### Service

Creating a service:

    from kubernetes import K8sConfig
    from kubernetes import K8sService
    
    that_cfg = K8sConfig(api_host='somehost:8888')
    that_svc = K8sService(config=that_cfg, name='redis')\
        .add_port(name='redisport', port=31010, target_port='redisport')\
        .add_selector(selector=dict(name='redis'))\
        .set_cluster_ip('192.168.1.100')
    that_svc.create()

Fetching a service:

    from kubernetes import K8sConfig
    from kubernetes import K8sService
    
    that_cfg = K8sConfig(api_host='somehost:8888')
    that_svc = K8sService(config=that_cfg, name='redis')
    that_svc.get()

Deleting a service:

    from kubernetes import K8sConfig
    from kubernetes import K8sService
    
    that_cfg = K8sConfig(api_host='somehost:8888')
    that_svc = K8sService(config=that_cfg, name='redis')
    that_svc.get()
    that_svc.delete()

### Secret

Creating a secret:

    from kubernetes import K8sConfig
    from kubernetes import K8sSecret
    
    that_cfg = K8sConfig(api_host='somehost:8888')
    that_secret = K8sSecret(config=that_cfg, name='myregistry')\
        .set_dockercfg_secret(data='{"somehost":{"auth":"bW81Ym8fZG7ja2HyOmMvY2tlcmZvhm1UdWovMJIR",'
                                   '"email":"email@company.com"}}')
    that_secret.create()

Fetching a secret:

    from kubernetes import K8sConfig
    from kubernetes import K8sSecret
    
    that_cfg = K8sConfig(api_host='somehost:8888')
    that_secret = K8sSecret(config=that_cfg, name='myregistry')
    that_secret.get()

Deleting a secret:

    from kubernetes import K8sConfig
    from kubernetes import K8sSecret
    
    that_cfg = K8sConfig(api_host='somehost:8888')
    that_secret = K8sSecret(config=that_cfg, name='myregistry')
    that_secret.get()
    that_secret.delete()

### Unit tests

Development of features and unit tests was done against both a full Kubernetes cluster, as well as using 
the [minikube](https://github.com/kubernetes/minikube) tool. You will find a `./bin/minukube.sh` script in the 
source tree which fetches the application binary.

The unit tests which require making remote API calls check if there is a reachable API server; if no such endpoint
is found, the test is skipped. It is recommended to begin testing things out against `minikube`.

```
$ nosetests tests/
```

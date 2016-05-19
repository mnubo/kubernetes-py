# kubernetes-py

A python module to use Kubernetes. Currently based on the version 1 of the API.

Currently supported Kubernetes objects:

* Pod
* ReplicationController
* Secret
* Service

## Usage

Until proper documentation is made, please find some code snippets to help understand how to use this module.

### Pod

Creating a pod:

    from kubernetes import K8sConfig
    from kubernetes import K8sPod
    from kubernetes import K8sContainer
    
    that_cfg = K8sConfig(api_host='somehost:8888', auth=('basic_username', 'basic_passwd'))
    that_pod = K8sPod(config=that_cfg, name='redis')
    that_pod.add_container(container=K8sContainer(name='redis', image='library/redis:2')
                          .add_port(container_port=6379, host_port=31010, name='redismasterport'))
    that_pod.create()
    
Fetching a pod:

    from kubernetes import K8sConfig
    from kubernetes import K8sPod
    
    that_cfg = K8sConfig(api_host='somehost:8888', token='50a2fabfdd276f573ff97ace8b11c5f4')
    that_pod = K8sPod(config=that_cfg, name='redis')
    that_pod.get()

Deleting a pod:

    from kubernetes import K8sConfig
    from kubernetes import K8sPod
    
    that_cfg = K8sConfig(api_host='somehost:8888')
    that_pod = K8sPod(config=that_cfg, name='redis')
    that_pod.get()
    that_pod.delete()

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


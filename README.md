# kubernetes-py

[![pypi](http://img.shields.io/pypi/v/kubernetes-py.png)](https://pypi.python.org/pypi/kubernetes-py)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/kubernetes-py.svg)](https://pypi.python.org/pypi/kubernetes-py/)
[![License](https://img.shields.io/pypi/l/kubernetes-py.svg)](https://pypi.python.org/pypi/kubernetes-py/)
[![Build Status](https://github.com/mnubo/kubernetes-py/workflows/Python%20build%20and%20tests/badge.svg?branch=master)](https://github.com/mnubo/kubernetes-py/)
[![Coverage Status](https://coveralls.io/repos/github/mnubo/kubernetes-py/badge.svg?branch=master)](https://coveralls.io/github/mnubo/kubernetes-py?branch=master)

Kubernetes API bindings in Python.

```
**************************************** WARNING **************************************** 

The package has been renamed to kubernetes_py in version 1.10.7.1. Please update your 
code accordingly. This was based on a request backed by several users.

*****************************************************************************************
```

Run on our own on-prem and AWS Kubernetes clusters at `1.10.5`

Also unit tested on :
* Minikube at `1.10.7`
* Google GKE clusters at `1.6.4`

Currently supported Kubernetes objects:

* ~/.kube/config
* ComponentStatus
* Container
* CronJob
* DaemonSet
* Deployment
* HorizontalPodAutoscalers
* Job
* Namespace
* Node
* PersistentVolume
* PersistentVolumeClaim
* PetSet
* Pod
* ReplicaSet
* ReplicationController
* Secret
* Service
* ServiceAccount
* StatefulSet
* StorageClass
* Volume
* VolumeMount


## Installation

For a normal installation, simply run the following command.
```
pip install kubernetes-py
```

## Usage

Find some code snippets below to help understand how to use this module.


### Configuration

By default, the module attempts to load existing configuration from `~/.kube/config` or from a kubeconfig using 
the `KUBECONFIG` environment variable. It can also initialize automatically with `in-cluster` configurations.
You are welcome to specify another location if you so choose. 

Otherwise, individual configuration parameters can be overridden piecemeal. In this case you must 
specify `kubeconfig=None` when initializing a K8sConfig object; the `~/kube/.config` file 
takes precedence if it exists.
    
    from kubernetes_py import K8sConfig
    
    # Defaults found in ~/.kube/config
    cfg_default = K8sConfig()
    
    # Defaults found in another kubeconfig file
    cfg_other = K8sConfig(kubeconfig='/path/to/kubeconfig')
    
    # Overriding the host, using basic auth
    cfg_basic = K8sConfig(
        kubeconfig=None, 
        api_host=somehost:8888, 
        auth=('basic_user', 'basic_passwd')
    )
    
    # Overriding the host, using certificates
    cfg_cert = K8sConfig(
        kubeconfig=None, 
        api_host=somehost:8888, 
        cert=('/path/to/cert.crt', '/path/to/cert.key')
    )
    
    # Overriding the host, using a Bearer token
    cfg_token = K8sConfig(
        kubeconfig=None, 
        api_host=somehost:8888, 
        token='50a2fabfdd276f573ff97ace8b11c5f4'
    )


### Containers

This module assumes the default container runtime.

##### Defining a container:

    from kubernetes_py import K8sContainer
    
    container = K8sContainer(name='redis', image='redis:3.0.7')
    container.add_port(
        container_port=6379, 
        host_port=6379, 
        name='redis'
    )


### CronJobs

##### Creating a CronJob

    from kubernetes_py import K8sCronJob
    
    cj = K8sCronJob(
        config=cfg_cert,
        name='my-cronjob',
    )
    cj.schedule = '*/1 * * * *'
    cj.concurrency_policy = 'Forbid'
    cj.starting_deadline_seconds = 10
    cj.create()

##### Updating a CronJob

    from kubernetes_py import K8sCronJob
    
    cj = K8sCronJob(config=cfg_cert, name='my-cronjob').get()
    cj.suspend = True
    cj.update()
    
##### Deleting a CronJob

    from kubernetes_py import K8sCronJob
    
    cj = K8sCronJob(config=cfg_cert, name='my-cronjob').get()
    cj.delete()


### Deployments

##### Creating a Deployment:

    from kubernetes_py import K8sDeployment
    
    deployment = K8sDeployment(
        config=cfg_cert, 
        name='my-deployment',
        replicas=3
    )
    deployment.add_container(container)
    deployment.create()

##### Fetching a Deployment:

    from kubernetes_py import K8sDeployment
    
    deployment = K8sDeployment(config=cfg_cert, name='my-deployment')
    deployment.get()


##### Fetching all available Deployments:

    from kubernetes_py import K8sDeployment
    
    deployment = K8sDeployment(config=cfg_cert, name='my-deployment')
    deployment.list()


##### Updating a Deployment:

    from kubernetes_py import K8sDeployment, K8sContainer
    
    deployment = K8sDeployment(config=cfg_cert, name='my-deployment')
    container = K8sContainer(name='nginx', image='nginx:1.7.9')
    deployment.add_container(container)
    deployment.create()
    deployment.set_container_image(name='nginx', image='nginx:1.9.1')
    deployment.update()


##### Scaling a Deployment:

    from kubernetes_py import K8sDeployment, K8sContainer
    
    deployment = K8sDeployment(config=cfg_cert, name='my-deployment')
    container = K8sContainer(name='nginx', image='nginx:1.7.9')
    deployment.add_container(container)
    deployment.set_replicas(3)
    deployment.create()
    deployment.scale(10)


##### Deleting a Deployment:

    from kubernetes_py import K8sDeployment
    
    deployment = K8sDeployment(config=cfg_cert, name='my-deployment')
    deployment.delete()    


### Jobs

##### Creating a Job

    from kubernetes_py import K8sJob
    
    job = K8sJob(config=cfg_cert, name='my-job')
    job.parallelism = 10
    job.completions = 20
    job.create()
    
##### Updating a Job

    from kubernetes_py import K8sJob
    
    job = K8sJob(config=cfg_cert, name='my-job').get()
    job.parallelism = 5
    job.update()
    
##### Deleting a Job

    from kubernetes_py import K8sJob
    
    job = K8sJob(config=cfg_cert, name='my-job').get()
    job.delete()
    

### Persistent Volumes

##### Creating an AWS EBS Persistent Volume:

    from kubernetes_py import K8sPersistentVolume
    
    pv_aws = K8sPersistentVolume(
        config=cfg_cert, 
        name="my-aws_ebs", 
        type="awsElasticBlockStore"
    )
    pv_aws.fs_type = "xfs"
    pv_aws.volume_id = "vol-0a89cd040d534a371"
    pv_aws.create()

As [specified](https://kubernetes.io/docs/concepts/storage/volumes/#awselasticblockstore):
- the nodes on which pods are running must be AWS EC2 instances
- those instances need to be in the same region and availability-zone as the EBS volume
- EBS only supports a single EC2 instance mounting a volume

Pod creation will timeout waiting for readiness if not on AWS; unschedulable.


##### Creating a GCE PD Persistent Volume

    from kubernetes_py import K8sPersistentVolume
    
    pv_gce = K8sPersistentVolume(
        config=cfg_cert, 
        name="my-gce_pd", 
        type="gcePersistentDisk"
    )
    pv_gce.fs_type = "ext4"
    pv_gce.pd_name = "han-shot-first"
    pv_gce.create()

As [specified](https://kubernetes.io/docs/concepts/storage/volumes/#gcepersistentdisk):
- the nodes on which pods are running must be GCE VMs
- those VMs need to be in the same GCE project and zone as the PD

Pod creation will timeout waiting for readiness if not on GCE; unschedulable.


##### Creating an NFS Persistent Volume

    from kubernetes_py import K8sPersistentVolume
    
    pv = K8sPersistentVolume(
        config=cfg_cert,
        name="my-pv",
        type="nfs"
    )
    pv.nfs_server = "nfs.mycompany.com"
    pv.nfs_path = "/path/to/dir"
    pv.create()
    

### Persistent Volume Claims


##### Creating and Mounting a PersistentVolumeClaim

    from kubernetes_py import K8sContainer
    from kubernetes_py import K8sPersistentVolumeClaim
    from kubernetes_py import K8sPod
    from kubernetes_py import K8sVolume
    from kubernetes_py import K8sVolumeMount
    
    container = K8sContainer(name='nginx', image='nginx:1.9.1')
    
    pvc = K8sPersistentVolumeClaim(
        config=cfg_cert,
        name="my-pvc",
    )
    pvc.create()
    
    vol = K8sVolume(
        config=cfg_cert,
        name="my-volume",
        type="persistentVolumeClaim"
    )
    vol.claim_name = pvc.name
    
    mount = K8sVolumeMount(
        config=cfg_cert,
        name=vol.name,
        mount_path="/path/on/container"
    )
    container.add_volume_mount(mount)
    
    pod = K8sPod(
        config=cfg_cert,
        name="my-pod"
    )
    pod.add_volume(vol)
    pod.add_container(container)
    pod.create()


### Pods

##### Creating a Pod:

    from kubernetes_py import K8sPod
    
    pod = K8sPod(config=cfg_basic, name='redis')
    pod.add_container(container)
    pod.create()
    
##### Fetching a Pod:

    from kubernetes_py import K8sPod
    
    pod = K8sPod(config=cfg_token, name='redis')
    pod.get()
    
##### Fetching all available Pods:

    from kubernetes_py import K8sPod
    
    pod = K8sPod(config=cfg_token, name='redis')
    pod.list()

##### Deleting a Pod:

    from kubernetes_py import K8sPod
    
    pod = K8sPod(config=cfg_cert, name='redis')
    pod.delete()

### ReplicationController

##### Creating a ReplicationController:

    from kubernetes_py import K8sReplicationController
    
    rc = K8sReplicationController(
        config=cfg_cert, 
        name='redis', 
        image='redis:3.2.3', 
        replicas=1
    )
    rc.create()

##### Fetching a ReplicationController:

    from kubernetes_py import K8sReplicationController
    
    rc = K8sReplicationController(config=cfg_cert, name='redis')
    rc.get()
    
##### Fetching all available ReplicationControllers:

    from kubernetes_py import K8sReplicationController
    
    rc = K8sReplicationController(config=cfg_cert, name='redis')
    rc.list()    

##### Deleting a ReplicationController:

    from kubernetes_py import K8sReplicationController
    
    rc = K8sReplicationController(config=cfg_cert, name='redis')
    rc.delete()

### Service

##### Creating a service:

    from kubernetes_py import K8sService
    
    svc = K8sService(config=cfg_cert, name='redis')
    svc.add_port(name='redisport', port=31010, target_port='redisport')
    svc.add_selector(selector=dict(name='redis'))
    svc.set_cluster_ip('192.168.1.100')
    svc.create()

##### Fetching a service:

    from kubernetes_py import K8sService

    svc = K8sService(config=cfg_cert, name='redis')
    svc.get()

##### Deleting a service:

    from kubernetes_py import K8sService
    
    svc = K8sService(config=cfg_cert, name='redis')
    svc.delete()

### Secret

##### Creating a secret:

    from kubernetes_py import K8sSecret
    
    data = { "auths": {
                "repo:port": {
                    "auth": "authstring", 
                    "email": "you@company.com"
                }}}  
    
    secret = K8sSecret(config=cfg_cert, name='my-registry')
    secret.dockerconfigjson = data
    secret.create()
        
##### Fetching a secret:

    from kubernetes_py import K8sSecret

    secret = K8sSecret(config=cfg_cert, name='my-registry')
    secret.get()

##### Deleting a secret:

    from kubernetes_py import K8sSecret
    
    secret = K8sSecret(config=cfg_cert, name='my-registry')
    secret.delete()
    
### Volume

##### Mounting an AWS EBS volume inside a Pod:
    
    from kubernetes_py import K8sVolume
    
    volume = K8sVolume(
        config=cfg_cert,
        name='aws-volume',
        type='awsElasticBlockStore',
        mount_path='/path/inside/container'
    )
    volume.set_volume_id('vol-123456')  # this volume must already exist
    container.add_volume_mount(volume)
    pod.add_volume(volume)
    pod.add_container(container)
    pod.create()


## Unit tests

The unit tests that require making remote API calls check if there is a reachable API server; if no such endpoint
is found, the test is skipped. 

It is recommended to begin testing things out against `minikube`. However, be aware
that minikube does not support the entire feature set of a full Kubernetes install.

```
$ nosetests --with-coverage --cover-package=kubernetes_py
```

Please note that when using minikube, and Kubernetes in general, the default hosts are as below:

* `kubernetes`
* `kubernetes.default`
* `kubernetes.default.svc`
* `kubernetes.default.svc.cluster.local`

For certificate validation to succeed, you should edit your `~/.kube/config` to address one of the hosts, eg.:

    - cluster:
        certificate-authority: /Users/kubernetes/.minikube/ca.crt
        server: https://kubernetes:8443

Finally, add an entry to your `/etc/hosts` file for the host alias you choose.

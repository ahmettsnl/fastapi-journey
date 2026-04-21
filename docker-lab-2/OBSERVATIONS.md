# OBSERVATIONS

1. The difference between docker run and kubectl run is that docker run starts a container directly on the local machine, while kubectl run creates a pod inside a Kubernetes cluster. Kubernetes provides more control and management over containers.

2. In kubectl describe pod, the Scheduler is responsible for assigning the pod to a node. This corresponds to the kube-scheduler component in the Kubernetes control plane.

3. In the kube-system namespace, I observed components like:
- kube-apiserver: manages the cluster and handles API requests
- etcd: stores all cluster data

4. Alpine:
When I exited the pod, all changes were lost. This is because pods are temporary and containers do not persist data unless volumes are used.

5. After deleting the pod, Kubernetes did not restart it. This is because it was a standalone pod without a controller. If a Deployment was used, Kubernetes would automatically recreate the pod.
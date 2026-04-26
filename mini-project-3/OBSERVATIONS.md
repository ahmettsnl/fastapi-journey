1. What is the difference between a Pod and a Deployment? Why would you use a Deployment instead of a bare Pod?

A Pod is the smallest unit in Kubernetes and it usually runs one container. When I deployed the project, I saw that Pods are created automatically by Deployments. A Deployment is more useful because it manages Pods for you. For example, if a Pod crashes, Kubernetes automatically creates a new one. Also, when I scaled the application, the Deployment created multiple Pods easily, which would be difficult to manage manually with just Pods.

2. Why is a ConfigMap used for the MongoDB URL instead of hardcoding it in the Deployment YAML?

Using a ConfigMap makes the configuration more flexible. During the setup, I noticed that the MongoDB URL is stored separately and then used by the application. This means if the database address changes, I don’t need to edit the whole deployment file. It helps keep the application and configuration separate and easier to manage.

3. What happened to the original Pod when you scaled the WebApp to 3 replicas? Did it get replaced, or were new Pods added alongside it?

When I changed the replicas from 1 to 3, the original Pod stayed the same and two new Pods were created. I confirmed this by running kubectl get pods, and I could see three webapp Pods running at the same time. So Kubernetes did not replace the existing Pod, it added new ones.

4. What would happen to the application if the MongoDB Pod crashed? How would Kubernetes respond?

If the MongoDB Pod crashes, Kubernetes will automatically try to restart it because it is managed by a Deployment. From what I understood during the process, the system keeps the desired state, so it will recreate the Pod to keep the application working. There might be a short downtime, but it should recover automatically.

5. What is one thing that surprised you or that you found confusing? How did you resolve it?

One thing that confused me was that the Pods stayed in "ContainerCreating" status for a while after applying the YAML files. At first I thought something was wrong, but after checking with kubectl describe pod, I saw that the images were still being pulled. After waiting a bit, everything started running normally. So I learned that some delays are normal, especially during the first setup.
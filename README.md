# my-app
Time Spent: ~ 4h10min
1. Cluster Constructure Overview

    3 Nodes Cluster:

    Server(control-plane)
    |
    |——————Ingress Controller

    Agent1(workder1)
    |
    |——————Pods
        |
        |------foo-app-1
        |------foo-app-2

    Agent2(workder2)
    |
    |——————Pods
        |
        |------bar-app-1
        |------bar-app-2

    Network Services
    |
    |——————foo-service: Forward traffic on port 80 to foo pods
    |——————bar-service: Forward traffic on port 80 to bar pods
    |——————ingress
            |------ /foo ->foo-service:80
            |------ /bar ->bar-service:80

    Network Flow: 
    http://localhost/foo -> Ingress -> foo-service -> foo-pod
    http://localhost/bar -> Ingress -> bar-service -> bar-pod

2. Deployment 
    Enviroment preparation：
        K8s cluster enviroment (KinD or K3d)
        Kubectl configured
        Docker
    Deployment steps: 
    1) Cluster Initialization : manifests/k3d-confg.yaml
    2) Ingress Controller Installation: manifests/ingress-nginx.yaml
    3) Namespace Initialization: manifests/namespace.yaml
    4) Ingress Initialization: manifests/ingress.yaml
    5) Application and service  deployment: manifests/foo-deployment.yaml, manifests/bar-deployment.yaml
    6) After finishing the cluster deployment, run test commands [curl http://localhost/foo, curl http://localhost/bar]



    

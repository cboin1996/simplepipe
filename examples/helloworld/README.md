# Helloworld
## Run
1. Ensure that you have navigated to root directory of the project
2. Build the docker image using    
    ```shell 
    docker build /examples/helloworld/. -t helloworld
    ```
3. Load the image into your cluster using k3d command ```k3d image import```
    ```shell
    k3d image import helloworld -c simplepipe-cluster
4. Test running the image using docker, and observe the output displays correctly
    ```shell
    docker run helloworld
    ```
5. Submit the workflow using command 
    ```shell
    kubectl create -f examples/workflows/hello.yaml -n argo
    ```
6. Verify the workflow was submitted by checking the argoUI for a workflow with prefix simplepipe:
    - if you haven't already, open a second shell in the project and execute
        ```shell
        task argo:portfwd
        ```
    - this will port forward the argo server onto 2746. Launch https://localhost:2746 to view the interface.
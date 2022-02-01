# Instructions

1. Ensure that the Taskfile has been executed, and that a cluster has been created on your 
pc.  
    - If you haven't already, execute:
    ``shell
        task install
    ```
2. Ensure that you have navigated to the examples/helloworld directory within terminal.
2. Build the docker image using Docker build . -t helloworld
3. Test running the image, and observe the output displays correctly
4. Submit the workflow using command kubectl create -f workflows/hello.yml -n argo
5. Verify the workflow was submitted by checking the argoUI for a workflow with prefix simplepipe:
    - if you haven't already, open a second shell in the project and execute
        ```shell
            task argo:portfwd
        ```
    - this will port forward the argo server onto 2746. Launch https://localhost:2746 to view the interface.
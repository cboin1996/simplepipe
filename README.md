# simplepipe

Simple k8s monitoring with argo workflows and prometheus.
This application provides a cluster wide argo installation
with a few example namespaces that can submit workflows.

In addition, a per namespace push gateway is provided for pushing
metrics to prometheus. 

## Installation
See the [Taskfile.yml](Taskfile.yml) for installation commands.


## Examples

See the README.md in each example folder for how to run.

### Application examples:

- [helloworld](./images/helloworld/): A simple hello world python application.
- [simplepipe](./images/simplepipe/): An application that is capable of parsing metrics
    and pushing them to the push gateway.

### Workflow examples:

- [hello.yaml](./workflows/hello.yaml): Workflow associated with the [helloworld](./examples/helloworld/)
project.

- [simplepipe.yaml](./workflows/simplepipe.yaml): Workflow associated with a use case for metrics gathering using the 
simplepipe python package.

## [simplepipe](./simplepipe/) package
Python package wrapping the python prometheus client. This package is 
useful for gathering metrics from file or in memory and pushing
them to a prometheus gateway.


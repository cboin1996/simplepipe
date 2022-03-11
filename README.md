# simplepipe

Simple k8s monitoring with argo workflows and prometheus.

## Installation
See the [Taskfile.yml](Taskfile.yml) for installation commands.


## Examples

See the README.md in each example folder for how to run.

### Application examples:

- [helloworld](./examples/helloworld/): A simple hello world python application.

### Workflow examples:

- [hello.yaml](./examples/workflows/hello.yaml): Workflow associated with the [helloworld](./examples/helloworld/)
project.

- [simplepipe.yaml](./examples/workflows/simplepipe.yaml): Workflow associated with a use case for metrics gathering using the 
simplepipe python package

## [simplepipe](./simplepipe/) package
Python package wrapping the python prometheus client. This package is 
useful for gathering metrics from file, or from list objects and pushing
them to a prometheus gateway.

### [simple.py](./simple.py)

Trivial example of generating a metric to a file in the proper format
for simplepipe to push to the prometheus push gateway

### [weather.py](./weather.py)

Example of real time monitoring weather in guelph and pushing updates
to the push gateway


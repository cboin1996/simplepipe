# simplepipe

Simple k8s monitoring with argo workflows and prometheus.
This application provides a cluster wide argo installation
with a few example namespaces that can submit workflows.

In addition, a per namespace push gateway is provided for pushing
metrics to prometheus. 

## Installation
See the [Taskfile.yml](Taskfile.yml) for installation commands.

## Docs
A presentation is included for this repository: see [docs](./docs/).

The [Makefile](./docs/markdown-beamer-livereload/Makefile) can be launched to build
the presentation. For development, use ```make dev``` to enable live reloading as you edit
[content.md](./docs/content.md).

At the moment, the [assets](./docs/assets/) folder contains the flow diagrams referenced in 
the slides. These figures are manually captured from rendered .md files.

## Examples

See the README.md in each example folder for how to run.

### Application examples:

- [helloworld](./images/helloworld/): A simple hello world python application.
- [simplepipe](./images/simplepipe/): An application that is capable of parsing metrics
    and pushing them to the push gateway.
    - Run a workflow under the alice namespace: ```kubectl create -f workflows/simplepipe.yaml -n alice``` 

### Workflow examples:

- [hello.yaml](./workflows/hello.yaml): Workflow associated with the 
[helloworld](./examples/helloworld/) project.

- [simplepipe.yaml](./workflows/simplepipe.yaml): Workflow associated with a use 
case for metrics gathering using the simplepipe python package.

## [simplepipe](./images/simplepipe/simplepipe) package
Python package wrapping the python prometheus client. This package is 
useful for gathering metrics from file or in memory and pushing
them to a Prometheus Pushgateway.



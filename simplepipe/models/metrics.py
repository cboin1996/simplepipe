from enum import Enum
from typing import Generic, TypeVar, List
import prometheus_client

from pydantic.generics import GenericModel
from pydantic import parse_obj_as

from util import fileutil

class MetricTypeEnum(str, Enum):
    Gauge = "gauge"
    Summary = "summary"
    Histogram = "histogram"
    Info = "info"

TypeValue = TypeVar('TypeValue')
class Metric(GenericModel, Generic[TypeValue]):
    """Base type definition for a metric.
    """
    name: str
    description: str
    value: TypeValue
    metric_type: MetricTypeEnum
    
    def construct_as_prometheus(self, registry: prometheus_client.CollectorRegistry):
        """Construct a metric as a prometheus metric, adding it to the given registry

        Args:
            registry (prometheus_client.CollectorRegistry): the prometheus registry.
        """
        if self.metric_type == MetricTypeEnum.Gauge:
            g =  prometheus_client.Gauge(
                self.name,
                self.description,
                registry=registry
            )
            g.set(self.value)
            return g

        if self.metric_type == MetricTypeEnum.Summary:
            s =  prometheus_client.Summary(
                self.name,
                self.description,
                registry=registry
            )
            s.observe(self.value)
            return s

        if self.metric_type == MetricTypeEnum.Histogram:
            h = prometheus_client.Histogram(
                self.name,
                self.description,
                registry=registry
            )
            h.observe(self.value)

        if self.metric_type == MetricTypeEnum.Info:
            i = prometheus_client.Info(
                self.name,
                self.description,
                registry=registry
            )
            i.info(self.value)
        
class MetricCollector(object):
    """A class for collecting and pushing metrics to prometheus push gateway.

    The metrics collector is capable of parsing metrics in the following formats:
    - json array : [{"name": "example_metric",     
                       "description": "metric for example purposes",
                        "value": 0,
                        "metric_type": "gauge"}]
    The below examples assume you have the prometheus gateway installed in a local
    environment.
    Examples:
    - pushing from a file\n
        >>> collector = MetricCollector("http://localhost:9091")
        >>> collector.load_and_push(fp="./my_metrics.json", job_name="example_from_file")
    - pushing from a dictionary\n
        >>> metrics = [{"name": "example_metric",     
                       "description": "metric for example purposes",
                        "value": 0
                        "metric_type": "gauge"}]
        >>> collector = MetricCollector("http://localhost:9091")
        >>> collector.parse_and_push(metrics=metrics, job_name="example_from_dict")
    """
    def __init__(self, prometheus_push_gateway_ip: str) -> None:
        self.prometheus_push_gateway_ip = prometheus_push_gateway_ip 

    def load_and_push(self, fp: str, job_name: str):
        """Helper method for loading metrics from a file and pushing them 
        to the prometheus push gateway

        Args:
            fp (str): the filepath
            metric (List[Metric]): the list of Metric objects
            job_name (str): a name for the job associated with this push
        """
        metrics = load_metrics_from_file(fp)
        self.push_to_gateway(metrics=metrics, job_name=job_name)

    def parse_and_push(self, metrics: List[dict], job_name: str):
        metrics = load_metrics_from_file(fp)
        self.push_to_gateway(metrics=metrics, job_name=job_name)

    def push_to_gateway(self, metrics: List[Metric], job_name: str):
        """Push metrics to the prometheus gateway

        Args:
            metrics (List[Metric]): like of Metric objects
            job_name (str): a name for the job associated with this push
        """
        registry = prometheus_client.CollectorRegistry()
        for metric in metrics:
            metric.construct_as_prometheus(registry=registry)
            
        prometheus_client.push_to_gateway(self.prometheus_push_gateway_ip, 
                                          job=job_name, 
                                          registry=registry)

def load_metrics_from_file(fp: str):
    """Load metrics from a file at the given filepath.
    Note: the metrics from within this method should follow the structure of the 
    :class:`Metric <simplepipe.models.metrics.Metric>` class.

    Example:
        Currently, the supported metric format should be in the form of a json array, or python dict. 
        Here is an example of an integer metric of type gauge. 
        >>> metrics = [{"name": "example_metric",     
                       "description": "metric for example purposes",
                        "value": 0
                        "metric_type": "gauge"}]

    Args:
        fp (str): the filepath

    Raises:
        ValueError: if the file type is invalid/not supported, a value error is raised.

    Returns:
        List[Metric]: list of parsed Metric objects.
    """
    file_extension_str = fileutil.detect_filetype(fp)

    if fileutil.DataType.has_value(file_extension_str):
        extension = fileutil.DataType(file_extension_str)

        if extension == fileutil.DataType.JSON:
            metrics = fileutil.load_json_from_file(fp)
            return parse_metrics(metrics, fileutil.DataType.JSON)

    # no metrics were loaded, and thus the filetype must be invalid.
    raise ValueError(f"Invalid filetype! Filetype of '{file_extension_str}' is unsupported.")     

def parse_metrics(metrics, typ: fileutil.DataType):
    """Method for parsing metrics given a data type

    Args:
        metrics (object): the metrics to parse
        typ (fileutil.DataType): the data type which declares how to parsing should occur

    Returns:
        List[Metric]: the parsed list of metrics.
    """
    # can declare other types as they are implemented, with custom parsing 
    # per use case.
    if typ == fileutil.DataType.JSON:
        return parse_obj_as(List[Metric], metrics)

if __name__=="__main__":
    metrics = [{"name" : "test", "job": "testjob", "description": "this is a test job", "value": "6", "metric_type": "gauge"}]
    parsed = parse_obj_as(List[Metric], metrics)
    # print(parsed)

    for metric in parsed:
        print(metric.construct_as_prometheus())
    # print(BaseMetric[int](title="ree", job="ree", testjob="ree", description="ree", value=1))
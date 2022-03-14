from enum import Enum
import logging
from typing import Generic, TypeVar, List
import prometheus_client
import json
import os

from pydantic.generics import GenericModel
from pydantic import parse_obj_as

logger = logging.getLogger(__name__)

class DataType(str, Enum):
    """Enum for file types
    """
    JSON = ".json"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_ 

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
        """Helper method for parsing metrics in the following format and pushing them
        to the prometheus gateway:
        >>> metrics = [{"name": "example_metric",     
                "description": "metric for example purposes",
                "value": 0,
                "metric_type": "gauge"}]
        """
        metrics = parse_metrics(metrics, typ=DataType.JSON)
        self.push_to_gateway(metrics=metrics, job_name=job_name)

    def push_to_gateway(self, metrics: List[Metric], job_name: str):
        """Push metrics to the prometheus gateway

        Args:
            metrics (List[Metric]): like of Metric objects
            job_name (str): a name for the job associated with this push
        """
        registry = prometheus_client.CollectorRegistry()
        for metric in metrics:
            logger.info(f"Adding metric {metric} to registry.")
            metric.construct_as_prometheus(registry=registry)
        logger.info(f"Pushing metrics to registry at ip: {self.prometheus_push_gateway_ip}.")
        prometheus_client.push_to_gateway(self.prometheus_push_gateway_ip, 
                                          job=job_name, 
                                          registry=registry)
        logger.info(f"Success.")

def load_metrics_from_file(fp: str):
    """Load metrics from a file at the given filepath.
    Note: the metrics from within this method should follow the structure of the 
    :class:`Metric <simplepipe.models.metrics.Metric>` class.

    Example:
        Currently, the supported metric format should be in the form of a json array, or python dict. 
    Here is an example of an integer metric of type gauge.
    >>> metrics = [{"name": "example_metric",     
                    "description": "metric for example purposes",
                    "value": 0,
                    "metric_type": "gauge"}]

    Args:
        fp (str): the filepath

    Raises:
        ValueError: if the file type is invalid/not supported, a value error is raised.

    Returns:
        List[Metric]: list of parsed Metric objects.
    """
    logger.info(f"Attempting to load metrics from {fp}")
    file_extension_str = detect_filetype(fp)

    if DataType.has_value(file_extension_str):
        extension = DataType(file_extension_str)

        if extension == DataType.JSON:
            with open(fp, 'r') as f:
                metrics = json.load(f)
            parsed_metrics = parse_metrics(metrics, DataType.JSON)
            logger.info("Parsed metrics successully.")
            return parsed_metrics

    logger.info(f"Loading metrics from {fp} failed!")
    # no metrics were loaded, and thus the filetype must be invalid.
    raise ValueError(f"Invalid filetype! Filetype of '{file_extension_str}' is unsupported.")     

def parse_metrics(metrics, typ: DataType):
    """Method for parsing metrics given a data type

    Args:
        metrics (object): the metrics to parse
        typ (DataType): the data type which declares how to parsing should occur

    Returns:
        List[Metric]: the parsed list of metrics.
    """
    # can declare other types as they are implemented, with custom parsing 
    # per use case.
    if typ == DataType.JSON:
        return parse_obj_as(List[Metric], metrics)
    else:
        raise ValueError(f"Invalid type '{typ}' passed. Cannot parse metrics!")

def detect_filetype(fp: str) -> str:
    """Parses the file extension from a str path

    Args:
        fp (str): the path to the file

    Returns:
        str: the extension for the file.
    """

    if os.path.exists(fp):
        file_name, file_extension, = os.path.splitext(os.path.join(fp))
    else:
        raise ValueError(f"Path {fp} does not exist and thus file type cannot be determined!")

    return file_extension



if __name__=="__main__":
    metrics = [{"name" : "test", "job": "testjob", "description": "this is a test job", "value": "6", "metric_type": "gauge"}]
    parsed = parse_obj_as(List[Metric], metrics)
    # print(parsed)

    for metric in parsed:
        print(metric.construct_as_prometheus())
    # print(BaseMetric[int](title="ree", job="ree", testjob="ree", description="ree", value=1))
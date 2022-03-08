from models import metrics
import prometheus_client
from typing import List
import sys
from examples import simple
from util import logutil, dateutil
from config import env
"""
Entry point for push gateway application.
"""
def main(startup_args: List[str]):
    """Main method for loading the application.
    """
    startup_time = dateutil.get_time_now("YYYYmmdd_HH_mm_ss")
    logutil.set_logger_config_globally(startup_time)
    config = env.loader()

    # TODO: consider case where you can launch as an app with fp as cli arg.
    # Install argo workflows clusterwide with minio and postgres.
    metric_path = simple.main()
    collector = metrics.MetricCollector(prometheus_push_gateway_ip=config.push_gateway_hostname)
    collector.load_and_push(metric_path, 'simple')

if __name__=="__main__":
    main(sys.argv[1:])
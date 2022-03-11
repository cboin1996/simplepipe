import prometheus_client
from typing import List
import sys
import logging

from examples import simple
from util import logutil, dateutil
from config import env
from cli import parser
from models import metrics

"""
Entry point for push gateway application.
"""
def main(startup_args: List[str]):
    """Main method for loading the application.
    """
    startup_time = dateutil.get_time_now("YYYYmmdd_HH_mm_ss")
    logutil.set_logger_config_globally(startup_time)
    config = env.loader()
    logger = logging.getLogger(__name__)

    logger.info("Starting up.")
    parsed_args = parser.parse_args(startup_args)
    collector = metrics.MetricCollector(prometheus_push_gateway_ip=config.push_gateway_hostname)
    collector.load_and_push(parsed_args.mpath, parsed_args.jname)

if __name__=="__main__":
    main(sys.argv[1:])
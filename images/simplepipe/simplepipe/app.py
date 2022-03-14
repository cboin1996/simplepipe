import prometheus_client
from typing import List
import sys
import logging
import datetime
import argparse

from examples import simple
from config import env
from models import metrics

def set_logger_config_globally(timestamp: str) -> None:
    """Sets the python logging module settings for output
    to stdout and to file.

    Args:
        timestamp (str): the timestamp to name the log file.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )

def parse_args(args: list):
    """
    Command line parser for simplepipe.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("mpath", 
                        type=str,
                        help="The filepath to the metrics you wish to push to prometheus.")
    parser.add_argument("jname", 
                        type=str,
                        help="The name for the job associated with this metric push.")
    return parser.parse_args(args)
"""
Entry point for push gateway application.
"""
def main(startup_args: List[str]):
    """Main method for loading the application.
    """
    startup_time = datetime.datetime.now().strftime("YYYYmmdd_HH_mm_ss")
    set_logger_config_globally(startup_time)
    config = env.loader()
    logger = logging.getLogger(__name__)

    logger.info("Starting up.")
    parsed_args = parse_args(startup_args)
    collector = metrics.MetricCollector(prometheus_push_gateway_ip=config.push_gateway_hostname)
    collector.load_and_push(parsed_args.mpath, parsed_args.jname)

if __name__=="__main__":
    main(sys.argv[1:])
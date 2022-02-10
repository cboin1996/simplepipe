from metric import weather
import prometheus_client
from util import logutil, dateutil
from api.cli import parse
from typing import List
import sys
"""
Entry point for push gateway application.
"""
def main(startup_args: List[str]):
    """Main method for loading the application.
    """
    startup_time = dateutil.get_time_now("YYYYmmdd_HH_mm_ss")
    logutil.set_logger_config_globally(startup_time)
    parsed_args = parse.startup_parser(startup_args)
    # Registry for the job/any metrics for this push.
    registry = prometheus_client.CollectorRegistry()

    if parsed_args.mode == "dev":
        wm = weather.WeatherMonitor(registry, "http://localhost:9091")
    else:
        wm = weather.WeatherMonitor(registry, "http://prom-pushgw-prometheus-pushgateway.default:9091")
    wm.startup()
    wm.run()
    wm.shutdown()

if __name__=="__main__":
    main(sys.argv[1:])
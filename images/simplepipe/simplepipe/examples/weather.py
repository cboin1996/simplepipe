from xml.dom import NotFoundErr
from bs4 import BeautifulSoup
import prometheus_client
import requests
import time
import logging

logger = logging.getLogger(__name__)
class WeatherMonitor(object):
    """Simple synchronous weather monitor polling guelph's weather every
    30 seconds.
    """ 
    def __init__(self, gw_ip: str):
        logger.info("Initializing.")
        self.registry = prometheus_client.CollectorRegistry() # Registry for the job/any metrics.
        self.gw_ip = gw_ip
        self.state_enum = prometheus_client.Enum('weather_monitor_status', 'status of the weather monitor',
                                            states=['starting', 'running', 'stopped'], registry=self.registry)
        # CPU and RAM metrics through the process collector are passed to the registry for update upon push
        prometheus_client.ProcessCollector('weather_monitor_cpu_ram', registry=self.registry)
        self.continue_running = True
        logger.info("Initialized.")

    def startup(self):
        """Startup method.
        """
        logger.info("Starting up.")
        self.state_enum.state('starting')
        self.push_metrics()
        logger.info("Startup complete.")

    def run(self):
        """Run method. Runs indefinetely, pushing
        the temperature in guelph to prometheus.
        """
        logger.info("Running.")
        self.state_enum.state('running')
        while self.continue_running:
            try: 
                # Example of pushing a gauge type metric
                g = prometheus_client.Gauge('temperature_guelph', 
                                            'Temperature in guelph in celcius.', 
                                            registry=self.registry)
                g.set(self.get_temperature_guelph())
                self.push_metrics()
                time.sleep(30000)
            except NotFoundErr as nfe:
                logger.error(f"Caught exception {nfe}!", exc_info=1)
            except KeyboardInterrupt as kbe:
                logger.info(f"Keyboard interrupt recieved! Exiting run method.")
                self.continue_running = False
            except Exception as e:
                logger.exception(f"Caught exception {e}!", exc_info=1)

        logger.info("Exiting run method!")

    def shutdown(self):
        """Shutdown method, 
            allowing shutdown to be invoked externally or internally.
        """
        logger.info("Shutting down!")
        self.continue_running = False
        self.state_enum.state('stopped')
        self.push_metrics()
        logger.info("Shutdown complete!")

    def get_temperature_guelph(self) -> float:
        """Scrape the canadian government weather website 
        "https://weather.gc.ca/city/pages/on-5_metric_e.html"
        for the current day's temperature in Guelph, ON.
        Args:
            country_code (str): the country code (ca for canada, us for us).
            region (str): the province or state.
            city (str): the city.

        Returns:
            float: the temperature in celcius
        """
        url = "https://weather.gc.ca/city/pages/on-5_metric_e.html"

        # submit the request to the weather network
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            # temperature resides within a <span> tag, with class 'wxo-metric-hide'
            spans = soup.find_all('span', {'class': 'wxo-metric-hide'})
            temp_str = spans[0].get_text()
            temperature = temp_str.split("°C")[0]
            return temperature
        else:
            raise NotFoundErr(f"""Could not complete request! 
                                Server returned code: {response.status_code} with body:
                                {response.text}""")
    
    def push_metrics(self) -> None:
        """Push all metrics in the registry to the gateway, overriding jobs with same job and groupid.
        """
        prometheus_client.push_to_gateway(self.gw_ip, job="weather_monitor", registry=self.registry)

if __name__=="__main__":
    # No implementation here yet to run as a script yet.
    pass
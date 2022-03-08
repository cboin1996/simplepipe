import random
from util import fileutil
import sys, os

def main():
    """Simple example for mocking a data science workflow, 
    outputting a random integer into a metric mocking how 
    much data was processed.  

    Return : the file path to the generated metric file
    """
    integer = random.randint(1,100)

    metric_fp = os.path.join(sys.path[0], 'metric.json')
    metric = [{"name" : "simple", 
              "description": "generated random integer", "value": "6", "metric_type": "gauge"}]
    fileutil.write_json_to_file(metric_fp, metric)
    return metric_fp
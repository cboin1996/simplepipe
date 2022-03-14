import random
import json
import sys, os

def main():
    """Simple example for mocking a data science workflow, 
    outputting a random integer into a metric mocking how 
    much data was processed.  

    Return : the file path to the generated metric file
    """
    integer = random.randint(1,100)

    metric_fp = os.path.join(sys.path[0], 'metric.json')
    metrics = [{"name" : "simple", 
              "description": "generated random integer", "value": "6", "metric_type": "gauge"}]
    with open(fp, 'w') as f:
        f.write(json.dumps(metrics))
    return metric_fp
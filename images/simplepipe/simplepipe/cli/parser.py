import argparse

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
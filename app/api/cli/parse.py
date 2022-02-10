import argparse
from typing import List
def startup_parser(args: List[str]) -> argparse.Namespace:
    """Parse any arguments passed upon startup of the program.

    Args:
        args (list): list of arguments
    """
    parser = argparse.ArgumentParser(description="Simplepipe.")
    mode_choices = ['dev', 'prod']
    parser.add_argument("--mode", default="prod", choices=mode_choices, 
        metavar="M", 
        help=f"The mode to run the application in (choices are {mode_choices}. Defaults to prod.")
    parsed_args = parser.parse_args(args)
    return parsed_args
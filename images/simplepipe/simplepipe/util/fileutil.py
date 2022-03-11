from enum import Enum
import json
import os

def load_json_from_file(fp: str) -> dict:
    """Load json from a file at the given filepath

    Args:
        fp (str): the file path for the json file

    Returns:
        dict: a dictionary representation of the object
    """
    with open(fp, 'r') as f:
        dct = json.load(f)
    
    return dct

def write_json_to_file(fp: str, obj):
    """Write json to file.

    Args:
        fp (str): the filepath to write to including file name
        obj (dict): the dict object to convert and write
    """
    with open(fp, 'w') as f:
        f.write(json.dumps(obj))

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

class DataType(str, Enum):
    """Enum for file types
    """
    JSON = ".json"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_ 
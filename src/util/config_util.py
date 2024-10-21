""" Module for accessing the *.ini file. """


from configparser import ConfigParser


def get(*key_chain, config_path="src/api/app.ini"):
    """ Gets the value at a certain key or chain of keys inside the config file.
    Returns:
        any: The desired value.
    """
    config = ConfigParser()
    config.read(config_path)

    current_value = config
    for key in key_chain:
        current_value = current_value[key]

    return current_value

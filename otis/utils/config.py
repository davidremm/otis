import json
import os
import sys


class Config(object):

    def __init__(self, path):
        self.path = path

    def read_json_config(self):
        """
        Return json configuration.

        :return: dict
        """
        if os.path.isfile(self.path):
            with open(self.path, mode='r') as config_file:
                try:
                    return json.load(fp=config_file)
                except Exception as e:
                    print("Error reading config {0}. Exception: {1}".format(self.path, e))
                    sys.exit(1)
        else:
            print("Unable to find configuration file in path {0}.".format(self.path))
            sys.exit(1)

    def write_json_config(self, config):
        """
        Write json configuration.

        :param dict config: Configuration to write
        :return:
        """
        with open(self.path, mode='w') as config_file:
            try:
                return json.dump(
                    obj=config,
                    fp=config_file,
                    sort_keys=True,
                    indent=2,
                    separators=(',', ': ')
                )
            except Exception as e:
                print("Error writing config {0}. Exception: {1}".format(self.path, e))
                sys.exit(1)

import os
import sys

from otis.utils.config import Config


class List():

    def __init__(self, sub_parser):
        self._parser = sub_parser.add_parser('list')
        self._parser.set_defaults(func=self.list)

    def list(self, args):
        config_dir = os.getenv('OTIS_CONFIG_DIR')
        if not os.path.isdir(config_dir):
            print("Invalid config directory {0}".format(config_dir))
            sys.exit(1)
        config_path = os.path.join(config_dir, 'config.json')

        # get configuration
        config = Config(path=config_path).read_json_config()

        # no elevators configured
        if 'elevators' not in config or len(config['elevators']) == 0:
            print("No elevators configured.")
            sys.exit()

        # set state of elevators
        for elevator_id, elevator in config['elevators'].iteritems():
            if elevator['state'] == 'maintenance':
                print("Elevator {0} is in maintenance mode".format(elevator_id))
            elif elevator['state'] == 'stopped':
                print("Elevator {0} is available on floor {1}".format(elevator_id, elevator['cur_floor']))
            else:
                print("Elevator {0} is on floor {1} and headed {2}, temp_state {3}. Pickup locations {4}, dropoff locations {5}".format(
                    elevator_id,
                    elevator['cur_floor'],
                    elevator['state'],
                    elevator['temp_state'],
                    elevator['enter'],
                    elevator['exit']
                ))

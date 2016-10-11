import os
import sys

from otis.utils.config import Config


class Maintenance():

    def __init__(self, sub_parser):
        self._parser = sub_parser.add_parser('maintenance')
        self._build_arguments()
        self._parser.set_defaults(func=self.maintenance)

    def _build_arguments(self):
        self._parser.add_argument(
            '-e', '--elevator-id',
            dest='elevator_id',
            required=True,
            help='REQUIRED - Elevator id to put into maintenance mode'
        )

    def maintenance(self, args):
        """
        Place specified elevator in maintenance mode. If already in maintenance mode, set state back to stopped.

        :param args:
        :return:
        """
        config_dir = os.getenv('OTIS_CONFIG_DIR')
        if not os.path.isdir(config_dir):
            print("Invalid config directory {0}".format(config_dir))
            sys.exit(1)
        config_path = os.path.join(config_dir, 'config.json')

        # get configuration
        config_obj = Config(path=config_path)
        config = config_obj.read_json_config()

        # no elevators configured
        if 'elevators' not in config or len(config['elevators']) == 0:
            print("No elevators configured.")
            sys.exit()

        # invalid elevator id
        if args.elevator_id not in config['elevators']:
            print("Invalid elevator id. Elevator {0} doesn't exist".format(args.elevator_id))
            sys.exit(1)

        # place elevator in/out of maintenance mode
        if config['elevators'][args.elevator_id]['state'] == 'maintenance':
            config['elevators'][args.elevator_id]['state'] = 'stopped'
            print("Elevator {0} is now available".format(args.elevator_id))
        else:
            config['elevators'][args.elevator_id]['state'] = 'maintenance'
            config['elevators'][args.elevator_id]['floors'] = []
            print("Elevator {0} is now in maintenance mode".format(args.elevator_id))
        config_obj.write_json_config(config=config)

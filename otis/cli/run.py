import os
import sys

from otis.elevator import Elevator
from otis.utils.config import Config


class Run():

    def __init__(self, sub_parser):
        self._parser = sub_parser.add_parser('run')
        self._build_arguments()
        self._parser.set_defaults(func=self.run)

    def _build_arguments(self):
        self._parser.add_argument(
            '-l', '--location',
            dest='location',
            required=False,
            help='OPTIONAL - Current floor'
        )
        self._parser.add_argument(
            '-d', '--destination',
            dest='destination',
            required=False,
            help='OPTIONAL - Desired floor'
        )

    def run(self, args):
        """
        Run elevators. If a location and destination are give, determine which elevator is best for the
        user to enter. Each elevator then run one 'turn'.

        :param args: Command line args.
        :return:
        """
        if args.location and not args.destination or args.destination and not args.location:
            print("--location and --destination must be used together")
            sys.exit(1)

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

        # find the best elevator for the user to enter
        if args.location and args.destination:
            print("User requests an elevator from floor {0} to {1}".format(args.location, args.destination))
            self.find_best_elevator(
                location=int(args.location),
                destination=int(args.destination),
                elevators=config['elevators'],
                up_enter_queue=config['up_enter_queue'],
                up_exit_queue=config['up_exit_queue'],
                down_enter_queue=config['down_enter_queue'],
                down_exit_queue=config['down_exit_queue']
            )

        # allow each elevator to make one step
        for elevator_id, elevator in config['elevators'].iteritems():
            elevator_obj = Elevator(
                id=elevator_id,
                state=elevator['state'],
                temp_state=elevator['temp_state'],
                cur_floor=elevator['cur_floor'],
                enter_list=elevator['enter'],
                exit_list=elevator['exit']
            )
            elevator_obj.step(
                up_enter_queue=config['up_enter_queue'],
                up_exit_queue=config['up_exit_queue'],
                down_enter_queue=config['down_enter_queue'],
                down_exit_queue=config['down_exit_queue']
            )
            self.update_state(config, elevator_obj)

        # write state to config
        config_obj.write_json_config(config=config)

    @staticmethod
    def find_best_elevator(location, destination, elevators, up_enter_queue, up_exit_queue, down_enter_queue, down_exit_queue):
        """
        Determine the best elevator for the user to enter and update the elevators list of unique floors.

        :param int location: Users location
        :param int destination: Users desired destination
        :param dict elevators: Elevators
        :param list up_queue: Users waiting to go up
        :param list down_queue: Users waiting to go down
        :return:
        """
        min_wait = None
        best_elevator_id = None
        user_direction = "up" if location < destination else "down"
        for elevator_id, elevator in elevators.iteritems():
            # skip broken elevators
            if elevator['state'] == "maintenance":
                continue

            # both headed up
            if elevator['state'] == "up" and user_direction == "up" and elevator['temp_state'] == "":
                # elevator is below user and (no min yet or if this elevator is closer than previous best)
                if elevator['cur_floor'] <= location and (not min_wait or location - elevator['cur_floor'] < min_wait):
                    min_wait = location - elevator['cur_floor']
                    best_elevator_id = elevator_id

            # both headed down
            elif elevator['state'] == "down" and user_direction == "down" and elevator['temp_state'] == "":
                if elevator['cur_floor'] >= location and (not min_wait or elevator['cur_floor'] - location < min_wait):
                    min_wait = elevator['cur_floor'] - location
                    best_elevator_id = elevator_id
            else:
                # this user is not convenient to pickup, continue looking
                continue

            # cannot do better, stop looking
            if min_wait == 0:
                break

        # add floor to elevators floors
        if best_elevator_id:
            print("User should take elevator {0}".format(best_elevator_id))
            if location not in elevators[best_elevator_id]['enter']:
                elevators[best_elevator_id]['enter'].append(location)
            if destination not in elevators[best_elevator_id]['exit']:
                elevators[best_elevator_id]['exit'].append(destination)
        else:
            # add user to queue
            if location < destination:
                up_enter_queue.append(location)
                up_exit_queue.append(destination)
            elif location > destination:
                down_enter_queue.append(location)
                down_exit_queue.append(destination)
            else:
                # location == destination, nothing to do
                pass

    def update_state(self, config, elevator_obj):
        """
        Update elevator state in configuration.

        :param dict config: Configuration
        :param Elevator elevator_obj: Elevator obj
        :return:
        """
        elevator = config['elevators'][elevator_obj.id]
        elevator['state'] = elevator_obj.state
        elevator['temp_state'] = elevator_obj.temp_state
        elevator['cur_floor'] = elevator_obj.cur_floor
        elevator['enter'] = elevator_obj.enter_list
        elevator['exit'] = elevator_obj.exit_list

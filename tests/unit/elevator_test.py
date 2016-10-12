from otis.elevator import Elevator
from tests import unittest


class TestElevator(unittest.TestCase):

    def test_step(self):
        # next step is our stop
        elevator = Elevator(
            id=1,
            state='up',
            temp_state='',
            cur_floor=4,
            enter_list=[],
            exit_list=[5]
        )
        elevator.step(
            up_enter_queue=[],
            up_exit_queue=[],
            down_enter_queue=[],
            down_exit_queue=[]
        )
        # elevator finished all stops
        assert elevator.state == "stopped"

        # broken elevator
        elevator = Elevator(
            id=1,
            state='maintenance',
            temp_state='',
            cur_floor=0,
            enter_list=[],
            exit_list=[]
        )
        elevator.step(
            up_enter_queue=[],
            up_exit_queue=[],
            down_enter_queue=[],
            down_exit_queue=[]
        )
        # elevator shouldn't move
        assert elevator.cur_floor == 0

        # new user in up queue
        up_enter_queue = [0]
        up_exit_queue = [5]
        elevator = Elevator(
            id=1,
            state='stopped',
            temp_state='',
            cur_floor=0,
            enter_list=[],
            exit_list=[]
        )
        elevator.step(
            up_enter_queue=up_enter_queue,
            up_exit_queue=up_exit_queue,
            down_enter_queue=[],
            down_exit_queue=[]
        )
        # pickup user, move one floor
        assert elevator.state == "up"
        assert elevator.cur_floor == 1
        assert len(up_enter_queue) == 0 and len(up_exit_queue) == 0

        # new user in down queue
        down_enter_queue = [5]
        down_exit_queue = [0]
        elevator = Elevator(
            id=1,
            state='stopped',
            temp_state='',
            cur_floor=0,
            enter_list=[],
            exit_list=[]
        )
        elevator.step(
            up_enter_queue=[],
            up_exit_queue=[],
            down_enter_queue=down_enter_queue,
            down_exit_queue=down_exit_queue
        )
        # temp move up
        assert elevator.temp_state == "up"
        assert elevator.state == "down"
        assert elevator.cur_floor == 1
        assert len(up_enter_queue) == 0 and len(up_exit_queue) == 0

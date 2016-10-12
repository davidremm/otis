from otis.elevator import Elevator
from tests import unittest


class TestElevator(unittest.TestCase):

    def test_step(self):
        # next step is our stop
        elevator = Elevator(
            id=1,
            state='up',
            cur_floor=4,
            enter_list=[],
            exit_list=[5]
        )
        elevator.step([], [])
        assert elevator.state == "stopped"

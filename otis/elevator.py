STATES = ["stopped", "up", "down", "maintenance"]


class Elevator(object):

    def __init__(self, id, state, cur_floor, floors):
        """
        :param int id: Elevator id
        :param str state: Elevator state
        :param int cur_floor: Current floor
        :param list floors: Unique floor destinations
        """
        self.id = id
        self.state = state
        self.cur_floor = cur_floor
        self.floors = floors

    def step(self):
        """
        Elevator can make one move (if any are required)
        """
        # elevator is broken
        if self.state == "maintenance":
            print("Elevator {0} is maintenance mode and is not operational".format(self.id))
            return
        # elevator is available
        if len(self.floors) == 0 and self.state == "stopped":
            print("Elevator {0} is available on floor {1}".format(self.id, self.cur_floor))
            return

        # take a 'step' and determine next cur_floor
        if self.state == "up":
            self.cur_floor += 1
        else:
            self.cur_floor -= 1

        # determine next stop
        next_stop = self.floors[0] if self.state == "up" else self.floors[len(self.floors) - 1]

        if self.cur_floor == next_stop:
            print("Elevator {0} has arrived to floor {1}".format(self.id, self.cur_floor))

            # remove floor from list of floors
            self.floors.remove(self.cur_floor)

            # elevator is now available
            if len(self.floors) == 0:
                self.state = "stopped"
        else:
            print("Elevator {0} is headed {1} to floor {2}".format(self.id, self.state, next_stop))

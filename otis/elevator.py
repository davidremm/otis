STATES = ["stopped", "up", "down", "maintenance"]


class Elevator(object):

    def __init__(self, id, state, temp_state, cur_floor, enter_list, exit_list):
        """
        :param int id: Elevator id
        :param str state: Elevator state
        :param str temp_state: Elevator temp up or down for pickup
        :param int cur_floor: Current floor
        :param list enter: Unique pickup floors
        :param list exit: Unique destination floors
        """
        self.id = id
        self.state = state
        self.temp_state = temp_state
        self.cur_floor = cur_floor
        self.enter_list = enter_list
        self.exit_list = exit_list

    def step(self, up_enter_queue, up_exit_queue, down_enter_queue, down_exit_queue):
        """
        Elevator can make one move (if any are required)

        :param list up_queue: Users waiting to go up
        :param list down_queue: Users waiting to go down
        """
        # elevator is broken
        if self.state == "maintenance":
            print("Elevator {0} is maintenance mode and is not operational".format(self.id))
            return
        if self.state != "stopped":
            print("Elevator {0} is on floor {1}".format(self.id, self.cur_floor))

        # elevator is available
        if len(self.enter_list) == 0 and len(self.exit_list) == 0 and self.state == "stopped":
            # check if a users is waiting to go up or down
            if len(up_enter_queue) > 0:
                print("User should take elevator {0}".format(self.id))
                self.enter_list.append(up_enter_queue[0])
                self.exit_list.append(up_exit_queue[0])
                self.state = "up" if up_enter_queue[0] >= self.cur_floor else "down"
                # user is going up, but elevator goes down to pickup
                if self.state == "down":
                    self.temp_state = "down"
                    self.state = "up"
                up_enter_queue.pop(0)
                up_exit_queue.pop(0)
            elif len(down_enter_queue) > 0:
                print("User should take elevator {0}".format(self.id))
                self.enter_list.append(down_enter_queue[0])
                self.exit_list.append(down_exit_queue[0])
                self.state = "up" if down_enter_queue[0] >= self.cur_floor else "down"
                # user is going down, but elevator goes down to pickup
                if self.state == "up":
                    self.temp_state = "up"
                    self.state = "down"
                down_enter_queue.pop(0)
                down_exit_queue.pop(0)
            else:
                print("Elevator {0} is available on floor {1}".format(self.id, self.cur_floor))
                return

        # check if we are picking someone up
        if self.cur_floor in self.enter_list:
            # remove floor from list of floors
            self.enter_list.remove(self.cur_floor)
            # if temporary state is set, unset it
            if self.temp_state != "":
                self.temp_state = ""
            print("Elevator {0} is picking up users on floor {1}".format(self.id, self.cur_floor))

        # take a 'step' and determine next cur_floor
        if self.temp_state == "up":
            self.cur_floor += 1
        elif self.temp_state == "down":
            self.cur_floor -= 1
        elif self.temp_state == "" and self.state == "up":
            self.cur_floor += 1
        elif self.temp_state == "" and self.state == "down":
            self.cur_floor -= 1

        # check if we are dropping someone off
        if self.cur_floor in self.exit_list:
            self.exit_list.remove(self.cur_floor)
            print("Elevator {0} is dropping users off on floor {1}".format(self.id, self.cur_floor))

        # elevator is now available
        if len(self.enter_list) == 0 and len(self.exit_list) == 0:
            self.state = "stopped"
        # else:
        #     # next_stop = self.cur_floor + 1 if self.state == "up" else self.cur_floor - 1
        #     print("Elevator {0} is on floor {1}".format(self.id, self.cur_floor))

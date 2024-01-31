from enum import IntEnum
import random
import itertools

##############


class Orientation(IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    # this allows things like: Orientation.NORTH + 1 == Orientation.EAST
    def __add__(self, i):
        orientations = list(Orientation)
        return orientations[(int(self) + i) % 4]

    def __sub__(self, i):
        orientations = list(Orientation)
        return orientations[(int(self) - i) % 4]

##############


class State:
  # Note, that you do not necessarily have to use this class if you find a
  # different data structure more useful as state representation.

  # TODO: add other attributes that store necessary information about a state of the environment
  #       Only information that can change over time should be kept here.

    def __init__(self, turned_on, position, orientation, dirts):
        # TODO: add other attributes that store necessary information about a state of the environment
        self.turned_on = turned_on
        self.position = position
        self.orientation = orientation
        self.dirts = dirts
        return

    def __str__(self):
        # TODO: modify as needed
        return f"State({self.turned_on}, {self.position}, {self.orientation}, {self.dirts})"

    def __hash__(self):
        # TODO: modify as needed
        return hash(str(self))

    def __eq__(self, other):
        # TODO: modify as needed
        # compare every  attribute to the other
        return (self.turned_on == other.turned_on) and (self.position == other.position) and (self.orientation == other.orientation) and (self.dirts == other.dirts)


##############

class Environment:
  # TODO: add other attributes that store necessary information about the environment
  #       Information that is independent of the state of the environment should be here.

    def __init__(self, width, height, nb_dirts):
        self._width = width
        self._height = height
        # TODO: randomly initialize an environment of the given size
        # That is, the starting position, orientation and position of the dirty cells should be (somewhat) random.
        # for example as shown here:
        # generate all possible positions
        all_positions = list(itertools.product(
            range(1, self._width+1), range(1, self._height+1)))  # (1, 1)
        # randomly choose a home location
        self.home = random.choice(all_positions)
        # randomly choose locations for dirt
        self.dirts = tuple(random.sample(all_positions, nb_dirts))
        return

    def get_initial_state(self):
        # TODO: return the initial state of the environment
        return State(False, self.home, Orientation.NORTH, self.dirts)

    def get_legal_actions(self, state):
        actions = []
        # TODO: check conditions to avoid useless actions
        if not state.turned_on:
            actions.append("TURN_ON")
        else:  # if turned on
            if state.position == self.home:  # only possible if robot is back to the home position
                actions.append("TURN_OFF")
            if state.position in state.dirts:  # should be only possible if there is dirt in the current position
                actions.append("SUCK")

            # For GO movement, check if will bump into wall
            if state.orientation == Orientation.NORTH:
                if state.position[1] < self._height:
                    actions.append("GO")
            if state.orientation == Orientation.SOUTH:
                if state.position[1] > 1:
                    actions.append("GO")
            if state.orientation == Orientation.EAST:
                if state.position[0] < self._width:
                    actions.append("GO")
            if state.orientation == Orientation.WEST:
                if state.position[0] > 1:
                    actions.append("GO")

            actions.append("TURN_LEFT")
            actions.append("TURN_RIGHT")
        return actions

    def get_next_state(self, state, action):
        # TODO: add missing actions
        if action == "TURN_ON":
            return State(True, state.position, state.orientation, state.dirts)
        elif action == "TURN_OFF":
            return State(False, state.position, state.orientation, state.dirts)
        elif action == "SUCK":
            new_dirts = tuple(
                filter(lambda x: x != state.position, state.dirts))
            return State(state.turned_on, state.position, state.orientation, new_dirts)
        elif action == "TURN_RIGHT":
            return State(state.turned_on, state.position, state.orientation + 1, state.dirts)
        elif action == "TURN_LEFT":
            return State(state.turned_on, state.position, state.orientation - 1, state.dirts)
        elif action == "GO":
            if state.orientation == Orientation.NORTH:
                return State(state.turned_on, (state.position[0], state.position[1] + 1), state.orientation, state.dirts)
            elif state.orientation == Orientation.SOUTH:
                return State(state.turned_on, (state.position[0], state.position[1] - 1), state.orientation, state.dirts)
            elif state.orientation == Orientation.EAST:
                return State(state.turned_on, (state.position[0] + 1, state.position[1]), state.orientation, state.dirts)
            else:
                return State(state.turned_on, (state.position[0] - 1, state.position[1]), state.orientation, state.dirts)

            return State(state.turned_on, state.position)
        else:
            raise Exception("Unknown action %s" % str(action))

    def get_cost(self, state, action):
        # TODO: return correct cost of each action
        if action == "TURN_OFF" and state.position == self.home and len(state.dirts):
            return 1 + 50 * len(state.dirts)
        elif action == "TURN_OFF" and state.position != self.home and len(state.dirts):
            return 100 + 50 * len(state.dirts)
        elif action == "SUCK" and (state.position in state.dirts):
            return 1
        elif action == "SUCK" and (state.position not in state.dirts):
            return 5
        return 1

    def is_goal_state(self, state):
        # TODO: correctly implement the goal test
        # We are home, turned off
        return not state.turned_on and state.position == self.home and len(state.dirts) == 0

##############


def expected_number_of_states(width, height, nb_dirts):
    # TODO: return a reasonable upper bound on number of possible states
    size = width * height
    return (4 * size * (2 ** nb_dirts)) + (4 * 2 ** nb_dirts)

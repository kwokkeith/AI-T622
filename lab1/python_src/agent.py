import random

#############

"""Agent acting in some environment"""
class Agent(object):

  def __init__(self):
    return

  # this method is called on the start of the new environment
  # override it to initialise the agent
  def start(self):
    print("start called")
    return

  # this method is called on each time step of the environment
  # it needs to return the action the agent wants to execute as as string
  def next_action(self, percepts):
    print("next_action called")
    return "NOOP"

  # this method is called when the environment has reached a terminal state
  # override it to reset the agent
  def cleanup(self, percepts):
    print("cleanup called")
    return

#############

class MyAgent(Agent):
    def __init__(self):
        self.turned_on = False
        self.position = (0, 0)
        self.walls_found = 0
        self.grid_size = 0
        self.home = (0, 0)
        self.orientation = 0
        self.visited = {self.home}
        self.x_min, self.x_max, self.y_min, self.y_max = None, None, None, None
        self.bump = 0

    def next_action(self, percepts):
        """
        TURN_ON,
        TURN_OFF,
        GO,
        SUCK,
        TURN_RIGHT,
        TURN_LEFT
        """
        print(f"Percepts: {percepts}")


        if not self.turned_on:
            self.turned_on = True
            return "TURN_ON"

        if "DIRT" in percepts:
            return "SUCK"

        if "BUMP" in percepts:
            # Move the robot back by one in its orientation
            if self.orientation == 0:
                self.position = (self.position[0], self.position[1] - 1)
            elif self.orientation == 1:
                self.position = (self.position[0] - 1, self.position[1])
            elif self.orientation == 2:
                self.position = (self.position[0], self.position[1] + 1)
            else:
                self.position = (self.position[0] + 1, self.position[1])

            self.bump += 1
            # If BUMP = 2, means we reach the NE corner
            if self.bump == 2:
                self.x_max, self.y_max = self.position[0], self.position[1]
            # If BUMP = 4, means reach the SW corner
            elif self.bump == 4:
                self.x_min, self.y_min = self.position[0], self.position[1]
                # Calculate size of grid
                self.grid_size = (self.y_max - self.y_min + 1) * (self.x_max - self.x_min + 1)
            self.turn_right()
            return "TURN_RIGHT"

        # Push the position in the grid into the visited set
        self.visited.add(self.position)

        # IF all the grid is cleaned
        if len(self.visited) >= self.grid_size and self.grid_size > 0:
            # Get robot to return to its original position
            if self.position[0] < 0:
                if self.orientation == 2:
                    self.turn_left()
                    return "TURN_LEFT"
                if self.orientation != 1:
                    self.turn_right()
                    return "TURN_RIGHT"
                self.move(self.orientation)
                return "GO"
            elif self.position[0] > 0:
                if self.orientation == 0:
                    self.turn_left()
                    return "TURN_LEFT"
                if self.orientation != 3:
                    self.turn_right()
                    return "TURN_RIGHT"
                self.move(self.orientation)
                return "GO"
            elif self.position[1] < 0:
                if self.orientation == 1:
                    self.turn_left()
                    return "TURN_LEFT"
                if self.orientation != 0:
                    self.turn_right()
                    return "TURN_RIGHT"
                self.move(self.orientation)
                return "GO"
            elif self.position[1] > 0:
                if self.orientation == 3:
                    self.turn_left()
                    return "TURN_LEFT"
                if self.orientation != 2:
                    self.turn_right()
                    return "TURN_RIGHT"
                self.move(self.orientation)
                return "GO"
            elif (self.position[0], self.position[1]) == (0, 0):
                self.turned_on = False
                return "TURN_OFF"

        # If already mapped the grid
        if self.bump == 5:
            if self.position[0] == self.x_max - 1:
                self.bump += 1
                self.x_max -= 1
                self.turn_right()
                return "TURN_RIGHT"
        if self.bump > 5:
            # NORTH or SOUTH
            if self.orientation == 0:
                if self.position[1] == self.y_max - 1:
                    self.y_max -= 1
                    self.turn_right()
                    return "TURN_RIGHT"
            if self.orientation == 2:
                if self.position[1] == self.y_min + 1:
                    self.y_min += 1
                    self.turn_right()
                    return "TURN_RIGHT"
            # WEST or EAST
            if self.orientation == 1:
                if self.position[0] == self.x_max - 1:
                    self.x_max -= 1
                    self.turn_right()
                    return "TURN_RIGHT"
            if self.orientation == 3:
                if self.position[0] == self.x_min + 1:
                    self.x_min += 1
                    self.turn_right()
                    return "TURN_RIGHT"

        self.move(self.orientation)
        return "GO"

    def turn_left(self):
        self.orientation = (self.orientation - 1) % 4

    def turn_right(self):
        self.orientation = (self.orientation + 1) % 4

    def move(self, orientation, step=1):
        match orientation:
            case 0:
                self.position = (self.position[0], self.position[1] + step)
            case 1:
                self.position = (self.position[0] + step, self.position[1])
            case 2:
                self.position = (self.position[0], self.position[1] - step)
            case 3:
                self.position = (self.position[0] - step, self.position[1])

    def cleanup(self, percepts):
        print("cleanup called")
        self.turned_on = False
        return "TURN_OFF"




"""A random Agent for the VacuumCleaner world

 RandomAgent sends actions uniformly at random. In particular, it does not check
 whether an action is actually useful or legal in the current state.
 """
class RandomAgent(Agent):

  def next_action(self, percepts):
    print("perceiving: " + str(percepts))
    actions = ["TURN_ON", "TURN_OFF", "TURN_RIGHT", "TURN_LEFT", "GO", "SUCK"]
    action = random.choice(actions)
    print("selected action: " + action)
    return action

#############

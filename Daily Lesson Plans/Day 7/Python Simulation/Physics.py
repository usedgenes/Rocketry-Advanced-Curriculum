import numpy as np
#input_force_vector = [Fx,Fz,Tau]
'''
        Y+
        |
        |<=
        |    =
        | = Theta
        ----------X+

'''

class Physics():
    def __init__(self, initial_state_vector, mass, mmoi):
        self.state_vector = initial_state_vector
        self.mass = mass
        self.mmoi = mmoi
        self.input_last = None
        self.actuator_state = []
    def inputForces(self, input_force_vector,dt):
        G = -9.18 
        self.state_vector["ay"] = (input_force_vector[0] / self.mass) + G
        self.state_vector["ax"] = input_force_vector[1] / self.mass
        self.state_vector["alpha"] = input_force_vector[2] / self.mmoi
        self.state_vector["vy"] += self.state_vector["ay"] * dt
        if(self.state_vector["py"] == 30 and self.state_vector["vy"] < 0):
            self.state_vector["vy"] = 0
        self.state_vector["vx"] += self.state_vector["ax"] * dt
        self.state_vector["omega"] += self.state_vector["alpha"] * dt
        self.state_vector["py"] += self.state_vector["vy"] * dt
        if self.state_vector["py"] < 0:
            self.state_vector["py"] = 0
        self.state_vector["px"] += self.state_vector["vx"] * dt
        self.state_vector["theta"] += self.state_vector["omega"] * dt
        return self.state_vector
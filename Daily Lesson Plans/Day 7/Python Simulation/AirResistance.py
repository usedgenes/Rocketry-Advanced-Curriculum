class AirResistance():
    def __init__(self, airDensity, crossSectionalArea):
        self.airDensity = airDensity
        self.crossSectionalArea = crossSectionalArea
        
    def getDrag(self, velocity, dragCoefficient):
        return 0.5*dragCoefficient*self.airDensity*self.crossSectionalArea*velocity*velocity
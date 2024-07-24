previousTime = 0;
error = 0;
derivative_error = 0;
output = 0;
class Airbrake():
    def __init__(self, KP, KI, KD, targetAltitude, closedDragCoefficient, openDragCoefficient):
        self.kp = KP
        self.ki = KI
        self.kd = KD        
        self.targetAltitude = targetAltitude
        self.error_last = 0
        self.integral_error = 0
        self.saturation_max = None
        self.saturation_min = None
        self.closedDragCoefficient = closedDragCoefficient
        self.openDragCoefficient = openDragCoefficient
    def compute(self, currentAltitude, currentTime):
        global previousTime
        global error
        global derivative_error
        global integral_error
        global output
        dt = currentTime - previousTime
        if(dt == 0):
            return 0;
        previousTime = currentTime
        error = self.targetAltitude - currentAltitude #compute the error
        derivative_error = (error - self.error_last) / dt #find the derivative of the error (how the error changes with time)
        self.integral_error += error * dt #error build up over time
        output = self.kp*error + self.ki*self.integral_error + self.kd*derivative_error 
        self.error_last = error
        if output > self.saturation_max and self.saturation_max is not None:
            output = self.saturation_max
        elif output < self.saturation_min and self.saturation_min is not None:
            output = self.saturation_min
        return (self.openDragCoefficient-self.closedDragCoefficient)*output
    
    def setLims(self,min,max):
        self.saturation_max = max
        self.saturation_min = min
        
    def getError(self):
        global error
        return error
    
    def getDerivativeError(self):
        global derivative_error
        return derivative_error
    
    def getIntegralError(self):
        return self.integral_error
    
    def getOutput(self):
        global output
        return output
import numpy as np
import time as Time
import Rocket 
import MotorThrustCurve as thrust
import Physics as phys
import Graphs as gh
import AirResistance as drag
import OldAirbrake
import Airbrake
import Altimeter

mass = 0.65
dragCoefficient = 0.45
openDragCoefficient = 0.8
airDensity = 1.2
area = 0.0034
cutoffFrequency = 0.9
initialAlpha = 0.03
targetAltitude = 850
maxEfficiency = 3
motorDelay = 1.5

motor = thrust.ThrustCurve("AeroTech_F67W.csv", 0.08, 0.03)

airResistance = drag.AirResistance(airDensity, area)

normalRocket = Rocket.Rocket(1600,1600, mass, 1, 500)
oldAirbrakeRocket = Rocket.Rocket(1600, 1600, mass, 1, 1000)
airbrakeRocket = Rocket.Rocket(1600,1600, mass, 1, 1500)

altimeter = Altimeter.Altimeter()

oldAirbrake = OldAirbrake.OldAirbrake(dragCoefficient, openDragCoefficient, airDensity, area, mass, cutoffFrequency, initialAlpha, targetAltitude, maxEfficiency, motorDelay)

airbrake = Airbrake.Airbrake(0.0002, 0.00005, 0.02, targetAltitude, dragCoefficient, openDragCoefficient)
airbrake.setLims(0, 1)

normalRocket_state_vector = {"ay" : 0 ,"vy" : 0,"py" : 0,"ax" : 0 ,"vx" : 0,"px" : normalRocket.getX() ,"alpha" : 0.0,"omega" : 0.5,"theta" : 0.0}
oldAirbrakeRocket_state_vector = {"ay" : 0 ,"vy" : 0,"py" : 0,"ax" : 0 ,"vx" : 0,"px" : oldAirbrakeRocket.getX() ,"alpha" : 0.0,"omega" : 0.5,"theta" : 0.0}
airbrakeRocket_state_vector = {"ay" : 0 ,"vy" : 0,"py" : 0,"ax" : 0 ,"vx" : 0,"px" : airbrakeRocket.getX() ,"alpha" : 0.0,"omega" : 0.5,"theta" : 0.0}

normalRocket_phys = phys.Physics(normalRocket_state_vector, normalRocket.mass, normalRocket.mmoi)
oldAirbrakeRocket_phys = phys.Physics(oldAirbrakeRocket_state_vector, oldAirbrakeRocket.mass, oldAirbrakeRocket.mmoi)
airbrakeRocket_phys = phys.Physics(airbrakeRocket_state_vector, airbrakeRocket.mass, airbrakeRocket.mmoi)


sim_time = 0.0
time_lim = 10
delta_t = 0.05

time = []
normalRocket_vert_pos = []
oldAirbrakeRocket_vert_pos = []
airbrakeRocket_vert_pos = []
projectedFilteredAltitude = []
error = []
derivativeError = []
integralError = []
output = []

normalRocket_vertical_pos = {"xlab" : "time(s)", "ylab" : "Normal Rocket Pos Y", "title" : "Normal Rocket"}
oldAirbrakeRocket_vertical_pos = {"xlab" : "time(s)", "ylab" : "Old Airbrake Rocket Pos Y", "title" : "Old Airbrake Rocket"}
airbrakeRocket_vertical_pos = {"xlab" : "time(s)", "ylab" : "Airbrake Rocket Pos Y", "title" : "Airbrake Rocket"}
projected_altitude = {"xlab" : "time(s)", "ylab" : "Projected Altitude", "title" : "Projected Altitude"}
error_graph = {"xlab" : "time(s)", "ylab" : "Error", "title" : "Error"}
derivativeError_graph = {"xlab" : "time(s)", "ylab" : "Derivative Error", "title" : "Derivative Error"}
integralError_graph = {"xlab" : "time(s)", "ylab" : "Integral Error", "title" : "Integral Error"}
output_graph = {"xlab" : "time(s)", "ylab" : "Output", "title" : "Output"}

graphs_dict = [normalRocket_vertical_pos, oldAirbrakeRocket_vertical_pos, airbrakeRocket_vertical_pos, projected_altitude, error_graph, integralError_graph, derivativeError_graph, output_graph]

graphics = gh.GraphHandler()
graphics.graphsHandler(8,graphs_dict)

Time.sleep(1)

while(sim_time < time_lim):
    thrust = motor.getThrust(sim_time)
    
    #Normal Rocket:
    drag = airResistance.getDrag(normalRocket_state_vector["vy"], dragCoefficient)
    normalRocket_state_vector = normalRocket_phys.inputForces([thrust - drag, 0, 0], delta_t)
    normalRocket.moveRocket(normalRocket_state_vector["px"], normalRocket_state_vector["py"])
    
    #Old Airbrake Rocket:
    altimeterAltitude = altimeter.getAltimeterData(oldAirbrakeRocket_state_vector)
    altimeterTime = altimeter.getTime(sim_time, delta_t)
    airbrakeDrag = oldAirbrake.getDrag(altimeterAltitude, altimeterTime)
    netVerticalForce = thrust - airResistance.getDrag(oldAirbrakeRocket_state_vector["vy"], dragCoefficient + airbrakeDrag)
    oldAirbrakeRocket_state_vector = oldAirbrakeRocket_phys.inputForces([netVerticalForce, 0, 0], delta_t)
    oldAirbrakeRocket.moveRocket(oldAirbrakeRocket_state_vector["px"], oldAirbrakeRocket_state_vector["py"])
    
    #Airbrake Rocket:
    pidDrag = airbrake.compute(altimeterAltitude, altimeterTime)
    netVerticalForce = thrust - airResistance.getDrag(airbrakeRocket_state_vector["vy"], dragCoefficient + pidDrag)
    airbrakeRocket_state_vector = airbrakeRocket_phys.inputForces([netVerticalForce, 0, 0], delta_t)
    airbrakeRocket.moveRocket(airbrakeRocket_state_vector["px"], airbrakeRocket_state_vector["py"])
    
    normalRocket_vert_pos.append(normalRocket.getY()-30)
    oldAirbrakeRocket_vert_pos.append(oldAirbrakeRocket.getY()-30)
    airbrakeRocket_vert_pos.append(airbrakeRocket.getY()-30)
    projectedFilteredAltitude.append(oldAirbrake.getFilteredProjectedAltitude())
    error.append(airbrake.getError())
    integralError.append(airbrake.getIntegralError())
    derivativeError.append(airbrake.getDerivativeError())
    output.append(airbrake.getOutput())
    graphs = [(time, normalRocket_vert_pos), (time, oldAirbrakeRocket_vert_pos), (time, airbrakeRocket_vert_pos), (time, projectedFilteredAltitude), (time, error), (time, integralError), (time, derivativeError), (time, output)]
    time.append(sim_time)
    sim_time += delta_t
    
graphics.showGraphs(graphs)


